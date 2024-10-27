#!/usr/bin/python3
""" Convert Markdown file to HTML file. """
import sys
import os
import re
import hashlib


def markdown_to_html(markdown_f, output_f):
    """Convert Markdown file to HTML file."""
    if not os.path.exists(markdown_f):
        print(f"Missing {markdown_f}", file=sys.stderr)
        sys.exit(1)

    with open(markdown_f, "r") as f:
        lines = f.readlines()

    html_lines = []
    for line in lines:
        line = line.strip()
        line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
        line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
        line = re.sub(r'\[\[(.*?)\]\]', lambda x:
                      hashlib.md5(x.group(1).encode()).hexdigest(), line)
        line = re.sub(r'\(\((.*?)\)\)', lambda x:
                      x.group(1).replace('c', '').replace('C', ''), line)

        if line.startswith('#'):
            heading_lvl = min(6, line.count('#'))
            heading_txt = line.strip('#').strip()
            html_lines.append(f"<h{heading_lvl}>{heading_txt}</h{heading_lvl}>")

        elif line.startswith('-'):
            html_lines.append("<ul>")
            html_lines.append(f"<li>{line.strip('-').strip()}</li>")
            html_lines.append("</ul>")

        elif line:
            html_lines.append(f"<p>{line}</p>")

    with open(output_f, 'w') as f:
        f.write('\n'.join(html_lines))


def main():
    """Main function to parse command line args and convert Markdown to HTML"""
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>",
              file=sys.stderr)
        sys.exit(1)

    markdown_f = sys.argv[1]
    output_f = sys.argv[2]

    markdown_to_html(markdown_f, output_f)
    sys.exit(0)


if __name__ == "__main__":
    main()
