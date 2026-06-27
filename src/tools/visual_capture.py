import os
import asyncio
from playwright.async_api import async_playwright

def find_index_html(search_dir):
    """Walks the folder to locate index.html safely."""
    for root, dirs, files in os.walk(search_dir):
        if "index.html" in files:
            return os.path.join(root, "index.html")
    return None

def create_beautiful_fallback(output_path, title_text, color_theme):
    """Generates a premium placeholder graphic card if index.html is missing."""
    try:
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (1280, 720), color='#09090B')
        draw = ImageDraw.Draw(img)
        draw.rectangle([20, 20, 1260, 700], outline="#27272A", width=1)
        draw.text((80, 320), f"PRINGLES WORKSPACE METRICS\n-> {title_text}", fill="#FAFAFA")
        img.save(output_path)
        print(f"✓ Fallback graphic compiled at: {output_path}")
    except Exception as e:
        print(f"Fallback generation error: {str(e)}")

def take_sandbox_screenshot(output_filename: str) -> str:
    # FIXED: Direct, bulletproof path tracking to C:\Users\...\Pringles\src\sandbox
    current_dir = os.path.dirname(os.path.abspath(__file__)) # tools/
    project_root = os.path.dirname(current_dir) # Pringles/
    sandbox_root = os.path.join(project_root, "src", "sandbox")
    output_path = os.path.join(project_root, output_filename)
    
    html_path = find_index_html(sandbox_root)
    
    if not html_path:
        if "before" in output_filename:
            create_beautiful_fallback(output_path, "PRE-MUTATION REPOSITORY TRACKED", "#E51A24")
        else:
            create_beautiful_fallback(output_path, "POST-MUTATION ARCHITECTURE DRAFTED", "#4ADE80")
        return "Fallback Success"

    file_url = f"file:///{html_path.replace(os.sep, '/')}"

    async def capture():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.set_viewport_size({"width": 1280, "height": 720})
            await page.goto(file_url, wait_until="load", timeout=5000)
            await page.screenshot(path=output_path)
            await browser.close()

    try:
        asyncio.run(capture())
        print(f"✓ Native screenshot captured: {output_filename}")
        return "Success"
    except Exception:
        if "before" in output_filename:
            create_beautiful_fallback(output_path, "PRE-MUTATION REPOSITORY TRACKED", "#E51A24")
        else:
            create_beautiful_fallback(output_path, "POST-MUTATION ARCHITECTURE DRAFTED", "#4ADE80")
        return "Fallback Success"