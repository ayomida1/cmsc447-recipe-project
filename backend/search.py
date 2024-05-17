from flask import jsonify
from elasticsearch import Elasticsearch

# Info needs to be updated when switching elasticsearch free trial accounts
client = Elasticsearch(
  "https://f8b079afb3584f8b897309ce8d32200e.us-east4.gcp.elastic-cloud.com:443",
  api_key = "R3FQemg0OEJtX0FuOXNfOGZqZmk6UG5mWWMzWFVTNGVFSmsxOGV0SjlUZw=="
 )

# Performs search function. Takes in the search query and returns a list
# of recipe ids found by elasticsearch.
def searchRecipes(query):
    # Define Elasticsearch query
    search = {
        "query": {
            "bool": {
                "should": [
                    {   
                        "prefix": {
                            "name": {
                                "value": query,
                                "case_insensitive": True
                            }
                        }
                    },
                    {
                        "prefix": {
                            "tags": {
                                "value": query,
                                "case_insensitive": True
                            }
                        }
                    }
                ]
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
def indexRecipe(recipeID, recipeName, tags):
    body = {
        "name": recipeName,
        "tags": tags
    }
    client.index(index = "recipes", id = recipeID, body = body)
    
# Removes a recipe from the index, Must be done with every recipe thats
# taken out of the database. Takes in ID of recipe to be removed
def removeRecipe(recipeID):
    client.delete(index = "recipes", id = recipeID)

# Removes every recipe currently inside the index by deleting the index
# A new index gets made when a new recipe is inserted
def clearIndex():
    client.client.indices.delete(index = "recipes")