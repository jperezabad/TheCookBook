from flask import Blueprint, Response, request, json
from application.models.recipe import Recipe
from .error import Error

# Blueprint Configuration
api = Blueprint('recipes', __name__, url_prefix='/api/v1')

#############
## RECIPES ##
#############

@api.route('/recipes', methods=['GET', 'POST', 'PUT', 'DELETE'])
def recipes():
    
    data = request.json

    try:
    
        if request.method == "GET":
            
            recipe = Recipe.objects().to_json()

            return Response(recipe, mimetype='application/json', status=200)
        
        elif request.method == "POST":

            recipe = Recipe.create(data)

            return Response(recipe.to_json(), mimetype='application/json', status=200)
            
        elif request.method == "PUT":
                
            recipe = Recipe.update(data)

            return Response(recipe.to_json(), mimetype='application/json', status=200)
        
        elif request.method == "DELETE":

            Recipe.delete(data)

            response = {"Result" : "Recipe deleted"}

            return Response(json.dumps(response), mimetype='application/json', status=200)
        
    except Error as e: return error(str(e))

@api.route("/recipes/<recipeID>")
def recipesByID(recipeID):

    try:

        recipe = Recipe.objects(id=recipeID).first()

        return Response(recipe.to_json(), mimetype='application/json', status=200)
    
    except Error as e: return error(str(e))

###########
## ERROR ##
###########

def error(message):
    response = {'Error': message }
    return Response(json.dumps(response), mimetype='application/json', status=400)