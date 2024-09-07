import aiohttp
from bs4 import BeautifulSoup

async def get_page_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                return soup.get_text()
            else:
                return f"Failed to retrieve the page. Status code: {response.status}"