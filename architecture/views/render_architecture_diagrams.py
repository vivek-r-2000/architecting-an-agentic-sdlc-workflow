"""Render publication-grade architecture diagram PNGs directly from SVG specifications.

Eliminates matplotlib text warping, font collisions, and alignment bugs.
Direct rasterization via Headless Chrome guarantees pixel-perfect fidelity with
the SVG specification at 300 DPI (scale factor 3.0).
"""

from pathlib import Path
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

VIEWS_DIR = Path(r"C:\Users\vivek\ASE\2019112020_AutoSE_A3\architecture\views")


def render_svg_file(svg_filename: str, png_filename: str, width: int, height: int, scale: float = 3.0):
    svg_path = VIEWS_DIR / svg_filename
    png_path = VIEWS_DIR / png_filename
    temp_html = VIEWS_DIR / f"_temp_{svg_filename}.html"

    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()

    # Wrap in HTML to guarantee exact box sizing, font stack, and zero margins
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{
    width: {width}px;
    height: {height}px;
    margin: 0;
    padding: 0;
    background: #ffffff;
    overflow: hidden;
  }}
  svg {{
    width: {width}px;
    height: {height}px;
    display: block;
  }}
</style>
</head>
<body>
{svg_content}
</body>
</html>
"""
    temp_html.write_text(html, encoding="utf-8")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=2000,1600")
    options.add_argument(f"--force-device-scale-factor={scale}")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(temp_html.as_uri())
        svg_element = driver.find_element("tag name", "svg")
        svg_element.screenshot(str(png_path))
    finally:
        driver.quit()
        if temp_html.exists():
            temp_html.unlink()

    with Image.open(png_path) as img:
        print(f"[+] Rendered {svg_filename} -> {png_filename} ({img.width}x{img.height})")


def render_component_view():
    render_svg_file("component_view.svg", "component_view.png", width=1240, height=880, scale=3.0)


def render_sequence_view():
    render_svg_file("sequence_view.svg", "sequence_view.png", width=1150, height=900, scale=3.0)


if __name__ == "__main__":
    print("[*] Starting publication-grade SVG -> PNG rendering...")
    render_component_view()
    render_sequence_view()
    print("[✓] All architecture diagram PNGs rendered successfully!")
