from app import scrapeRecipe

recipeURL = 'https://www.pickuplimes.com/recipe/fluffy-vegan-pancakes-841'
scrapedRecipe = scrapeRecipe(recipeURL)
print(scrapedRecipe)

