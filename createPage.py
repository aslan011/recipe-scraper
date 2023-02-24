import requests
import json
from termcolor import colored
import os
from dotenv import load_dotenv

load_dotenv()

NOTION_SECRET = os.getenv('NOTION_SECRET')
def generateChildBlocks(ingredients, instructions):
    print(instructions)
    blocks = []
    blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [
                {
                  "type": "text",
                    "text": {
                        "content": "Shopping List"
                    }
                }
            ]
        }
    },)
    for ingredient in ingredients:
        blocks.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": f"{ingredient['heading'] or 'Main'}"
                        }
                    }
                ]
            }
        })
        for i in ingredient['ingredients']:
            blocks.append(
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"{i}"
                                }
                            }
                        ]
                    }
                })
    blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [
                {
                  "type": "text",
                    "text": {
                        "content": "Instructions"
                    }
                }
            ]
        }
    })
    for instruction in instructions:
        blocks.append({
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": instruction
                        }
                    }
                ]
            }
        },)
    return blocks


def createPage(databaseId, recipeURL, data):
    title = data["title"]
    ingredients = data["ingredients"]
    instructions = data["instructions"]
    url = 'https://api.notion.com/v1'
    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": f"Bearer {NOTION_SECRET}",
    }

    newPageData = {
        "parent": {"database_id": databaseId},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": f"{title}"
                        }
                    }
                ],
            },
        },
    }
    data = json.dumps(newPageData)
    res = requests.post(f"{url}/pages", headers=headers, data=data)
    parsedRes = res.json()
    parentID = parsedRes['id']
    updateText = {
        "children": generateChildBlocks(ingredients, instructions)
    }
    updateData = json.dumps(updateText)
    update = requests.patch(
        f"{url}/blocks/{parentID}/children", headers=headers, data=updateData)

    print(update.json())
