import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent
HTML_PATH = BASE_DIR / "manual.html"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_PATH = OUTPUT_DIR / "Apex_Team_Manual.pdf"

async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    # Remove o PDF existente antes de gerar o novo, garantindo que o arquivo
    # final sempre substitua qualquer versão anterior na pasta outputs.
    if OUTPUT_PATH.exists():
        OUTPUT_PATH.unlink()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(HTML_PATH.as_uri())
        await page.wait_for_timeout(400)
        await page.pdf(
            path=str(OUTPUT_PATH),
            width="1123px",
            height="794px",
            print_background=True,
            margin={"top":"0","bottom":"0","left":"0","right":"0"},
        )
        await browser.close()
        print(f"PDF written -> {OUTPUT_PATH}")

asyncio.run(main())
