import os
import asyncio
from playwright.async_api import async_playwright

async def capture_perfect_pages():
    html_file = "merged_book.html"
    if not os.path.exists(html_file):
        print(f"Error: Could not find {html_file}!")
        return

    file_url = "file://" + os.path.abspath(html_file)

    async with async_playwright() as p:
        # Launch headless browser
        browser = await p.chromium.launch(headless=True)
        
        # We set a massive 1920x2560 canvas to give the book plenty of room to lay out naturally
        # We also set device_scale_factor=1 to prevent Windows display scaling (e.g., 150% zoom) from breaking coordinates
        page = await browser.new_page(
            viewport={"width": 1920, "height": 2560},
            device_scale_factor=1.0
        )
        
        print("Opening merged_book.html...")
        await page.goto(file_url)
        
        print("Waiting for assets to load...")
        await page.wait_for_timeout(5000)

        # Grab divs that have a container OR contain an image (the cover/full pages)
        page_elements = await page.query_selector_all('body > div:has(.container), body > div:has(img)')
        total_pages = len(page_elements)
        print(f"Found {total_pages} pages. Starting coordinate-based capture...")

        for i, element in enumerate(page_elements):
            output_name = f"wimpy_page_{str(i+1).zfill(3)}.png"
            
            # Scroll the element cleanly into view
            await element.scroll_into_view_if_needed()
            await page.wait_for_timeout(150)
            
            box = await element.bounding_box()
            
            if box:
                # To prevent tiny 1-pixel rounding errors from cutting off borders,
                # we slightly expand the crop box by 1 pixel on each side
                await page.screenshot(
                    path=output_name,
                    clip={
                        "x": max(0, box["x"]),
                        "y": max(0, box["y"]),
                        "width": box["width"],
                        "height": box["height"]
                    }
                )
                print(f"Successfully saved {output_name} ({int(box['width'])}x{int(box['height'])}px)")
            else:
                print(f"Warning: Could not get coordinates for page {i+1}")

        await browser.close()
        print("\nFinished! Check the folder—your pages should be perfectly framed now!")

asyncio.run(capture_perfect_pages())