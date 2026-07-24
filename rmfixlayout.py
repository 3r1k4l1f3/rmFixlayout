import os
import asyncio
import glob
import sys
import time
import threading
from playwright.async_api import async_playwright


while True:
    user_choice = input("Welcome:) When you are ready to scan your current directory, press 'y'. Press 'n' to cancel:\n>").lower().strip()

    if user_choice.lower() == 'y':
        print("Starting the process. This may take awhile. Go grab a coffee or a snack.")
        break
    elif user_choice.lower() == 'n':
        sys.exit()
    else:
        print("Invalid answer!")

async def capture_perfect_pages():

    pages_captured = 0

    html_files = glob.glob("*.html")
    for html_file in html_files:
        print(f"Found target!: {html_file}")
        if not os.path.exists(html_file):
            print("HTML file missing! Check to make sure the target file is in your current directory.")
            return

    file_url = "file://" + os.path.abspath(html_file)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        page = await browser.new_page(
            viewport={"width": 1920, "height": 2560},
            device_scale_factor=1.0
        )
        
        print(f"Opening {html_file}...")
        await page.goto(file_url)
        
        print("Waiting for assets to load...")
        await page.wait_for_timeout(5000)

        page_elements = await page.query_selector_all('body > div:has(.container), body > div:has(img)')
        total_pages = len(page_elements)
        print(f"Found {total_pages} pages! Starting conversion... Sit tight")

        for i, element in enumerate(page_elements):
            output_name = f"book_page_{str(i+1).zfill(3)}.png"
            
            await element.scroll_into_view_if_needed()
            await page.wait_for_timeout(150)
            
            box = await element.bounding_box()
            
            if box and box["height"] > 0 and box["width"] > 0:
                await page.screenshot(
                    path=output_name,
                    clip={
                        "x": max(0, box["x"]),
                        "y": max(0, box["y"]),
                        "width": box["width"],
                        "height": box["height"]
                    }
                )

                pages_captured += 1

                loading = True
                chars = ["/", "-", "\\", "|"]
                end_time = time.time() + 0.5
                spinner_idx = 0

                while time.time() < end_time:
                    sys.stdout.write(f"\rCapturing pages... [Page {pages_captured}] {chars[spinner_idx % len(chars)]}")
                    sys.stdout.flush()
                    spinner_idx += 1
                    time.sleep(0.1)
                    
            else:
                print(f"Warning: Could not get coordinates for page {i+1}")

        await browser.close()
        loading = False
        print("\nFinished! Continue in KCC to make the book an eBook format.")

asyncio.run(capture_perfect_pages())