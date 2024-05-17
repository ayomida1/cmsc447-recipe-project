import React, { useState, useEffect } from 'react';
import RecipeCard from './RecipeCard';
import RecipeDetails from './RecipeDetails';

function SavedRecipes({ currentUser, setSelectedRecipe }) {
    const [savedRecipes, setSavedRecipes] = useState([]);
    const [selectedRecipe, setSelectedRecipeState] = useState(null);

    useEffect(() => {
        if (currentUser) {
            fetch(`http://localhost:5000/saved_recipes?username=${currentUser}`)
                .then(response => response.json())
                .then(data => {
                    // Ensure data is an array
                    if (Array.isArray(data)) {
                        setSavedRecipes(data);
                    } else {
                        setSavedRecipes([]);
                    }
                })
                .catch(error => {
                    console.error('Error fetching saved recipes:', error);
                    setSavedRecipes([]);
                });
        } else {
            setSavedRecipes([]);
        }
    }, [currentUser]);

    const handleRecipeClick = (recipe) => {
        setSelectedRecipe(recipe);
        setSelectedRecipeState(recipe);
    };

    const handleCloseModal = () => {
        setSelectedRecipe(null);
        setSelectedRecipeState(null);
    };

    if (!currentUser) {
        return <p>Please log in to view your saved recipes.</p>;
    }

    return (
        <div className="saved-recipes">
            {savedRecipes.length > 0 ? (
                savedRecipes.map(recipe => (
                    <RecipeCard key={recipe.id} recipe={recipe} onClick={() => handleRecipeClick(recipe)} />
                ))
            ) : (
                <p>No saved recipes to display.</p>
            )}
            {selectedRecipe && (
                <RecipeDetails 
                    recipe={selectedRecipe} 
                    onClose={handleCloseModal} 
                    currentUser={currentUser} 
                />
            )}
        </div>
    );
}

export default SavedRecipes;
