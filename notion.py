from createPage import createPage
import requests
from app import scrapeRecipe
import os
from dotenv import load_dotenv

load_dotenv()

SCRAPE_NOTION_DB_ID = os.getenv('SCRAPE_NOTION_DB_ID')
RECIPE_NOTION_DB_ID = os.getenv('RECIPE_NOTION_DB_ID')
NOTION_SECRET = os.getenv('NOTION_SECRET')

url = f"https://api.notion.com/v1/databases/{SCRAPE_NOTION_DB_ID}/query"

payload = {"page_size": 100, "filter":             {
                "property": "Scraped",
                "checkbox": {
                    "equals": False
                }
            },}
headers = {
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json",
    "Authorization": f"Bearer {NOTION_SECRET}",
}

response = requests.post(url, json=payload, headers=headers).json()

recipeURL = response['results'][0]['properties']['URL']['title'][0]['text']['content']
scrapedRecipe = scrapeRecipe(recipeURL)
createPage(RECIPE_NOTION_DB_ID, recipeURL, scrapedRecipe)

