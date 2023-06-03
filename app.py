import os
from dotenv import load_dotenv
import requests
import bs4
import re

load_dotenv()

SPOONACULAR_SECRET = os.getenv('SPOONACULAR_SECRET')

def scrapeController(url):
    if "rainbowplantlife" in url:
        print(url)
        return scrapeRPLRecipe(url)
    else:
        return scrapeRecipe(url)

def scrapeRecipe(url):
    params = {
        "apiKey": SPOONACULAR_SECRET,
        "url": url
    }
    spoonacularExtractURL = "https://api.spoonacular.com/recipes/extract"
    recipe = requests.get(spoonacularExtractURL, params=params).json()
    ingredientsArray = parseIngredients(recipe["extendedIngredients"])
    instructionsArray = parseInstructions(recipe["analyzedInstructions"], recipe["instructions"])
    return { "title": recipe["title"], "ingredients": ingredientsArray, "instructions": instructionsArray, "image": recipe["image"], "author": recipe["sourceName"] }

def parseIngredients(ingredients):
    obj = {"heading": ''}
    obj["ingredients"] = []
    for el in ingredients:
        ingredient = el["originalName"]
        obj["ingredients"].append(ingredient)
    return [obj]

def parseInstructions(instructions, instructionString):
    if not instructions:
        return [instructionString]
    parsedInstructions = []
    for el in instructions[0]["steps"]:
        instruction = el["step"]
        parsedInstructions.append(instruction)
    return parsedInstructions

def scrapeRPLRecipe(url):
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    recipes = soup.find_all("div", class_="wprm-recipe-container")
    ingredientsGroup = recipes[0].find_all("div", class_="wprm-recipe-ingredient-group")
    instructionsGroup = recipes[0].find_all("div", class_="wprm-recipe-instruction-group")
    title = soup.find("h1", class_="entry-title")
    image_div = soup.find('div', class_='entry-image')['style']
    rawImageURL = re.search("http.*[)]",image_div)
    cleanedImageURL = image_div[rawImageURL.start():rawImageURL.end()-1]
    print(cleanedImageURL)
    ingredientsArray = []

    for i in ingredientsGroup:
        heading = i.find("h4", "wprm-recipe-group-name")
        ingredientsArray.append(parseRPLIngredients(i, heading))
    
    # assume only 1 set of instructions
    instructionsArray = parseRPLInstructions(instructionsGroup[0])

    return { "title": title.text, "ingredients": ingredientsArray, "instructions": instructionsArray, "image": cleanedImageURL, "author": "Rainbow Plant Life" }

def getRPLTextContent(el, tag, identifer):
    element = el.find(tag, identifer)
    if element:
        return element.text
    else:
        return ''

def parseRPLIngredients(group, heading):
    if (heading):
        heading = '*' + heading.text + '*'
    else:
        heading = ''
    obj = {
        "heading": heading
    }
    obj["ingredients"] = []
    ingredients = group.find("ul", class_="wprm-recipe-ingredients")
    for el in ingredients:
        ingredient = getRPLTextContent(el, "span","wprm-recipe-ingredient-name")
        amount = getRPLTextContent(el, "span", "wprm-recipe-ingredient-amount")
        unit = getRPLTextContent(el, "span", "wprm-recipe-ingredient-unit")
        string = amount + ' ' + unit + ' ' + ingredient
        obj["ingredients"].append(string)
    return obj

def parseRPLInstructions(group):
    instructions = []
    instructionsSoup = group.find("ul", class_="wprm-recipe-instructions")
    for el in instructionsSoup:
        instruction = el.text
        instructions.append(instruction)
    return instructions