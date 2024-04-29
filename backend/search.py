from flask import jsonify
from elasticsearch import Elasticsearch

# Info needs to be updated when switching elasticsearch free trial accounts
client = Elasticsearch(
  "https://12685a2fc8ff47f68a1300c263fe4f09.us-east4.gcp.elastic-cloud.com:443",
  api_key = "X3hnVTVvNEJDUExWbDNlOGxaM3k6a21ORmNLZ2JTcDJUcmVSTDNhU3Nrdw=="
 )

# Performs search function. Takes in the search query and returns a list
# of recipe ids found by elasticsearch.
def searchRecipes(query):
    # Define Elasticsearch query
    search = {
        "query": {
            "match": {
                "name": query
            }
        }
    }
    
    # Perform search
    results = client.search(index = 'recipes', body = search)
    
    # Extract and return matching recipe ids
    matches = [hit['_id'] for hit in results['hits']['hits']]
    return matches

# Put a new recipe into the index, must be done for every new recipe added
# to the database for elasticsearch to be able to find it.
# Takes in ID and Name of the recipe
def indexRecipe(recipeID, recipeName):
    body = {
        "name": recipeName
    }
    client.index(index = "recipes", id = recipeID, body = body)
    
# Removes a recipe from the index, Must be done with every recipe thats
# taken out of the database. Takes in ID of recipe to be removed
def removeRecipe(recipeID):
    client.delete(index = "recipes", id = recipeID)
