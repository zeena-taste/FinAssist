from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import re

def search_internet(params: dict) -> dict:
    """Search the internet for real-time data, and actively scrape the top webpage for deep numerical comparison logic."""
    query = params.get("query", "")
    print(f"[SEARCH TOOL] Querying internet for: {query}")
    try:
        results = ""
        top_url = None
        
        with DDGS() as ddgs:
            # fetch top 3 generic snippet results
            for idx, r in enumerate(ddgs.text(query, max_results=3)):
                href = r.get('href', '')
                if idx == 0 and href:
                     top_url = href
                results += f"- {r.get('title')}: {r.get('body')} | Source: {href}\n"
                
        if not results:
            return {"status": "success", "result": "No relevant info found online."}

        # Sub-Tool: Deep Web Scraper for real mathematical extraction
        if top_url:
             try:
                 print(f"[SEARCH TOOL] Deep Scraping top URL natively: {top_url}")
                 # Impersonate a standard Windows browser implicitly bypassing standard 403 Firewalls dynamically
                 headers = {
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                 }
                 resp = requests.get(top_url, headers=headers, timeout=8)
                 
                 if resp.status_code == 200:
                      soup = BeautifulSoup(resp.text, "html.parser")
                      
                      # Prune unnecessary layout chunks seamlessly optimizing tokens naturally
                      for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
                           script.extract()
                      
                      text = soup.get_text(separator=' ')
                      clean_text = re.sub(r'\s+', ' ', text).strip()
                      
                      # Inject up to 2000 chars of pure readable text locally giving the AI deep context
                      if len(clean_text) > 50:
                           results += f"\n\n--- DEEP PAGE SCRAPE OF TOP RESULT ({top_url}) ---\n"
                           results += clean_text[:2000] + "... [TRUNCATED FOR TOKEN LIMIT]"
                           
             except Exception as e:
                 print(f"[SEARCH TOOL] Deep crawl failed silently (Bot block or timeout): {e}")
                 # Fails gracefully by falling back to the generic DuckDuckGo snippet payloads securely
            
        return {"status": "success", "result": results}
        
    except Exception as e:
        return {"status": "error", "message": f"Web search systemic failure: {str(e)}"}
