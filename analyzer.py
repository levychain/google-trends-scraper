"""
Analyzer module: Opportunity scoring and keyword comparison engine.
Compares keywords against reference benchmarks to find comparable opportunities.
"""

import logging
from dataclasses import dataclass
from typing import Optional

import pandas as pd
import numpy as np

import config

logger = logging.getLogger(__name__)


@dataclass
class KeywordMetrics:
    """Metrics for a single keyword."""
    keyword: str
    avg_interest: float
    max_interest: float
    min_interest: float
    volatility: float
    momentum: float  # Slope: last 6mo vs prior 6mo
    breakout_queries_count: int
    related_queries_count: int
    rising_queries_count: int
    recent_peak: bool  # Peaked in last 90 days?
    recent_peak_value: float


@dataclass
class ComparisonScore:
    """Similarity score comparing keyword to reference benchmarks."""
    keyword: str
    similarity_score: float  # 0-100: how similar to reference keywords
    avg_interest_gap: float  # How close is avg_interest to reference avg
    momentum_gap: float  # How close is momentum to reference momentum
    breadth_gap: float  # How close is related_query count to reference count
    metrics: KeywordMetrics


class KeywordAnalyzer:
    """Analyzes keywords and compares them to reference benchmarks."""

    def __init__(self):
        self.reference_metrics = {}

    def extract_metrics(
        self, keyword: str, interest_df: pd.DataFrame, related_queries: dict
    ) -> KeywordMetrics:
        """Extract metrics from interest_over_time and related_queries data."""

        # Interest statistics
        avg_interest = interest_df[keyword].mean() if keyword in interest_df.columns else 0
        max_interest = interest_df[keyword].max() if keyword in interest_df.columns else 0
        min_interest = interest_df[keyword].min() if keyword in interest_df.columns else 0
        volatility = interest_df[keyword].std() if keyword in interest_df.columns else 0

        # Momentum: compare last 6 months to prior 6 months
        if len(interest_df) >= 26:  # At least 26 weeks for 6mo+6mo split
            mid = len(interest_df) // 2
            last_6mo = interest_df.iloc[mid:][keyword].values
            prior_6mo = interest_df.iloc[:mid][keyword].values

            last_6mo_trend = np.polyfit(range(len(last_6mo)), last_6mo, 1)[0]
            prior_6mo_trend = np.polyfit(range(len(prior_6mo)), prior_6mo, 1)[0]

            # Momentum = ratio of recent trend to prior trend
            if prior_6mo_trend != 0:
                momentum = last_6mo_trend / prior_6mo_trend
            else:
                momentum = last_6mo_trend
        else:
            # Fallback: simple linear trend over entire period
            x = np.arange(len(interest_df))
            momentum = np.polyfit(x, interest_df[keyword].values, 1)[0]

        # Related queries
        rq_data = related_queries.get(keyword, {})
        top_queries = rq_data.get("top", [])
        rising_queries = rq_data.get("rising", [])

        # Count breakout queries (usually marked with "Breakout" status)
        breakout_count = sum(
            1 for q in rising_queries
            if isinstance(q, dict) and q.get("isPartial") == True
        )

        related_count = len(top_queries)
        rising_count = len(rising_queries)

        # Recent peak: did it peak in last 90 days?
        recent_peak = False
        recent_peak_value = 0.0
        if len(interest_df) >= 13:  # At least 13 weeks
            recent_weeks = interest_df.iloc[-13:][keyword]
            recent_peak = recent_weeks.max() > interest_df[keyword].quantile(0.75)
            recent_peak_value = float(recent_weeks.max())

        return KeywordMetrics(
            keyword=keyword,
            avg_interest=float(avg_interest),
            max_interest=float(max_interest),
            min_interest=float(min_interest),
            volatility=float(volatility),
            momentum=float(momentum),
            breakout_queries_count=breakout_count,
            related_queries_count=related_count,
            rising_queries_count=rising_count,
            recent_peak=recent_peak,
            recent_peak_value=recent_peak_value,
        )

    def set_reference_keywords(self, reference_keywords: list[str], metrics_dict: dict[str, KeywordMetrics]) -> None:
        """Set reference benchmarks from reference keywords."""
        self.reference_metrics = {kw: metrics_dict[kw] for kw in reference_keywords if kw in metrics_dict}

        if self.reference_metrics:
            ref_avgs = [m.avg_interest for m in self.reference_metrics.values()]
            ref_momentums = [m.momentum for m in self.reference_metrics.values()]
            ref_breadths = [m.related_queries_count for m in self.reference_metrics.values()]

            self.reference_avg_interest = np.mean(ref_avgs)
            self.reference_momentum = np.mean(ref_momentums)
            self.reference_breadth = np.mean(ref_breadths)

            logger.info(
                f"Reference benchmarks set: "
                f"avg_interest={self.reference_avg_interest:.1f}, "
                f"momentum={self.reference_momentum:.2f}, "
                f"breadth={self.reference_breadth:.0f}"
            )

    def compare_to_reference(self, keyword: str, metrics: KeywordMetrics) -> ComparisonScore:
        """Compare a keyword to reference benchmarks."""

        if not self.reference_metrics:
            raise ValueError("Reference keywords not set. Call set_reference_keywords() first.")

        # Calculate gaps (lower is better, 0 = perfect match)
        avg_interest_gap = abs(metrics.avg_interest - self.reference_avg_interest)
        momentum_gap = abs(metrics.momentum - self.reference_momentum)
        breadth_gap = abs(metrics.related_queries_count - self.reference_breadth)

        # Normalize gaps to 0-100 scale (inverse: closer to ref = higher score)
        # Adjust scales based on typical values
        max_interest_gap = max(self.reference_avg_interest, 50)  # Max reasonable difference
        max_momentum_gap = 2.0  # Momentum can be negative or positive
        max_breadth_gap = max(self.reference_breadth, 20)

        interest_score = max(0, 100 - (avg_interest_gap / max_interest_gap) * 100)
        momentum_score = max(0, 100 - (momentum_gap / max_momentum_gap) * 100)
        breadth_score = max(0, 100 - (breadth_gap / max_breadth_gap) * 100)

        # Composite similarity score: weighted average
        weights = {
            "interest": 0.35,
            "momentum": 0.35,
            "breadth": 0.30,
        }

        similarity_score = (
            interest_score * weights["interest"]
            + momentum_score * weights["momentum"]
            + breadth_score * weights["breadth"]
        )

        return ComparisonScore(
            keyword=keyword,
            similarity_score=float(similarity_score),
            avg_interest_gap=float(avg_interest_gap),
            momentum_gap=float(momentum_gap),
            breadth_gap=float(breadth_gap),
            metrics=metrics,
        )

    def get_opportunity_score(self, metrics: KeywordMetrics) -> float:
        """Calculate standalone opportunity score (0-100) for a keyword."""
        score = 0.0

        # Avg interest (25%)
        if metrics.avg_interest >= config.MIN_AVG_INTEREST:
            interest_component = min(100, (metrics.avg_interest / 80) * 100)
        else:
            interest_component = 0
        score += interest_component * config.OPPORTUNITY_WEIGHTS["avg_interest"]

        # Momentum (25%)
        momentum_component = max(0, min(100, (metrics.momentum + 1) * 50))  # Range [-1, 3] → [0, 100]
        score += momentum_component * config.OPPORTUNITY_WEIGHTS["momentum"]

        # Breakout queries (20%)
        breakout_component = min(100, (metrics.breakout_queries_count / config.MIN_BREAKOUT_QUERIES) * 50)
        score += breakout_component * config.OPPORTUNITY_WEIGHTS["breakout_queries"]

        # Breadth (15%)
        breadth_component = min(100, (metrics.related_queries_count / config.MIN_RELATED_QUERIES) * 50)
        score += breadth_component * config.OPPORTUNITY_WEIGHTS["breadth"]

        # Recency (15%)
        recency_component = 50 if metrics.recent_peak else 0
        score += recency_component * config.OPPORTUNITY_WEIGHTS["recency"]

        return score
