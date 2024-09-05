import requests
from bs4 import BeautifulSoup
from googlesearch import search

async def search_google(query: str):
    print("# [search_google.py] [search_google] Searching Google...")

    async def get_page_info(url):
        print(f"# [search_google.py] [get_page_info] Getting Page Info for {url}...")
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = soup.title.string if soup.title else "No title found"
            description = soup.find('meta', attrs={'name': 'description'})
            description = description['content'] if description else "No description found"
            
            return title, description
        except Exception as e:
            print(f"# [search_google.py] [get_page_info] Error fetching {url}: {str(e)}")
            return "Error fetching page", str(e)

    async def format_search_results(query, num_results=5):
        print("# [search_google.py] [format_search_results] Formatting Search Results...")
        formatted_results = []
        
        for url in search(query, num_results=num_results):
            title, description = await get_page_info(url)
            website_name = url.split('//')[1].split('/')[0]
            
            formatted_result = f"""
    Title: {title}
    From: {website_name}
    URL: {url}
    Description: {description[:150]}...
    """
            formatted_results.append(formatted_result)
        
        return formatted_results
    
    results = await format_search_results(query)
    return_message = "\n".join(results)
    print(f"# [search_google.py] [search_google] Google Search Complete, Returning {len(results)} Results")
    return return_message