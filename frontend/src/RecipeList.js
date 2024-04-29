import React, { useState, useEffect } from 'react';
import RecipeCard from './RecipeCard';
import RecipeDetails from './RecipeDetails';

function RecipeList() {
    const [recipes, setRecipes] = useState([]);
    const [selectedRecipe, setSelectedRecipe] = useState(null);

    useEffect(() => {
        fetch('http://localhost:5000/recipes')
            .then(response => response.json())
            .then(data => setRecipes(data))
            .catch(error => console.error('Error fetching recipes:', error));
    }, []);

    const handleRecipeClick = recipe => {
        setSelectedRecipe(recipe);
    };

    const handleCloseModal = () => {
        setSelectedRecipe(null);
    };

    return (
        <div>
            {recipes.map(recipe => (
                <RecipeCard key={recipe.id} recipe={recipe} onClick={handleRecipeClick} />
            ))}
            {selectedRecipe && <RecipeDetails recipe={selectedRecipe} onClose={handleCloseModal} />}
        </div>
    );
}

export default RecipeList;