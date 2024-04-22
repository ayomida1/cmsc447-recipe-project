import React, { useState, useEffect } from 'react';

function RecipeList() {
    const [recipes, setRecipes] = useState([]);

    useEffect(() => {
        fetch('http://localhost:5000/recipes')  // Adjust the URL based on your Flask app's route
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Failed to load recipes:', data.error);
                } else {
                    setRecipes(data);
                }
            })
            .catch(err => {
                console.error('Error fetching recipes:', err);
            });
    }, []);  // Empty dependency array means this effect runs once after the initial render

    return (
        <div>
            <h1>Recipes</h1>
            <div>
                {recipes.length > 0 ? (
                    recipes.map(recipe => (
                        <div key={recipe.id}>
                            <h2>{recipe.name}</h2>
                            <p>Description: {recipe.description}</p>
                            <p>Ingredients: {recipe.ingredients}</p>
                            <p>Instructions: {recipe.instructions}</p>
                            <hr />
                        </div>
                    ))
                ) : (
                    <p>No recipes found.</p>
                )}
            </div>
        </div>
    );
}

export default RecipeList;
