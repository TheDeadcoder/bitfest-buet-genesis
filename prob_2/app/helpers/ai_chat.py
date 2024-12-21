from app.core.openai import openaiClient

def generate_recipe_completion(query: str, available_recipes: str, available_ingredients: str) -> str:
    try:
        system_prompt = f"""
        You are a helpful AI assistant that helps users with their cooking needs. 
        A user has asked asked a query or his cooking needs or tastes.
        A user have some recipes and ingredients available.
        You need to generate a response based on the user query, available recipes and ingredients.
        You MUST not answer a recipe whose necessary ingredients are not available.
        If no recipe cannot be answered, you can suggest a recipe based on the user query. But it MUST be prepared with the available ingredients.
        """
        human_prompt = f"""
        User Query: {query}
        Available Recipes: {available_recipes}
        Available Ingredients: {available_ingredients}
        """

        print(available_recipes)
        print(available_ingredients)
        response = openaiClient.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": human_prompt}
            ],
            max_tokens=1500,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating recipe completion: {e}")
        return "Error generating recipe completion"  