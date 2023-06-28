from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Recipe(BaseModel):
    name: str
    prep_time: int
    cook_time: int
    ingredients: dict


class UpdateRecipe(BaseModel):
    name: Optional[str] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    ingredients: Optional[dict] = None


recipes = {}


@app.get("/get-recipe/{recipe_id}")
def get_recipe(recipe_id: int = Path(None, description="The id of the recipe you would like to view", gt=0)):
    return recipes[recipe_id]


@app.get("/get-recipe-by-name")
def get_recipe(name: Optional[str] = None):
    for recipe_id in recipes:
        if recipes[recipe_id].name == name:
            return recipes[recipe_id]
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe name not found.")


@app.post("/create-recipe/{recipe_id}")
def create_recipe(recipe_id: int, recipe: Recipe):
    if recipe_id in recipes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe id already exists.")

    recipes[recipe_id] = recipe
    return recipes[recipe_id]


@app.put("/update-recipe/{recipe_id}")
def update_recipe(recipe_id: int, recipe: UpdateRecipe):
    if recipe_id not in recipes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe id does not already exist.")

    if recipe.name is not None:
        recipes[recipe_id].name = recipe.name

    if recipe.prep_time is not None:
        recipes[recipe_id].prep_time = recipe.prep_time

    if recipe.cook_time is not None:
        recipes[recipe_id].cook_time = recipe.cook_time

    if recipe.ingredients is not None:
        recipes[recipe_id].ingredients = recipe.ingredients

    return recipes[recipe_id]


@app.delete("/delete-recipe")
def delete_recipe(recipe_id: int = Query(..., description="The id of the recipe to delete")):
    if recipe_id not in recipes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    del recipes[recipe_id]
    return {"Success": "Recipe deleted."}
