"""
Compiles paper/report.md into a standalone, print-ready academic PDF/HTML document.
Uses standard CSS styling aligned with Apart Research & academic workshop submissions.
"""

import os
import re

def markdown_to_html(md_text):
    # Convert headings
    lines = md_text.split('\n')
    html_lines = []
    in_table = False
    table_header = True

    for line in lines:
        # Images
        line = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<div class="figure-container"><img src="\2" alt="\1"><p class="caption">\1</p></div>', line)
        # Bold & Italic
        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
        # Code inline
        line = re.sub(r'`(.*?)`', r'<code>\1</code>', line)

        # Headings
        if line.startswith('# '):
            html_lines.append(f'<h1 class="paper-title">{line[2:]}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('> '):
            html_lines.append(f'<blockquote>{line[2:]}</blockquote>')
        elif line.startswith('---'):
            html_lines.append('<hr>')
        elif line.startswith('|'):
            # Table handling
            if '---' in line:
                continue
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if not in_table:
                html_lines.append('<div class="table-container"><table>')
                in_table = True
                table_header = True

            if table_header:
                th_cells = "".join(f'<th>{c}</th>' for c in cols)
                html_lines.append(f'<thead><tr>{th_cells}</tr></thead><tbody>')
                table_header = False
            else:
                td_cells = "".join(f'<td>{c}</td>' for c in cols)
                html_lines.append(f'<tr>{td_cells}</tr>')
        else:
            if in_table:
                html_lines.append('</tbody></table></div>')
                in_table = False
            if line.strip():
                if line.startswith('* '):
                    html_lines.append(f'<li>{line[2:]}</li>')
                elif line.startswith('1. ') or line.startswith('2. ') or line.startswith('3. '):
                    html_lines.append(f'<li class="ordered">{line[3:]}</li>')
                else:
                    html_lines.append(f'<p>{line}</p>')
            else:
                html_lines.append('')

    if in_table:
        html_lines.append('</tbody></table></div>')

    return "\n".join(html_lines)

def build_report_html():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_md_path = os.path.join(base_dir, "paper", "report.md")
    report_html_path = os.path.join(base_dir, "paper", "report.html")

    with open(report_md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    body_html = markdown_to_html(md_text)

    # Embed SVGs inline so the HTML is 100% self-contained for PDF printing
    fig_dir = os.path.join(base_dir, "figures")
    for fig_name in ["escalation_by_model_stance.svg", "hostile_attribution_rate.svg", "domain_sensitivity.svg"]:
        fig_path = os.path.join(fig_dir, fig_name)
        if os.path.exists(fig_path):
            with open(fig_path, "r", encoding="utf-8") as svg_file:
                svg_content = svg_file.read()
                body_html = body_html.replace(f'src="../figures/{fig_name}"', '')
                body_html = body_html.replace(f'src="/figures/{fig_name}"', '')

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Apart Research Sprint Submission — Dispute Escalation Benchmark</title>
  <style>
    @page {{
      size: A4;
      margin: 20mm 18mm 20mm 18mm;
      @bottom-right {{
        content: counter(page);
      }}
    }}
    body {{
      font-family: "Charter", "Georgia", "Cambria", serif;
      font-size: 10.5pt;
      line-height: 1.55;
      color: #1a1a1a;
      max-width: 820px;
      margin: 0 auto;
      padding: 30px 20px;
    }}
    h1.paper-title {{
      font-size: 19pt;
      line-height: 1.25;
      font-weight: 700;
      text-align: center;
      margin-bottom: 12px;
      letter-spacing: -0.01em;
    }}
    p.meta {{
      text-align: center;
      font-size: 9.5pt;
      color: #555;
      margin-bottom: 24px;
    }}
    h2 {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 13pt;
      font-weight: 700;
      border-bottom: 1px solid #ccc;
      padding-bottom: 4px;
      margin-top: 26px;
      margin-bottom: 10px;
      page-break-after: avoid;
    }}
    h3 {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 11pt;
      font-weight: 600;
      margin-top: 18px;
      margin-bottom: 6px;
      page-break-after: avoid;
    }}
    p {{
      margin-bottom: 10px;
      text-align: justify;
    }}
    blockquote {{
      border-left: 3px solid #2563eb;
      background: #f8fafc;
      padding: 8px 14px;
      margin: 12px 0;
      font-size: 9.5pt;
      font-style: italic;
    }}
    code {{
      font-family: "Consolas", "Courier New", monospace;
      font-size: 9pt;
      background: #f1f5f9;
      padding: 1px 4px;
      border-radius: 3px;
    }}
    .table-container {{
      margin: 16px 0;
      overflow-x: auto;
      page-break-inside: avoid;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 9pt;
    }}
    th, td {{
      padding: 6px 10px;
      border: 1px solid #d1d5db;
      text-align: left;
    }}
    th {{
      background: #f3f4f6;
      font-weight: 600;
    }}
    li {{
      margin-left: 20px;
      margin-bottom: 4px;
    }}
    .figure-container {{
      text-align: center;
      margin: 18px 0;
      page-break-inside: avoid;
    }}
    .figure-container img {{
      max-width: 100%;
      height: auto;
      border: 1px solid #e5e7eb;
      border-radius: 4px;
    }}
    .caption {{
      font-size: 8.5pt;
      color: #666;
      margin-top: 4px;
      font-style: italic;
    }}
    hr {{
      border: 0;
      border-top: 1px solid #e5e7eb;
      margin: 24px 0;
    }}
    @media print {{
      body {{
        padding: 0;
        max-width: 100%;
      }}
      h2 {{
        break-before: auto;
      }}
      .table-container, .figure-container {{
        break-inside: avoid;
      }}
    }}
  </style>
</head>
<body>
{body_html}
</body>
</html>
"""

    with open(report_html_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"Exported print-ready academic paper to: {report_html_path}")

if __name__ == "__main__":
    build_report_html()
