"""
Reporter module: Generate HTML reports with Plotly charts and data exports.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

import config
from analyzer import KeywordMetrics, ComparisonScore

logger = logging.getLogger(__name__)


class HTMLReporter:
    """Generate HTML reports with Plotly charts."""

    def __init__(self, output_dir: Path = config.REPORTS_DIR):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _generate_timestamp(self) -> str:
        """Generate timestamp for report filenames."""
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def _generate_html_header(self, title: str) -> str:
        """Generate HTML header."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>{title}</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: #f5f5f5;
                }}
                .container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #1a1a1a;
                    border-bottom: 3px solid #4285f4;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #333;
                    margin-top: 30px;
                    margin-bottom: 15px;
                }}
                .chart-container {{
                    margin: 30px 0;
                    border: 1px solid #eee;
                    border-radius: 4px;
                    overflow: hidden;
                }}
                .summary-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                .summary-table th, .summary-table td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                .summary-table th {{
                    background-color: #f8f9fa;
                    font-weight: 600;
                    color: #333;
                }}
                .summary-table tr:hover {{
                    background-color: #f5f5f5;
                }}
                .score {{
                    font-weight: 600;
                    padding: 4px 8px;
                    border-radius: 4px;
                }}
                .score.high {{
                    background-color: #c8e6c9;
                    color: #1b5e20;
                }}
                .score.medium {{
                    background-color: #fff9c4;
                    color: #f57f17;
                }}
                .score.low {{
                    background-color: #ffcccc;
                    color: #b71c1c;
                }}
                .metric {{
                    display: inline-block;
                    padding: 8px 12px;
                    margin: 4px 8px 4px 0;
                    background: #f0f0f0;
                    border-radius: 4px;
                    font-size: 14px;
                }}
                .timestamp {{
                    color: #999;
                    font-size: 12px;
                    margin-top: 20px;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
        <div class="container">
            <h1>{title}</h1>
        """

    def _generate_html_footer(self) -> str:
        """Generate HTML footer."""
        return f"""
            <div class="timestamp">Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        </body>
        </html>
        """

    def generate_research_report(
        self,
        keywords: list[str],
        interest_df: pd.DataFrame,
        regions_df: pd.DataFrame,
        metrics: dict[str, KeywordMetrics],
        scores: Optional[dict[str, ComparisonScore]] = None,
    ) -> Path:
        """Generate comprehensive research report comparing keywords."""

        timestamp = self._generate_timestamp()
        filename = f"research_{timestamp}.html"
        filepath = self.output_dir / filename

        html_parts = [
            self._generate_html_header(f"Google Trends Research: {', '.join(keywords)}")
        ]

        # Summary table
        html_parts.append("<h2>Summary</h2>")
        html_parts.append(self._generate_summary_table(keywords, metrics, scores))

        # Interest over time chart
        html_parts.append("<h2>Interest Over Time</h2>")
        html_parts.append(self._generate_interest_chart(interest_df, keywords))

        # Metrics breakdown
        for keyword in keywords:
            if keyword in metrics:
                html_parts.append(f"<h2>{keyword} - Detailed Metrics</h2>")
                html_parts.append(self._generate_metrics_section(metrics[keyword]))

        # Regional interest
        if not regions_df.empty:
            html_parts.append("<h2>Regional Interest</h2>")
            html_parts.append(self._generate_region_heatmap(regions_df, keywords))

        html_parts.append(self._generate_html_footer())

        with open(filepath, "w") as f:
            f.write("\n".join(html_parts))

        logger.info(f"Report generated: {filepath}")
        return filepath

    def _generate_summary_table(
        self,
        keywords: list[str],
        metrics: dict[str, KeywordMetrics],
        scores: Optional[dict[str, ComparisonScore]] = None,
    ) -> str:
        """Generate summary table HTML."""

        rows = []
        for keyword in keywords:
            if keyword not in metrics:
                continue

            m = metrics[keyword]

            # Determine score color
            if scores and keyword in scores:
                score_val = scores[keyword].similarity_score
                score_class = "high" if score_val >= 70 else "medium" if score_val >= 50 else "low"
                score_html = f'<span class="score {score_class}">{score_val:.1f}</span>'
            else:
                score_html = "—"

            rows.append(f"""
            <tr>
                <td><strong>{keyword}</strong></td>
                <td>{m.avg_interest:.1f}</td>
                <td>{m.max_interest:.0f}</td>
                <td>{m.momentum:.2f}</td>
                <td>{m.related_queries_count}</td>
                <td>{m.rising_queries_count}</td>
                <td>{score_html}</td>
            </tr>
            """)

        table = f"""
        <table class="summary-table">
            <thead>
                <tr>
                    <th>Keyword</th>
                    <th>Avg Interest</th>
                    <th>Max Interest</th>
                    <th>Momentum</th>
                    <th>Related Queries</th>
                    <th>Rising Queries</th>
                    <th>Similarity Score</th>
                </tr>
            </thead>
            <tbody>
                {"".join(rows)}
            </tbody>
        </table>
        """
        return table

    def _generate_interest_chart(self, interest_df: pd.DataFrame, keywords: list[str]) -> str:
        """Generate interest over time Plotly chart."""

        fig = go.Figure()

        for keyword in keywords:
            if keyword in interest_df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=interest_df.index,
                        y=interest_df[keyword],
                        mode="lines",
                        name=keyword,
                        line=dict(width=3),
                    )
                )

        fig.update_layout(
            title="Interest Over Time",
            xaxis_title="Date",
            yaxis_title="Search Interest (0-100)",
            hovermode="x unified",
            height=500,
            template="plotly_white",
        )

        return f'<div class="chart-container">{fig.to_html(include_plotlyjs=False, div_id="interest_chart")}</div>'

    def _generate_metrics_section(self, metrics: KeywordMetrics) -> str:
        """Generate detailed metrics section for a keyword."""

        return f"""
        <div style="padding: 15px; background: #f9f9f9; border-radius: 4px;">
            <div class="metric">Avg Interest: {metrics.avg_interest:.1f}</div>
            <div class="metric">Max Interest: {metrics.max_interest:.0f}</div>
            <div class="metric">Volatility: {metrics.volatility:.2f}</div>
            <div class="metric">Momentum: {metrics.momentum:.2f}x</div>
            <div class="metric">Related Queries: {metrics.related_queries_count}</div>
            <div class="metric">Rising Queries: {metrics.rising_queries_count}</div>
            <div class="metric">Breakout Queries: {metrics.breakout_queries_count}</div>
            <div class="metric">Recent Peak: {'Yes' if metrics.recent_peak else 'No'}</div>
        </div>
        """

    def _generate_region_heatmap(self, regions_df: pd.DataFrame, keywords: list[str]) -> str:
        """Generate regional interest heatmap."""

        if len(keywords) == 1:
            keyword = keywords[0]
            if keyword in regions_df.columns:
                df = regions_df[[keyword]].reset_index()
                df.columns = ["region", "interest"]

                fig = px.choropleth(
                    df,
                    locations="region",
                    locationmode="country names",
                    color="interest",
                    hover_name="region",
                    color_continuous_scale="Blues",
                    title=f"Regional Interest: {keyword}",
                )

                fig.update_layout(height=600, template="plotly_white")

                return f'<div class="chart-container">{fig.to_html(include_plotlyjs=False, div_id="region_chart")}</div>'

        return "<p>Regional heatmap unavailable for multi-keyword comparison.</p>"

    def export_csv(
        self,
        keyword: str,
        interest_df: pd.DataFrame,
        regions_df: pd.DataFrame,
        output_dir: Path = config.DATA_DIR,
    ) -> Path:
        """Export data to CSV."""

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = self._generate_timestamp()

        # Interest over time
        interest_file = output_dir / f"{keyword}_{timestamp}_interest.csv"
        interest_df.to_csv(interest_file)

        # Regional interest
        if not regions_df.empty:
            regions_file = output_dir / f"{keyword}_{timestamp}_regions.csv"
            regions_df.to_csv(regions_file)

        logger.info(f"CSV exported: {interest_file}")
        return interest_file

    def export_json(
        self,
        keyword: str,
        metrics: KeywordMetrics,
        output_dir: Path = config.DATA_DIR,
    ) -> Path:
        """Export metrics to JSON."""

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = self._generate_timestamp()
        json_file = output_dir / f"{keyword}_{timestamp}.json"

        import json

        data = {
            "keyword": metrics.keyword,
            "avg_interest": metrics.avg_interest,
            "max_interest": metrics.max_interest,
            "min_interest": metrics.min_interest,
            "volatility": metrics.volatility,
            "momentum": metrics.momentum,
            "breakout_queries": metrics.breakout_queries_count,
            "related_queries": metrics.related_queries_count,
            "rising_queries": metrics.rising_queries_count,
            "recent_peak": metrics.recent_peak,
        }

        with open(json_file, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"JSON exported: {json_file}")
        return json_file
