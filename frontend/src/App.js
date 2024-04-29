import React, { useState, useEffect } from 'react';
import './App.css';
import RecipeList from './RecipeList';
import RecipeDetails from './RecipeDetails';
import SearchBar from './SearchBar';
import AddRecipe from './AddRecipe';

function App() {
    const [recipes, setRecipes] = useState([]);
    const [selectedRecipe, setSelectedRecipe] = useState(null);
    const [showAddRecipeModal, setShowAddRecipeModal] = useState(false);

    useEffect(() => {
        fetch('http://localhost:5000/recipes')
            .then(response => response.json())
            .then(setRecipes);
    }, []);

    const handleSelectRecipe = recipe => {
        setSelectedRecipe(recipe);
    };

    const handleCloseModal = () => {
        setSelectedRecipe(null);
    };

    const handleDeleteRecipe = () => {
        if (selectedRecipe) {
            fetch(`http://localhost:5000/delete_recipe/${selectedRecipe.id}`, {
                method: 'DELETE'
            }).then(response => {
                if (response.ok) {
                    setRecipes(recipes.filter(r => r.id !== selectedRecipe.id));
                    setSelectedRecipe(null);
                } else {
                    alert('Failed to delete recipe');
                }
            });
        }
    };

    const handleAddRecipe = newRecipe => {
        setShowAddRecipeModal(false);
        // Optionally add the recipe to the state if you want to display it immediately
    };

    const toggleAddRecipeModal = () => {
        setShowAddRecipeModal(!showAddRecipeModal);
    };

    return (
        <div>
            <header>
                <h1>Welcome to the Recipe App</h1>
                <button onClick={toggleAddRecipeModal} style={{ marginLeft: '20px' }}>
                    Add Your Own Recipe
                </button>
                <SearchBar onSelectRecipe={handleSelectRecipe} />
            </header>
            <div className="main-content">
                <RecipeList recipes={recipes} onSelectRecipe={handleSelectRecipe} />
            </div>
            {selectedRecipe && <RecipeDetails recipe={selectedRecipe} onClose={handleCloseModal} onDelete={handleDeleteRecipe} />}
            {showAddRecipeModal && <AddRecipe onAddRecipe={handleAddRecipe} onCancel={() => setShowAddRecipeModal(false)} />}
        </div>
    );
}

export default App;
