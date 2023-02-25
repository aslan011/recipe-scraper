import requests
import bs4
import re

def scrapeRecipe(url):
    page = requests.get(url)
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
        ingredientsArray.append(parseIngredients(i, heading))
    
    # assume only 1 set of instructions
    instructionsArray = parseInstructions(instructionsGroup[0])

    return { "title": title.text, "ingredients": ingredientsArray, "instructions": instructionsArray, "image": cleanedImageURL }

def getTextContent(el, tag, identifer):
    element = el.find(tag, identifer)
    if element:
        return element.text
    else:
        return ''

def parseIngredients(group, heading):
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
        ingredient = getTextContent(el, "span","wprm-recipe-ingredient-name")
        amount = getTextContent(el, "span", "wprm-recipe-ingredient-amount")
        unit = getTextContent(el, "span", "wprm-recipe-ingredient-unit")
        string = amount + ' ' + unit + ' ' + ingredient
        obj["ingredients"].append(string)
    return obj

def parseInstructions(group):
    instructions = []
    instructionsSoup = group.find("ul", class_="wprm-recipe-instructions")
    for el in instructionsSoup:
        instruction = el.text
        instructions.append(instruction)
    return instructions