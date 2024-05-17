import React, { useState, useEffect } from 'react';
import RecipeCard from './RecipeCard';
import RecipeDetails from './RecipeDetails';

function RecipeList({ onSelectRecipe, currentUser, onEdit }) {
    const [recipes, setRecipes] = useState([]);
    const [selectedRecipe, setSelectedRecipe] = useState(null);
    const [showAll, setShowAll] = useState(false);

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

    const toggleShowAll = () => {
        setShowAll(!showAll);
    };

    // Determine the number of recipes to display
    const recipesToDisplay = showAll ? recipes : recipes.slice(0, 8); // Adjust 6 to the number of recipes per row

    return (
        <div>
            <div className="recipe-grid">
                {recipesToDisplay.map(recipe => (
                    <RecipeCard key={recipe.id} recipe={recipe} onClick={handleRecipeClick} />
                ))}
                {selectedRecipe && (
                    <RecipeDetails 
                        recipe={selectedRecipe} 
                        onClose={handleCloseModal} 
                        currentUser={currentUser}
                        onEdit={onEdit}
                    />
                )}
            </div>
            {recipes.length > 6 && (
                <div className="show-more-container">
                    <button className="show-more-button" onClick={toggleShowAll}>
                        {showAll ? 'Show Less ▲' : 'Show More ▼'}
                    </button>
                </div>
            )}
        </div>
    );
}

export default RecipeList;
