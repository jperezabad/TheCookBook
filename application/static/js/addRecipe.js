
const recipesEndpoint = '/api/v1/recipes';

function goHome(){
    window.location.href = "/"
}

function showImage() {
    var image = document.getElementById("image");
    var imageUrl = document.getElementById("imageUrl").value;

    if (imageUrl == "") {
        image.src = "";
        image.style.display = "none";
    } else {
        image.src = imageUrl;
        image.style.display = "block";
    }
}

function showVideo() {
    var video = document.getElementById("video")
    var videoId = document.getElementById("videoId").value;

    if (videoId == "") {
        video.src = "";
        video.style.display = "none";
    } else {
        video.src = "https://www.youtube.com/embed/" + videoId;
        video.style.display = "block";
    }
}

function addTag() {

    var parent = document.getElementById("tags");
    var position = parent.childElementCount + 1;

    var div = document.createElement("div");
    div.className = "horizontal";

    var tag = document.createElement("i");
    tag.className = "fas fa-tag";

    var input = document.createElement("input");
    input.type = "text";
    input.className = "tag"
    input.placeholder = "Tag " + position;

    var close = document.createElement("i");
    close.className = "fas fa-times"
    close.onclick = deleteTag;

    div.appendChild(tag);
    div.appendChild(input);
    div.appendChild(close);

    parent.appendChild(div);
}

function deleteTag() {

    var parent = document.getElementById("tags");
    parent.removeChild(parent.childNodes[parent.childNodes.length-1])
}

function addIngredient() {

    var parent = document.getElementById("ingredients");
    var position = parent.childElementCount + 1;

    var div = document.createElement("div");
    div.className = "horizontal";

    var bread = document.createElement("i");
    bread.className = "fas fa-bread-slice";

    var quantity = document.createElement("input");
    quantity.type = "number";
    quantity.placeholder = "Quantity";
    quantity.className = "quantity";
    quantity.min = 1;

    var measure = document.createElement("input");
    measure.type = "text";
    measure.placeholder = "Measure";
    measure.className ="measure";

    var input = document.createElement("input");
    input.type = "text";
    input.placeholder = "Ingredient " + position;
    input.className = "ingredient"

    var close = document.createElement("i");
    close.className = "fas fa-times"
    close.onclick = deleteIngredient;

    div.appendChild(bread);
    div.appendChild(quantity);
    div.appendChild(measure);
    div.appendChild(input);
    div.appendChild(close);

    parent.appendChild(div);
}

function deleteIngredient() {

    var parent = document.getElementById("ingredients");
    parent.removeChild(parent.childNodes[parent.childNodes.length-1])
}

function addDirection() {

    var parent = document.getElementById("directions");
    var position = parent.childElementCount + 1;

    var div = document.createElement("div");
    div.className = "horizontal";

    var utensils = document.createElement("i");
    utensils.className = "fas fa-utensils";

    var input = document.createElement("input");
    input.type = "text";
    input.placeholder = "Step " + position;
    input.className = "direction"

    var close = document.createElement("i");
    close.className = "fas fa-times"
    close.onclick = deleteDirection;

    div.appendChild(utensils);
    div.appendChild(input);
    div.appendChild(close);

    parent.appendChild(div);
}

function deleteDirection() {

    var parent = document.getElementById("directions");
    parent.removeChild(parent.childNodes[parent.childNodes.length-1])
}

function addInfo() {

    var parent = document.getElementById("infos");

    var div = document.createElement("div");
    div.className = "horizontal";

    var icon = document.createElement("i");
    icon.className = "fas fa-info";

    var input = document.createElement("input");
    input.type = "text";
    input.placeholder = "Additional information";
    input.className = "info"

    var close = document.createElement("i");
    close.className = "fas fa-times"
    close.onclick = deleteInfo;

    div.appendChild(icon);
    div.appendChild(input);
    div.appendChild(close);

    parent.appendChild(div);
}

function deleteInfo() {

    var parent = document.getElementById("infos");
    parent.removeChild(parent.childNodes[parent.childNodes.length-1])
}

function submitRecipe(recipeID) {

    var recipe = {};

    recipe.id = recipeID;
    recipe.title = document.getElementById("recipeName").value;
    recipe.time = document.getElementById("recipeTime").value;
    recipe.people = document.getElementById("recipePeople").value;

    if (recipe.title == "" || recipe.time == "" || recipe.people == "") {
        alert("Please fill in the mandatory fields");
        return;
    }
    
    recipe.video = document.getElementById("videoId").value;
    var imageUrl = document.getElementById("imageUrl").value;
    if (imageUrl != "") {
        recipe.image = imageUrl;
    } else if (document.getElementById("image").style.display == 'block') {
        recipe.imageBase64 = prepareImage();
    }

    recipe.tags = [];
    var tagsElements = document.getElementById("tags").children;
    for (var i = 0; i < tagsElements.length; i++) {
        var name = document.querySelectorAll("#tags .tag")[i].value;
        if (name != "") {
            recipe.tags.push(name);
        }
    }
    
    recipe.ingredients = [];
    var ingredients = document.getElementById("ingredients").children;
    if (ingredients.length < 1) {
        alert("Please introduce at least one ingredient");
        return;
    }
    for (var i = 0; i < ingredients.length; i++) {
        var ingredient = {};
        ingredient.name = document.querySelectorAll("#ingredients .ingredient")[i].value;
        ingredient.quantity = document.querySelectorAll("#ingredients .quantity")[i].value;
        ingredient.measure = document.querySelectorAll("#ingredients .measure")[i].value;
        if (ingredient.name != "") {
            if (ingredient.quantity == "") ingredient.quantity = null;
            if (ingredient.measure == "") ingredient.measure = null;
            recipe.ingredients.push(ingredient);
        }
        
    }

    recipe.steps = [];
    var stepsElements = document.getElementById("directions").children;
    if (stepsElements.length < 1) {
        alert("Please introduce at least one step");
        return;
    }
    for (var i = 0; i < stepsElements.length; i++) {
        var step = document.querySelectorAll("#directions .direction")[i].value;
        if (step != "") {
            recipe.steps.push(step);
        }       
    }

    recipe.info = []
    var infoElements = document.getElementById("infos").children;
    for (var i = 0; i < infoElements.length; i++) {
        var info = document.querySelectorAll("#infos .info")[i].value;
        if (info != "") {
            recipe.info.push(info);
        }       
    }

    var request = new XMLHttpRequest();
    if (recipeID == '') {
        request.open("POST", recipesEndpoint);
    } else {
        request.open("PUT", recipesEndpoint);
    }
    request.setRequestHeader("Content-Type", "application/json");

    request.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE) {
            if (this.status == 200) {
                if (recipeID == '') {
                    window.location.href = "/";
                } else {
                    window.location.href = "/recipe/" + recipeID;
                }
            } else {
                alert('ERROR: status code: ' + request.status);
            }
        }
    }

    request.send( JSON.stringify(recipe) );
}