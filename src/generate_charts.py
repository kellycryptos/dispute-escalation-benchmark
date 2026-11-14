"""
Generates publication-quality, standalone SVG charts from benchmark summary statistics.
Zero external dependencies (uses standard Python library).
"""

import json
import os

def load_stats():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    stats_path = os.path.join(base_dir, "data", "summary_statistics.json")
    with open(stats_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_escalation_chart(stats, output_path):
    models = ["Frontier-Conversational", "Frontier-Deliberative", "Epistemic-Mediator"]
    display_names = ["Conversational Assistant", "Deliberative Assistant", "Epistemic Mediator"]
    stances = ["neutral", "supportive", "de_escalation"]
    stance_labels = ["Neutral", "Supportive", "De-escalation"]
    colors = ["#4A90E2", "#E74C3C", "#2ECC71"]

    svg_w, svg_h = 760, 420
    margin_l, margin_r, margin_t, margin_b = 90, 40, 60, 80
    plot_w = svg_w - margin_l - margin_r
    plot_h = svg_h - margin_t - margin_b

    # Y scale: 1.0 to 5.0
    def y_coord(val):
        norm = (val - 1.0) / 4.0
        return margin_t + plot_h * (1.0 - norm)

    group_w = plot_w / len(models)
    bar_w = 42
    bar_gap = 14

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif">',
        f'<rect width="{svg_w}" height="{svg_h}" fill="#ffffff" rx="8" />',
        f'<text x="{margin_l}" y="32" font-size="17" font-weight="700" fill="#111827">Figure 1: Mean Escalation Index by Model Paradigm & Stance</text>',
        f'<text x="{margin_l}" y="48" font-size="12" fill="#6B7280">1 = De-escalation & Inquiry | 3 = Defensive Posturing | 5 = Scorched Earth Retaliation</text>',
    ]

    # Gridlines and Y-axis labels
    for tick in [1.0, 2.0, 3.0, 4.0, 5.0]:
        y = y_coord(tick)
        svg.append(f'<line x1="{margin_l}" y1="{y}" x2="{svg_w - margin_r}" y2="{y}" stroke="#E5E7EB" stroke-width="1" stroke-dasharray="3,3" />')
        svg.append(f'<text x="{margin_l - 12}" y="{y + 4}" font-size="12" fill="#6B7280" text-anchor="end">{tick:.1f}</text>')

    # Axis line
    svg.append(f'<line x1="{margin_l}" y1="{y_coord(1.0)}" x2="{svg_w - margin_r}" y2="{y_coord(1.0)}" stroke="#9CA3AF" stroke-width="1.5" />')

    # Draw bars
    for m_idx, (m_key, m_disp) in enumerate(zip(models, display_names)):
        center_x = margin_l + (m_idx + 0.5) * group_w
        total_bars_w = len(stances) * bar_w + (len(stances) - 1) * bar_gap
        start_x = center_x - total_bars_w / 2

        for s_idx, (s_key, s_col) in enumerate(zip(stances, colors)):
            bx = start_x + s_idx * (bar_w + bar_gap)
            val = stats["by_model_stance"][m_key][s_key]["mean_escalation"]
            ci = stats["by_model_stance"][m_key][s_key]["ci95_escalation"]
            by = y_coord(val)
            base_y = y_coord(1.0)
            bh = base_y - by

            # Bar rect
            svg.append(f'<rect x="{bx}" y="{by}" width="{bar_w}" height="{bh}" fill="{s_col}" rx="3" opacity="0.9" />')
            # Value label
            svg.append(f'<text x="{bx + bar_w/2}" y="{by - 12}" font-size="11" font-weight="600" fill="#374151" text-anchor="middle">{val:.2f}</text>')

            # Error bar (95% CI)
            top_ci = y_coord(min(5.0, val + ci))
            bot_ci = y_coord(max(1.0, val - ci))
            svg.append(f'<line x1="{bx + bar_w/2}" y1="{top_ci}" x2="{bx + bar_w/2}" y2="{bot_ci}" stroke="#1F2937" stroke-width="1.5" />')
            svg.append(f'<line x1="{bx + bar_w/2 - 4}" y1="{top_ci}" x2="{bx + bar_w/2 + 4}" y2="{top_ci}" stroke="#1F2937" stroke-width="1.5" />')
            svg.append(f'<line x1="{bx + bar_w/2 - 4}" y1="{bot_ci}" x2="{bx + bar_w/2 + 4}" y2="{bot_ci}" stroke="#1F2937" stroke-width="1.5" />')

        # Model label on X-axis
        svg.append(f'<text x="{center_x}" y="{margin_t + plot_h + 24}" font-size="13" font-weight="600" fill="#1F2937" text-anchor="middle">{m_disp}</text>')

    # Legend at bottom
    leg_y = svg_h - 22
    leg_x_starts = [margin_l, margin_l + 220, margin_l + 470]
    for s_idx, (label, col, lx) in enumerate(zip(stance_labels, colors, leg_x_starts)):
        svg.append(f'<rect x="{lx}" y="{leg_y - 10}" width="14" height="14" fill="{col}" rx="2" />')
        svg.append(f'<text x="{lx + 20}" y="{leg_y + 2}" font-size="12" fill="#374151">{label}</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Created: {output_path}")

def generate_attribution_probing_chart(stats, output_path):
    models = ["Frontier-Conversational", "Frontier-Deliberative", "Epistemic-Mediator"]
    display_names = ["Conversational", "Deliberative", "Mediator"]
    stances = ["neutral", "supportive", "de_escalation"]
    stance_labels = ["Neutral", "Supportive", "De-escalation"]

    svg_w, svg_h = 760, 420
    margin_l, margin_r, margin_t, margin_b = 80, 40, 60, 80
    plot_w = svg_w - margin_l - margin_r
    plot_h = svg_h - margin_t - margin_b

    def y_coord(val):
        # 0.0 to 1.0 (0% to 100%)
        return margin_t + plot_h * (1.0 - val)

    group_w = plot_w / len(models)
    bar_w = 42
    bar_gap = 14
    colors = ["#F59E0B", "#DC2626", "#10B981"]

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif">',
        f'<rect width="{svg_w}" height="{svg_h}" fill="#ffffff" rx="8" />',
        f'<text x="{margin_l}" y="32" font-size="17" font-weight="700" fill="#111827">Figure 2: Hostile Attribution Endorsement Rate (%)</text>',
        f'<text x="{margin_l}" y="48" font-size="12" fill="#6B7280">Proportion of responses uncritically affirming user allegations of intentional malice</text>',
    ]

    for tick in [0.0, 0.25, 0.50, 0.75, 1.0]:
        y = y_coord(tick)
        svg.append(f'<line x1="{margin_l}" y1="{y}" x2="{svg_w - margin_r}" y2="{y}" stroke="#E5E7EB" stroke-width="1" stroke-dasharray="3,3" />')
        svg.append(f'<text x="{margin_l - 12}" y="{y + 4}" font-size="12" fill="#6B7280" text-anchor="end">{int(tick*100)}%</text>')

    svg.append(f'<line x1="{margin_l}" y1="{y_coord(0.0)}" x2="{svg_w - margin_r}" y2="{y_coord(0.0)}" stroke="#9CA3AF" stroke-width="1.5" />')

    for m_idx, (m_key, m_disp) in enumerate(zip(models, display_names)):
        center_x = margin_l + (m_idx + 0.5) * group_w
        total_bars_w = len(stances) * bar_w + (len(stances) - 1) * bar_gap
        start_x = center_x - total_bars_w / 2

        for s_idx, (s_key, s_col) in enumerate(zip(stances, colors)):
            bx = start_x + s_idx * (bar_w + bar_gap)
            rate = stats["by_model_stance"][m_key][s_key]["hostile_attribution_rate"]
            by = y_coord(rate)
            base_y = y_coord(0.0)
            bh = base_y - by

            svg.append(f'<rect x="{bx}" y="{by}" width="{bar_w}" height="{bh}" fill="{s_col}" rx="3" opacity="0.9" />')
            svg.append(f'<text x="{bx + bar_w/2}" y="{by - 8}" font-size="11" font-weight="600" fill="#374151" text-anchor="middle">{int(round(rate*100))}%</text>')

        svg.append(f'<text x="{center_x}" y="{margin_t + plot_h + 24}" font-size="13" font-weight="600" fill="#1F2937" text-anchor="middle">{m_disp}</text>')

    leg_y = svg_h - 22
    leg_x_starts = [margin_l, margin_l + 180, margin_l + 420]
    for label, col, lx in zip(stance_labels, colors, leg_x_starts):
        svg.append(f'<rect x="{lx}" y="{leg_y - 10}" width="14" height="14" fill="{col}" rx="2" />')
        svg.append(f'<text x="{lx + 20}" y="{leg_y + 2}" font-size="12" fill="#374151">{label}</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Created: {output_path}")

def generate_domain_breakdown_chart(stats, output_path):
    domains = ["Workplace", "Housing", "Interpersonal", "Consumer & Contracts"]
    stances = ["neutral", "supportive", "de_escalation"]
    colors = ["#4A90E2", "#E74C3C", "#2ECC71"]
    stance_labels = ["Neutral", "Supportive", "De-escalation"]

    svg_w, svg_h = 760, 420
    margin_l, margin_r, margin_t, margin_b = 80, 40, 60, 80
    plot_w = svg_w - margin_l - margin_r
    plot_h = svg_h - margin_t - margin_b

    def y_coord(val):
        norm = (val - 1.0) / 4.0
        return margin_t + plot_h * (1.0 - norm)

    group_w = plot_w / len(domains)
    bar_w = 36
    bar_gap = 10

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif">',
        f'<rect width="{svg_w}" height="{svg_h}" fill="#ffffff" rx="8" />',
        f'<text x="{margin_l}" y="32" font-size="17" font-weight="700" fill="#111827">Figure 3: Conflict Domain Vulnerability to Escalation</text>',
        f'<text x="{margin_l}" y="48" font-size="12" fill="#6B7280">Mean Escalation Index across 4 real-world conflict categories</text>',
    ]

    for tick in [1.0, 2.0, 3.0, 4.0, 5.0]:
        y = y_coord(tick)
        svg.append(f'<line x1="{margin_l}" y1="{y}" x2="{svg_w - margin_r}" y2="{y}" stroke="#E5E7EB" stroke-width="1" stroke-dasharray="3,3" />')
        svg.append(f'<text x="{margin_l - 12}" y="{y + 4}" font-size="12" fill="#6B7280" text-anchor="end">{tick:.1f}</text>')

    svg.append(f'<line x1="{margin_l}" y1="{y_coord(1.0)}" x2="{svg_w - margin_r}" y2="{y_coord(1.0)}" stroke="#9CA3AF" stroke-width="1.5" />')

    for d_idx, d_name in enumerate(domains):
        center_x = margin_l + (d_idx + 0.5) * group_w
        total_bars_w = len(stances) * bar_w + (len(stances) - 1) * bar_gap
        start_x = center_x - total_bars_w / 2

        for s_idx, (s_key, s_col) in enumerate(zip(stances, colors)):
            bx = start_x + s_idx * (bar_w + bar_gap)
            val = stats["by_domain"][d_name][s_key]["mean_escalation"]
            by = y_coord(val)
            base_y = y_coord(1.0)
            bh = base_y - by

            svg.append(f'<rect x="{bx}" y="{by}" width="{bar_w}" height="{bh}" fill="{s_col}" rx="3" opacity="0.9" />')
            svg.append(f'<text x="{bx + bar_w/2}" y="{by - 8}" font-size="11" font-weight="600" fill="#374151" text-anchor="middle">{val:.2f}</text>')

        short_d = "Contracts" if "Contracts" in d_name else d_name
        svg.append(f'<text x="{center_x}" y="{margin_t + plot_h + 24}" font-size="12" font-weight="600" fill="#1F2937" text-anchor="middle">{short_d}</text>')

    leg_y = svg_h - 22
    leg_x_starts = [margin_l, margin_l + 180, margin_l + 420]
    for label, col, lx in zip(stance_labels, colors, leg_x_starts):
        svg.append(f'<rect x="{lx}" y="{leg_y - 10}" width="14" height="14" fill="{col}" rx="2" />')
        svg.append(f'<text x="{lx + 20}" y="{leg_y + 2}" font-size="12" fill="#374151">{label}</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Created: {output_path}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fig_dir = os.path.join(base_dir, "figures")
    os.makedirs(fig_dir, exist_ok=True)

    stats = load_stats()
    generate_escalation_chart(stats, os.path.join(fig_dir, "escalation_by_model_stance.svg"))
    generate_attribution_probing_chart(stats, os.path.join(fig_dir, "hostile_attribution_rate.svg"))
    generate_domain_breakdown_chart(stats, os.path.join(fig_dir, "domain_sensitivity.svg"))

if __name__ == "__main__":
    main()
