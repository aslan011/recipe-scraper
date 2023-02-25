from createPage import createPage
import requests
from app import scrapeRecipe
import os
from dotenv import load_dotenv
import json

load_dotenv()

SCRAPE_NOTION_DB_ID = os.getenv('SCRAPE_NOTION_DB_ID')
RECIPE_NOTION_DB_ID = os.getenv('RECIPE_NOTION_DB_ID')
NOTION_SECRET = os.getenv('NOTION_SECRET')

url = f"https://api.notion.com/v1/databases/{SCRAPE_NOTION_DB_ID}/query"

payload = {"page_size": 100, "filter": {
    "property": "Scraped",
                "checkbox": {
                    "equals": False
                }
},
    "sorts": [
    {
        "timestamp": "last_edited_time",
        "direction": "descending"
    }
]
}
headers = {
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json",
    "Authorization": f"Bearer {NOTION_SECRET}",
}

response = requests.post(url, json=payload, headers=headers).json()

recipeURL = response['results'][0]['properties']['URL']['title'][0]['text']['content']
pageID = response['results'][0]["id"]
scrapedRecipe = scrapeRecipe(recipeURL)
createPage(RECIPE_NOTION_DB_ID, recipeURL, scrapedRecipe)

updateScrapedURL = f'https://api.notion.com/v1/pages/{pageID}'
headers = {
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json",
    "Authorization": f"Bearer {NOTION_SECRET}",
}

newPageData = {
    "properties": {
        "Scraped": {"checkbox": True}
    }
}
data = json.dumps(newPageData)
res = requests.patch(updateScrapedURL, headers=headers, data=data)
