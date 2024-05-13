import React, { useState, useEffect } from 'react';
import './App.css';
import RecipeList from './RecipeList';
import RecipeDetails from './RecipeDetails';
import SearchBar from './SearchBar';
import AddRecipe from './AddRecipe';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';

function App() {
    const [recipes, setRecipes] = useState([]);
    const [selectedRecipe, setSelectedRecipe] = useState(null);
    const [showAddRecipeModal, setShowAddRecipeModal] = useState(false);
    const [showLogin, setShowLogin] = useState(false);
    const [showRegister, setShowRegister] = useState(false);
    const [currentUser, setCurrentUser] = useState(null);

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

    const handleLoginSuccess = (username) => {
        setCurrentUser(username);
        setShowLogin(false);
    };

    const handleLogout = () => {
        setCurrentUser(null);
    };

    return (
        <div>
            <header>
                <div className="authentication-info">
                    {currentUser ? `Logged in as: ${currentUser}` : 'Not logged in'}
                    <button onClick={handleLogout}>Logout</button>
                </div>
                <h1>Welcome to the Recipe App</h1>
                <div className="bottom-row">
                    <div>
                        <button onClick={() => setShowLogin(true)}>Login</button>
                        <button onClick={() => setShowRegister(true)}>Register</button>
                    </div>
                    <button onClick={toggleAddRecipeModal}>Add Your Own Recipe</button>
                    <div className="search-bar">
                        <SearchBar onSelectRecipe={handleSelectRecipe} />
                    </div>
                </div>
            </header>
            <div className="main-content">
                <RecipeList recipes={recipes} onSelectRecipe={handleSelectRecipe} />
            </div>
            {selectedRecipe && <RecipeDetails recipe={selectedRecipe} onClose={handleCloseModal} onDelete={handleDeleteRecipe} />}
            {showAddRecipeModal && <AddRecipe onAddRecipe={handleAddRecipe} onCancel={() => setShowAddRecipeModal(false)} />}
            {showLogin && <LoginForm onClose={() => setShowLogin(false)} onLoginSuccess={handleLoginSuccess} />}
            {showRegister && <RegisterForm onClose={() => setShowRegister(false)} />}
        </div>
    );
}

export default App;
