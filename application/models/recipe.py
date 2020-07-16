from mongoengine import *
import datetime
from application.api.error import Error
from application.utils import imgur as Imgur
from flask_login import current_user

class User(EmbeddedDocument):
    id = ObjectIdField(required=True)
    name = StringField(max_length=200, required=True)

class Ingredient(EmbeddedDocument):
    name = StringField(required=True)
    quantity = IntField()
    measure = StringField()

class Recipe(Document):
    title = StringField(max_length=200, required=True)
    people = IntField(min_value=1, required=True)
    time = IntField(min_value=1, required=True)
    image = URLField()
    video = StringField()
    tags = ListField(StringField())
    ingredients = ListField(EmbeddedDocumentField(Ingredient))
    steps = ListField(StringField())
    info = ListField(StringField())
    date = DateTimeField(default=datetime.datetime.utcnow)
    user = EmbeddedDocumentField(User)

    meta = {'indexes': [
        {'fields': ['$title'],
         'default_language': 'spanish' }
    ]}

    @staticmethod
    def create(data):

        if 'title' not in data or data['title'] == "": raise Error('Missing recipe title')
        if 'people' not in data or data['people'] == "": raise Error('Missing number of people')
        if 'time' not in data or data['time'] == "": raise Error('Missing recipe time')

        if 'image' not in data or data['image'] == "": data['image'] = None
        if 'imageBase64' not in data or data['imageBase64'] == "": data['imageBase64'] = None
        if 'video' not in data or data['video'] == "": data['video'] = None

        recipe = Recipe()
        recipe.title = data['title']
        recipe.people = data['people']
        recipe.time = data['time']
        if data['imageBase64'] != None: recipe.image = Imgur.uploadBase64(data['imageBase64'])
        if data['image'] != None: recipe.image = Imgur.uploadImage(data['image'])   
        if recipe.image is None: recipe.image = "https://i.imgur.com/qB1e5X4.png"
        recipe.video = data['video']
        recipe.tags = [ tag.lower() for tag in data['tags'] ] 
        recipe.steps = data['steps']
        for ingredientDict in data['ingredients']:
            ingredient = Ingredient()
            ingredient.name = ingredientDict['name'].lower()
            ingredient.quantity = ingredientDict['quantity']
            ingredient.measure = ingredientDict['measure']
            recipe.ingredients.append(ingredient)
        recipe.info = [ info for info in data['info'] ]
        user = User()
        user.name = current_user.username
        user.id = current_user.id
        recipe.user = user

        try:
            recipe.save()
            return recipe
        except ValidationError as e: raise Error('Validation error %s', e)

    @staticmethod
    def update(data):

        if 'id' not in data or data['id'] is None or data['id'] == "": raise Error('Missing recipe id')

        recipe = Recipe.objects(id=data['id']).first()

        if 'title' not in data or data['title'] == "": raise Error('Missing recipe title')
        if 'people' not in data or data['people'] == "": raise Error('Missing number of people')
        if 'time' not in data or data['time'] == "": raise Error('Missing recipe time')
        
        if 'video' not in data or data['video'] == "": data['video'] = None
        if 'image' not in data or data['image'] == "": data['image'] = None

        recipe.title = data['title']
        recipe.people = data['people']
        recipe.time = data['time']
        if 'imageBase64' in data: recipe.image = Imgur.uploadBase64(data['imageBase64'])
        if data['image'] != None and data['image'] != recipe.image: recipe.image = Imgur.uploadImage(data['image']) 
        recipe.video = data['video']
        recipe.tags = [ tag.lower() for tag in data['tags'] ] 
        recipe.steps = data['steps']
        recipe.ingredients = []
        for ingredientDict in data['ingredients']:
            ingredient = Ingredient()
            ingredient.name = ingredientDict['name']
            ingredient.quantity = ingredientDict['quantity']
            ingredient.measure = ingredientDict['measure']
            recipe.ingredients.append(ingredient)
        recipe.info = [ info for info in data['info'] ]

        try:
            recipe.save()
            return recipe
        except ValidationError as e: 
            print(str(e))
            raise Error('Validation error')

    @staticmethod
    def delete(data):
        
        if 'id' not in data or data['id'] is None or data['id'] == "": raise Error('Missing recipe id')

        recipe = Recipe.objects(id=data['id'])

        recipe.delete()


if __name__ == "__main__":

    connect('cookbook', username='root', password='admin', authentication_source='admin')

    for recipe in Recipe.objects(): print(recipe.to_json()) 

    recipe = Recipe(title="Risotto",people="4",time="60",tags=["Arroz", "almuerzo", "italiano"])
    recipe.save()
    print(recipe.id)
    for recipe in Recipe.objects(): print(recipe.to_json()) 
