#!/usr/bin/env python3
"""
Inlines styles.css into Index.html and every blog/*/index.html page.
Run this any time styles.css is edited, before deploying.

Usage: python3 inline-css.py
"""
import re
import glob
import os

ROOT = os.path.dirname(os.path.abspath(__file__))


def inline_into(html_path, css):
    with open(html_path, encoding="utf-8") as f:
        content = f.read()

    new_style_block = f"<style>\n{css}\n  </style>"

    # Replace whatever <style>...</style> block currently exists (the previously
    # inlined CSS) with the freshly read styles.css content.
    pattern = re.compile(r"<style>.*?</style>", re.S)
    if pattern.search(content):
        content, n = pattern.subn(new_style_block, content, count=1)
    else:
        raise RuntimeError(f"No <style> block found in {html_path} to replace")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  inlined into {html_path} ({len(content)} bytes)")


def main():
    css_path = os.path.join(ROOT, "styles.css")
    with open(css_path, encoding="utf-8") as f:
        css = f.read()

    inline_into(os.path.join(ROOT, "Index.html"), css)
    for blog_html in glob.glob(os.path.join(ROOT, "blog", "*", "index.html")):
        inline_into(blog_html, css)

    print("Done. All pages now contain the latest styles.css inline.")


if __name__ == "__main__":
    main()
