import React, { useState, useEffect } from 'react';
import RecipeCard from './RecipeCard';
import RecipeDetails from './RecipeDetails';

function SavedRecipes({ currentUser, setSelectedRecipe }) {
    const [savedRecipes, setSavedRecipes] = useState([]);
    const [selectedRecipe, setSelectedRecipeLocal] = useState(null);

    useEffect(() => {
        if (currentUser) {
            fetch(`http://localhost:5000/saved_recipes?username=${currentUser}`)
                .then(response => response.json())
                .then(data => setSavedRecipes(data))
                .catch(error => console.error('Error fetching saved recipes:', error));
        }
    }, [currentUser]);

    const handleRecipeClick = recipe => {
        setSelectedRecipeLocal(recipe);
        setSelectedRecipe(recipe); // Update the selected recipe in the parent component
    };

    const handleCloseModal = () => {
        setSelectedRecipeLocal(null);
        setSelectedRecipe(null); // Update the selected recipe in the parent component
    };

    return (
        <div className="recipe-grid">
            {savedRecipes.map(recipe => (
                <RecipeCard key={recipe.id} recipe={recipe} onClick={handleRecipeClick} />
            ))}
            {selectedRecipe && (
                <RecipeDetails 
                    recipe={selectedRecipe} 
                    onClose={handleCloseModal} 
                    currentUser={currentUser}
                    onEdit={() => {}}
                />
            )}
        </div>
    );
}

export default SavedRecipes;
