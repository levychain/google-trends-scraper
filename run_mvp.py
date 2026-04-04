#!/usr/bin/env python3
"""
Google Trends Research MVP — Multi-Series Runner
Load series-specific configs (YAML) and execute research pipeline for any NBN series.

Usage:
  python3 run_mvp.py --config configs/wardesk.yaml [--discovery-only] [--open]
  python3 run_mvp.py --config configs/neurodivergent.yaml --open
  python3 run_mvp.py --config configs/firstyes.yaml
"""

import argparse
import logging
import sys
import yaml
from pathlib import Path

# Add this directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import scraper
from fetcher import CachedFetcher, FetcherError, RateLimitError
from analyzer import KeywordAnalyzer, KeywordMetrics
from reporter import HTMLReporter
import config as base_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def load_config(config_path: str) -> dict:
    """Load series configuration from YAML file."""
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(path, 'r') as f:
        config = yaml.safe_load(f)

    if not config:
        raise ValueError(f"Config file is empty: {config_path}")

    logger.info(f"Loaded config for {config.get('series', 'Unknown')}")
    return config


def run_discovery(fetcher: CachedFetcher, series_config: dict, args):
    """Run discovery mode to find trending opportunities."""
    logger.info(f"🔍 Discovery mode for {series_config['series']}")
    logger.info(f"   Intent domain: {series_config.get('intent_domain', 'N/A')}")

    # Use seed keywords as search anchors
    keywords = series_config.get('seed_keywords', [])
    reference = series_config.get('reference_keywords', [])

    if not keywords:
        logger.error("No seed keywords defined in config")
        sys.exit(1)

    logger.info(f"   Seed keywords: {len(keywords)}")
    logger.info(f"   Reference benchmarks: {len(reference) if reference else 0}")

    # Fetch data
    try:
        all_keywords = list(dict.fromkeys(keywords + (reference or [])))
        if len(all_keywords) > base_config.MAX_KEYWORDS_PER_REQUEST:
            logger.warning(
                f"Total keywords ({len(all_keywords)}) exceeds max per request. "
                f"Fetching batches..."
            )

        metrics, interest_df, regions_df = scraper.fetch_data_for_keywords(
            fetcher,
            all_keywords,
            series_config.get('timeframe', base_config.DEFAULT_TIMEFRAME),
            series_config.get('geo', base_config.DEFAULT_GEO),
        )

        if not metrics:
            logger.error("No data retrieved from Google Trends")
            sys.exit(1)

        # Analyze
        analyzer = KeywordAnalyzer()

        if reference:
            ref_keywords = [kw for kw in reference if kw in metrics]
            if ref_keywords:
                logger.info(f"Setting reference benchmarks: {ref_keywords}")
                analyzer.set_reference_keywords(ref_keywords, metrics)

        # Score all keywords
        scores = {}
        for keyword in keywords:
            if keyword in metrics:
                kw_score = analyzer.score_keyword(keyword, metrics[keyword])
                scores[keyword] = kw_score

        # Sort by score
        sorted_keywords = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        logger.info(f"\n📊 Opportunity Scores for {series_config['series']}:")
        logger.info("-" * 60)
        for keyword, score in sorted_keywords:
            if score >= base_config.MIN_DISCOVERY_SCORE:
                logger.info(f"  {keyword:40s} Score: {score:.1f}")

        logger.info("-" * 60)
        logger.info(f"Found {len([s for _, s in sorted_keywords if s >= base_config.MIN_DISCOVERY_SCORE])} opportunities")

        # Generate report if not discovery-only
        if not args.discovery_only:
            report = HTMLReporter()
            report_path = report.generate(
                metrics=metrics,
                scores=scores,
                keyword_source=f"{series_config['series']} - Discovery Mode",
                timeframe=series_config.get('timeframe', base_config.DEFAULT_TIMEFRAME),
            )
            logger.info(f"\n✅ Report saved: {report_path}")

            if args.open:
                import webbrowser
                webbrowser.open(f"file://{report_path}")
                logger.info("   Opening in browser...")

        return True

    except (FetcherError, RateLimitError) as e:
        logger.error(f"Fetcher error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Google Trends Research MVP - Multi-Series Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run War Desk discovery
  python3 run_mvp.py --config configs/wardesk.yaml --open

  # Run Neurodivergent discovery without report
  python3 run_mvp.py --config configs/neurodivergent.yaml --discovery-only

  # Run The First Yes research
  python3 run_mvp.py --config configs/firstyes.yaml
        """,
    )

    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to series config YAML file (e.g., configs/wardesk.yaml)",
    )

    parser.add_argument(
        "--discovery-only",
        action="store_true",
        help="Run discovery analysis without generating HTML report",
    )

    parser.add_argument(
        "--open",
        action="store_true",
        help="Open HTML report in browser after generation",
    )

    args = parser.parse_args()

    # Load config
    try:
        series_config = load_config(args.config)
    except (FileNotFoundError, ValueError, yaml.YAMLError) as e:
        logger.error(f"Config load failed: {e}")
        sys.exit(1)

    # Initialize fetcher
    fetcher = CachedFetcher()

    # Run discovery
    try:
        run_discovery(fetcher, series_config, args)
        logger.info(f"\n✅ Research complete for {series_config['series']}")
    except KeyboardInterrupt:
        logger.info("\n⚠️  Research interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Research failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
