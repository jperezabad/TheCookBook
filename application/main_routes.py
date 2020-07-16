from flask import Blueprint, render_template, request, abort, current_app, redirect, url_for, make_response
from flask_login import login_required, current_user
from application.models.recipe import Recipe
from random import randint, seed
from mongoengine import ValidationError
import pdfkit
import base64
import math
from application.forms import SearchForm

# Blueprint Configuration
main = Blueprint('main', __name__, template_folder="templates", static_folder="static")

MAX_RECIPES_PER_PAGE = 12

@main.route('/')
def home():
    form = SearchForm()
    searchWord = request.args.get('search', "")
    try:
        page = int(request.args.get('page', 1))
        if page < 1: page = 1
    except ValueError: page = 1
    if searchWord == "": count = Recipe.objects().count()
    else: count = Recipe.objects().search_text(searchWord).count()
    maxPage = count/MAX_RECIPES_PER_PAGE
    if maxPage > 0 and page > maxPage: page = math.ceil(maxPage)
    if searchWord == "": recipes = Recipe.objects().order_by("-id").limit(MAX_RECIPES_PER_PAGE).skip(MAX_RECIPES_PER_PAGE*(page-1))
    else: recipes = Recipe.objects().search_text(searchWord).limit(MAX_RECIPES_PER_PAGE).skip(MAX_RECIPES_PER_PAGE*(page-1))
    return render_template('index.html',
        form=form,
        searchWord=searchWord,
        recipes=recipes, 
        count=count,
        maxPage=maxPage,
        page=page, 
        recipes_per_page=MAX_RECIPES_PER_PAGE)

@main.route('/recipe/<recipeID>')
def recipe(recipeID):
    try:
        recipe = Recipe.objects(id=recipeID).first()
    except ValidationError: abort(404)
    if not recipe:
        abort(404)
    return render_template('recipe.html', recipe=recipe)

@main.route('/recipe/<recipeID>/edit')
@login_required
def editRecipe(recipeID):
    recipe = Recipe.objects(id=recipeID).first()
    if not recipe:
        abort(404)
    return render_template('addRecipe.html', recipe=recipe)

@main.route('/addRecipe')
@login_required
def addRecipe():        
    return render_template('addRecipe.html', recipe=None)

@main.route('/user-profile')
@login_required
def userProfile():
    form = SearchForm()
    searchWord = request.args.get('search', "")
    try:
        page = int(request.args.get('page', 1))
        if page < 1: page = 1
    except ValueError: page = 1
    if searchWord == "": count = Recipe.objects(user__id=current_user.id).count()
    else: count = Recipe.objects(user__id=current_user.id).search_text(searchWord).count()
    maxPage = count/MAX_RECIPES_PER_PAGE
    if maxPage > 0 and page > maxPage: page = math.ceil(maxPage)
    if searchWord == "": recipes = Recipe.objects(user__id=current_user.id).order_by("-id").limit(MAX_RECIPES_PER_PAGE).skip(MAX_RECIPES_PER_PAGE*(page-1))
    else: recipes = Recipe.objects(user__id=current_user.id).search_text(searchWord).limit(MAX_RECIPES_PER_PAGE).skip(MAX_RECIPES_PER_PAGE*(page-1))
    return render_template('index.html',
        form=form,
        searchWord=searchWord,
        recipes=recipes, 
        count=count,
        maxPage=maxPage,
        page=page, 
        recipes_per_page=MAX_RECIPES_PER_PAGE)

'''
METHODS TO DOWNLOAD A RECIPE
'''

@main.route('/recipe/<recipeID>/download')
def downloadRecipe(recipeID):
    try:
        recipe = Recipe.objects(id=recipeID).first()
    except ValidationError: abort(404)
    if not recipe:
        abort(404)
    chefIcon = image_file_path_to_base64_string(current_app.root_path + '/static/icon/chef_white.png')
    html = render_template('download.html', recipe=recipe, chefIcon=chefIcon)
    css = ["application/static/css/header.css", "application/static/css/download.css"]
    pdf = pdfkit.from_string(html, False, css=css)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % recipe.title
    return response

def image_file_path_to_base64_string(filepath: str) -> str:
  '''
  Takes a filepath and converts the image saved there to its base64 encoding,
  then decodes that into a string.
  '''
  with open(filepath, 'rb') as f:
    return base64.b64encode(f.read()).decode()
