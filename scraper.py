import re
import asyncio
# import requests
# from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

base_url = "http://barttorvik.com/"

async def bpm_collect():
    async with async_playwright() as p:
        #launching browser
        browser = await p.webkit.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        #goes to specific barttorvik page (2025 player data)
        url = base_url + "playerstat.php?link=y&year=2025&start=20241101&end=20250501"
        await page.goto(url)

        #scrapes rows
        #await page.wait_for_selector('table.sortable', state='attached')
        await page.locator('#tble table').wait_for()
        rows = page.locator('#tble table tbody tr')

        players = []
        row_count = await rows.count()
        for i in range(row_count):
            row = rows.nth(i)
            cells = row.locator('td')

            p_data = {'name': await cells.nth(3).inner_text(),
                      'team': await cells.nth(4).inner_text(),
                      'bpm': await cells.nth(8).inner_text()}

            players.append(p_data)

        #sorts players in descending order of bpm
        players_sorted = sorted(players, key=lambda x:x['bpm'], reverse=True)

        top_3 = players_sorted[:3]

        print("Top 3 Players by BPM, 2025:")
        for player in top_3:
            print(f"Name: {player['name']}, Team: {player['team']}, BPM: {player['bpm']}")

        await browser.close()

asyncio.run(bpm_collect())