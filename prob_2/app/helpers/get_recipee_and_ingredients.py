from sqlalchemy.orm import Session
from app.db.models.recipes import Recipe as RecipeModel
from app.db.models.ingredients import Ingredient as IngredientModel
import uuid

def generate_markdown_recipes(user_id: uuid.UUID, db: Session) -> str:
    recipes = db.query(RecipeModel).filter(RecipeModel.user_id == user_id).all()

    ingredients = db.query(IngredientModel).filter(IngredientModel.user_id == user_id).all()
    markdown_content = ""
    
    if recipes:
        markdown_content += "# Recipes\n\n"
        for idx, recipe in enumerate(recipes, start=1):
            markdown_content += f"### {idx}. {recipe.recipe_name}\n"
            markdown_content += f"{recipe.recipe_text if recipe.recipe_text else 'No details provided.'}\n\n"
    else:
        markdown_content += "No recipes found for this user.\n\n"
    
    return markdown_content

def generate_markdown_ingredients(user_id: uuid.UUID, db: Session) -> str:
    ingredients = db.query(IngredientModel).filter(IngredientModel.user_id == user_id).all()
    markdown_content = ""
    
    if ingredients:
        markdown_content += "# Ingredients\n\n"
        for idx, ingredient in enumerate(ingredients, start=1):
            markdown_content += f"### {idx}. {ingredient.ingredient_name}\n"
            markdown_content += f"- Description: {ingredient.ingredient_description if ingredient.ingredient_description else 'No details provided.'}\n"
            markdown_content += f"- Quantity: {ingredient.ingredient_quantity}\n\n"
    else:
        markdown_content += "No ingredients found for this user.\n\n"

    return markdown_content


