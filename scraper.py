#!/usr/bin/env python3
"""
Google Trends Scraper CLI - Research comparable keywords at Epstein Files scale.
Find keywords with similar search patterns, momentum, and related-query breadth.
"""

import argparse
import logging
import sys
import webbrowser
from pathlib import Path

import pandas as pd

import config
from fetcher import CachedFetcher, FetcherError, RateLimitError
from analyzer import KeywordAnalyzer, KeywordMetrics
from reporter import HTMLReporter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def parse_keywords(keywords_str: str) -> list[str]:
    """Parse comma-separated keywords."""
    return [kw.strip() for kw in keywords_str.split(",") if kw.strip()]


def fetch_data_for_keywords(
    fetcher: CachedFetcher,
    keywords: list[str],
    timeframe: str,
    geo: str,
    batch_size: int = config.MAX_KEYWORDS_PER_REQUEST,
):
    """Fetch data for keywords, batching to respect pytrends limits."""

    all_metrics = {}
    all_interest = pd.DataFrame()
    all_regions = pd.DataFrame()
    all_related = {}

    # Process keywords in batches (pytrends max 5 per request)
    for i in range(0, len(keywords), batch_size):
        batch = keywords[i : i + batch_size]
        logger.info(f"Processing batch {i // batch_size + 1}: {batch}")

        try:
            # Fetch data for this batch
            interest_df = fetcher.interest_over_time(batch, timeframe=timeframe, geo=geo)
            related = fetcher.related_queries(batch, timeframe=timeframe, geo=geo)

            # Concatenate with overall dataframes
            for col in interest_df.columns:
                if col not in ["isPartial"]:
                    all_interest[col] = interest_df[col]

            for kw in batch:
                if kw in related:
                    all_related[kw] = related[kw]

            # Try regional data (only for single keyword)
            if len(batch) == 1:
                try:
                    regions_df = fetcher.interest_by_region(
                        batch, timeframe=timeframe, geo=geo
                    )
                    for col in regions_df.columns:
                        if col != "isPartial":
                            all_regions[col] = regions_df[col]
                except Exception as e:
                    logger.warning(f"Failed to fetch regional data: {e}")

        except RateLimitError as e:
            logger.error(f"Rate limited: {e}")
            logger.error("Try again in a few minutes or use cached data.")
            raise
        except Exception as e:
            logger.error(f"Error fetching data for {batch}: {e}")
            raise

    # Extract metrics for each keyword
    for keyword in keywords:
        try:
            metrics = KeywordAnalyzer().extract_metrics(keyword, all_interest, all_related)
            all_metrics[keyword] = metrics
        except Exception as e:
            logger.error(f"Failed to extract metrics for {keyword}: {e}")

    return all_metrics, all_interest, all_regions


def cmd_research(args):
    """Research mode: Compare specific keywords."""

    logger.info(f"Research mode: {args.keywords}")
    keywords = parse_keywords(args.keywords)

    if not keywords:
        logger.error("No keywords provided")
        sys.exit(1)

    if len(keywords) > config.MAX_KEYWORDS_PER_REQUEST:
        logger.warning(
            f"Limited to {config.MAX_KEYWORDS_PER_REQUEST} keywords per request. "
            f"Fetching {keywords[:config.MAX_KEYWORDS_PER_REQUEST]}"
        )
        keywords = keywords[:config.MAX_KEYWORDS_PER_REQUEST]

    fetcher = CachedFetcher()

    # Include reference keywords in the fetch so comparison works
    ref_keywords = parse_keywords(args.reference) if args.reference else []
    all_keywords_to_fetch = list(dict.fromkeys(keywords + ref_keywords))  # dedup, preserve order
    if len(all_keywords_to_fetch) > config.MAX_KEYWORDS_PER_REQUEST:
        logger.warning(
            f"Total keywords ({len(all_keywords_to_fetch)}) exceeds max per request ({config.MAX_KEYWORDS_PER_REQUEST}). "
            f"Reference keywords will be fetched in a separate batch."
        )

    try:
        # Fetch data for all keywords including references
        logger.info("Fetching data from Google Trends...")
        metrics, interest_df, regions_df = fetch_data_for_keywords(
            fetcher, all_keywords_to_fetch, args.timeframe, args.geo
        )

        if not metrics:
            logger.error("No data retrieved")
            sys.exit(1)

        # Analyze: set reference benchmarks and compare
        analyzer = KeywordAnalyzer()

        # If reference keywords specified, use them as benchmarks
        if args.reference:
            ref_keywords = [kw for kw in ref_keywords if kw in metrics]

            if ref_keywords:
                logger.info(f"Using reference benchmarks: {ref_keywords}")
                analyzer.set_reference_keywords(ref_keywords, metrics)

                # Compare all keywords to reference
                scores = {}
                for keyword in keywords:
                    if keyword in metrics:
                        score = analyzer.compare_to_reference(keyword, metrics[keyword])
                        scores[keyword] = score
                        logger.info(
                            f"{keyword}: similarity={score.similarity_score:.1f} "
                            f"(interest_gap={score.avg_interest_gap:.1f}, "
                            f"momentum_gap={score.momentum_gap:.2f})"
                        )
            else:
                logger.warning("Reference keywords not found in results")
                scores = None
        else:
            scores = None

        # Generate reports
        if args.report:
            logger.info("Generating HTML report...")
            reporter = HTMLReporter(config.REPORTS_DIR)
            report_path = reporter.generate_research_report(
                keywords, interest_df, regions_df, metrics, scores
            )

            logger.info(f"Report saved to {report_path}")

            # Open in browser
            if args.open:
                logger.info("Opening report in browser...")
                webbrowser.open(f"file://{report_path.absolute()}")

        # Export data
        if args.csv or args.json:
            reporter = HTMLReporter()
            for keyword in keywords:
                if keyword in metrics:
                    if args.csv:
                        reporter.export_csv(keyword, interest_df, regions_df)
                    if args.json:
                        reporter.export_json(keyword, metrics[keyword])

        logger.info("Done!")

    except RateLimitError:
        logger.error("Google Trends rate limited. Use cached data or try again later.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


def cmd_discover(args):
    """Discovery mode: Find trending opportunities."""

    logger.info(f"Discovery mode: {args.geo}")
    fetcher = CachedFetcher()

    try:
        logger.info("Fetching trending searches...")
        trending_df = fetcher.trending_searches(geo=args.geo)

        if trending_df.empty:
            logger.error("No trending data available")
            sys.exit(1)

        logger.info(f"Found {len(trending_df)} trending searches")

        # Get top N trending terms
        trending_keywords = trending_df.iloc[:20, 0].tolist() if len(trending_df.columns) > 0 else []

        if not trending_keywords:
            logger.error("Could not extract keywords from trending data")
            sys.exit(1)

        logger.info(f"Analyzing top trends: {trending_keywords[:5]}...")

        # Fetch detailed data for trending keywords
        metrics, interest_df, regions_df = fetch_data_for_keywords(
            fetcher, trending_keywords[:10], "now 7-d", args.geo
        )

        # Score each keyword
        analyzer = KeywordAnalyzer()
        opportunities = []

        for keyword in trending_keywords[:10]:
            if keyword in metrics:
                score = analyzer.get_opportunity_score(metrics[keyword])
                if score >= config.MIN_DISCOVERY_SCORE:
                    opportunities.append((keyword, score, metrics[keyword]))

        opportunities.sort(key=lambda x: x[1], reverse=True)

        # Display results
        logger.info("\n=== TOP DISCOVERY OPPORTUNITIES ===\n")
        for rank, (keyword, score, m) in enumerate(opportunities[:10], 1):
            logger.info(
                f"{rank}. {keyword} (Score: {score:.1f}) - "
                f"Interest: {m.avg_interest:.1f}, "
                f"Queries: {m.related_queries_count}, "
                f"Rising: {m.rising_queries_count}"
            )

        # Generate report
        if args.report:
            logger.info("Generating discovery report...")
            reporter = HTMLReporter(config.REPORTS_DIR)
            # For discovery, show top opportunities
            discovery_keywords = [kw for kw, _, _ in opportunities[:5]]
            if discovery_keywords:
                report_path = reporter.generate_research_report(
                    discovery_keywords, interest_df, regions_df, metrics
                )
                logger.info(f"Report saved to {report_path}")

                if args.open:
                    webbrowser.open(f"file://{report_path.absolute()}")

        logger.info("Done!")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Google Trends Scraper - Find keywords comparable to Epstein Files scale.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare specific keywords
  python scraper.py --keywords "topic1,topic2,topic3" --timeframe "today 12-m" --geo US --report

  # Find trending opportunities
  python scraper.py --discover --geo US

  # Export data without report
  python scraper.py --keywords "test" --csv --json --no-report
        """,
    )

    parser.add_argument(
        "--keywords",
        type=str,
        help="Comma-separated keywords to research (max 5)",
    )

    parser.add_argument(
        "--reference",
        type=str,
        help="Reference keywords to compare against (e.g., 'Jeffrey Epstein,Harvey Weinstein')",
    )

    parser.add_argument(
        "--timeframe",
        type=str,
        default=config.DEFAULT_TIMEFRAME,
        help=f"Timeframe for data (default: {config.DEFAULT_TIMEFRAME}). "
        "Examples: 'now 1-d', 'today 1-m', 'today 12-m', 'today 5-y'",
    )

    parser.add_argument(
        "--geo",
        type=str,
        default=config.DEFAULT_GEO,
        help=f"Geographic region (default: {config.DEFAULT_GEO}). Examples: US, GB, CA",
    )

    parser.add_argument(
        "--discover",
        action="store_true",
        help="Discovery mode: analyze trending searches instead of specified keywords",
    )

    parser.add_argument(
        "--report",
        action="store_true",
        default=True,
        help="Generate HTML report (default: True)",
    )

    parser.add_argument(
        "--no-report",
        action="store_false",
        dest="report",
        help="Skip HTML report generation",
    )

    parser.add_argument(
        "--open",
        action="store_true",
        help="Open report in browser after generation",
    )

    parser.add_argument(
        "--csv",
        action="store_true",
        help="Export data as CSV",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Export data as JSON",
    )

    args = parser.parse_args()

    # Route to appropriate command
    if args.discover:
        cmd_discover(args)
    elif args.keywords:
        cmd_research(args)
    else:
        parser.print_help()
        logger.error("Either --keywords or --discover must be specified")
        sys.exit(1)


if __name__ == "__main__":
    main()
