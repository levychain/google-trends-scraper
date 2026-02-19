"""
Fetcher module: pytrends wrapper with rate limiting, retries, and caching.
"""

import json
import time
from pathlib import Path
from datetime import datetime, timedelta
import logging

import pandas as pd
from pytrends.request import TrendReq
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
import requests

import config

logger = logging.getLogger(__name__)


class FetcherError(Exception):
    """Base exception for fetcher errors."""
    pass


class RateLimitError(FetcherError):
    """Raised when Google Trends rate limits are hit."""
    pass


class CachedFetcher:
    """Wrapper around pytrends with rate limiting, retries, and caching."""

    def __init__(self, backoff_seconds=config.REQUEST_BACKOFF_SECONDS):
        self.backoff_seconds = backoff_seconds
        self.last_request_time = 0
        self.hl = "en-US"
        self.tz = 360

    def _get_cache_path(self, key: str) -> Path:
        """Generate cache file path for a key."""
        filename = f"{key}.json"
        return config.CACHE_DIR / filename

    def _is_cache_fresh(self, cache_path: Path) -> bool:
        """Check if cache file exists and is fresh (< TTL)."""
        if not cache_path.exists():
            return False

        mtime = cache_path.stat().st_mtime
        age = time.time() - mtime
        return age < config.CACHE_TTL_SECONDS

    def _load_cache(self, key: str) -> dict | None:
        """Load data from cache if it exists and is fresh."""
        cache_path = self._get_cache_path(key)

        if self._is_cache_fresh(cache_path):
            try:
                with open(cache_path) as f:
                    data = json.load(f)
                    logger.info(f"Loaded from cache: {key}")
                    return data
            except Exception as e:
                logger.warning(f"Failed to load cache for {key}: {e}")
                return None

        return None

    def _save_cache(self, key: str, data: dict) -> None:
        """Save data to cache."""
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, "w") as f:
                json.dump(data, f, indent=2, default=str)
                logger.debug(f"Cached: {key}")
        except Exception as e:
            logger.warning(f"Failed to cache {key}: {e}")

    def _apply_backoff(self) -> None:
        """Apply rate limit backoff between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.backoff_seconds:
            sleep_time = self.backoff_seconds - elapsed
            logger.info(f"Rate limit backoff: sleeping {sleep_time:.1f}s")
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    @retry(
        stop=stop_after_attempt(config.RETRY_MAX_ATTEMPTS),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((RateLimitError, requests.ConnectionError)),
        reraise=True,
    )
    def _fetch_with_retry(self, fetch_fn, *args, **kwargs):
        """Execute fetch function with retry logic."""
        try:
            self._apply_backoff()
            return fetch_fn(*args, **kwargs)
        except Exception as e:
            if "429" in str(e) or "503" in str(e):
                raise RateLimitError(f"Rate limited by Google Trends: {e}")
            raise

    def interest_over_time(
        self,
        keywords: list[str],
        timeframe: str = config.DEFAULT_TIMEFRAME,
        geo: str = config.DEFAULT_GEO,
        cat: int = config.DEFAULT_CATEGORY,
    ) -> pd.DataFrame:
        """Fetch interest over time for keywords."""
        cache_key = f"interest_over_time_{'_'.join(sorted(keywords))}_{timeframe}_{geo}"

        cached = self._load_cache(cache_key)
        if cached:
            return pd.DataFrame(cached)

        logger.info(f"Fetching interest_over_time: {keywords}")
        pytrends = TrendReq(hl=self.hl, tz=self.tz)

        df = self._fetch_with_retry(
            pytrends.build_payload,
            keywords,
            timeframe=timeframe,
            geo=geo,
            cat=cat,
        )

        df_data = self._fetch_with_retry(pytrends.interest_over_time)

        # Convert to serializable format
        cache_data = df_data.to_dict(orient="list")
        self._save_cache(cache_key, cache_data)

        return df_data

    def related_queries(
        self,
        keywords: list[str],
        timeframe: str = config.DEFAULT_TIMEFRAME,
        geo: str = config.DEFAULT_GEO,
        cat: int = config.DEFAULT_CATEGORY,
    ) -> dict:
        """Fetch related queries for keywords."""
        cache_key = f"related_queries_{'_'.join(sorted(keywords))}_{timeframe}_{geo}"

        cached = self._load_cache(cache_key)
        if cached:
            return cached

        logger.info(f"Fetching related_queries: {keywords}")
        pytrends = TrendReq(hl=self.hl, tz=self.tz)

        self._fetch_with_retry(
            pytrends.build_payload,
            keywords,
            timeframe=timeframe,
            geo=geo,
            cat=cat,
        )

        related = self._fetch_with_retry(pytrends.related_queries)

        # Convert to serializable format
        cache_data = {}
        for kw, df_dict in related.items():
            if df_dict is None:
                # pytrends returns None for keywords with no related query data
                cache_data[kw] = {"top": [], "rising": []}
            else:
                # Handle cases where top/rising might be None or empty
                top_data = []
                rising_data = []

                if df_dict.get("top") is not None and not df_dict["top"].empty:
                    top_data = df_dict["top"].to_dict(orient="records")

                if df_dict.get("rising") is not None and not df_dict["rising"].empty:
                    rising_data = df_dict["rising"].to_dict(orient="records")

                cache_data[kw] = {"top": top_data, "rising": rising_data}

        self._save_cache(cache_key, cache_data)
        return cache_data

    def related_topics(
        self,
        keywords: list[str],
        timeframe: str = config.DEFAULT_TIMEFRAME,
        geo: str = config.DEFAULT_GEO,
        cat: int = config.DEFAULT_CATEGORY,
    ) -> dict:
        """Fetch related topics for keywords."""
        cache_key = f"related_topics_{'_'.join(sorted(keywords))}_{timeframe}_{geo}"

        cached = self._load_cache(cache_key)
        if cached:
            return cached

        logger.info(f"Fetching related_topics: {keywords}")
        pytrends = TrendReq(hl=self.hl, tz=self.tz)

        self._fetch_with_retry(
            pytrends.build_payload,
            keywords,
            timeframe=timeframe,
            geo=geo,
            cat=cat,
        )

        topics = self._fetch_with_retry(pytrends.related_topics)

        # Convert to serializable format
        cache_data = {}
        for kw, df_dict in topics.items():
            if df_dict is None:
                # pytrends returns None for keywords with no related topic data
                cache_data[kw] = {"top": [], "rising": []}
            else:
                # Handle cases where top/rising might be None or empty
                top_data = []
                rising_data = []

                if df_dict.get("top") is not None and not df_dict["top"].empty:
                    top_data = df_dict["top"].to_dict(orient="records")

                if df_dict.get("rising") is not None and not df_dict["rising"].empty:
                    rising_data = df_dict["rising"].to_dict(orient="records")

                cache_data[kw] = {"top": top_data, "rising": rising_data}

        self._save_cache(cache_key, cache_data)
        return cache_data

    def interest_by_region(
        self,
        keywords: list[str],
        timeframe: str = config.DEFAULT_TIMEFRAME,
        geo: str = config.DEFAULT_GEO,
        cat: int = config.DEFAULT_CATEGORY,
        resolution: str = "COUNTRY",
    ) -> pd.DataFrame:
        """Fetch interest by region for keywords."""
        cache_key = f"interest_by_region_{'_'.join(sorted(keywords))}_{timeframe}_{geo}_{resolution}"

        cached = self._load_cache(cache_key)
        if cached:
            return pd.DataFrame(cached)

        logger.info(f"Fetching interest_by_region: {keywords}")
        pytrends = TrendReq(hl=self.hl, tz=self.tz)

        self._fetch_with_retry(
            pytrends.build_payload,
            keywords,
            timeframe=timeframe,
            geo=geo,
            cat=cat,
        )

        df_data = self._fetch_with_retry(pytrends.interest_by_region, inc_low_vol=True, inc_geo_code=False)

        # Convert to serializable format
        cache_data = df_data.to_dict(orient="list")
        self._save_cache(cache_key, cache_data)

        return df_data

    def trending_searches(self, geo: str = config.DEFAULT_GEO) -> pd.DataFrame:
        """Fetch today's trending searches for a region."""
        cache_key = f"trending_searches_{geo}"

        cached = self._load_cache(cache_key)
        if cached:
            return pd.DataFrame(cached)

        logger.info(f"Fetching trending_searches: {geo}")
        pytrends = TrendReq(hl=self.hl, tz=self.tz)

        df_data = self._fetch_with_retry(pytrends.trending_searches, pn=geo)

        # Convert to serializable format
        cache_data = df_data.to_dict(orient="list")
        self._save_cache(cache_key, cache_data)

        return df_data

    def realtime_search_trends(self, geo: str = config.DEFAULT_GEO, cat: str = "all") -> pd.DataFrame:
        """Fetch real-time search trends for a region."""
        cache_key = f"realtime_trends_{geo}_{cat}"

        cached = self._load_cache(cache_key)
        if cached:
            return pd.DataFrame(cached)

        logger.info(f"Fetching realtime_search_trends: {geo}")
        pytrends = TrendReq(hl=self.hl, tz=self.tz)

        df_data = self._fetch_with_retry(pytrends.realtime_trending_searches, pn=geo, cat=cat)

        # Convert to serializable format
        cache_data = df_data.to_dict(orient="list")
        self._save_cache(cache_key, cache_data)

        return df_data
