import React, { useState, useEffect } from 'react';
import './App.css';
import RecipeList from './RecipeList';
import RecipeDetails from './RecipeDetails';
import SearchBar from './SearchBar';
import AddRecipe from './AddRecipe';
import LoginForm from './LoginForm'; 
import RegisterForm from './RegisterForm';
import SavedRecipes from './SavedRecipes';

function App() {
    const [recipes, setRecipes] = useState([]);
    const [selectedRecipe, setSelectedRecipe] = useState(null);
    const [showAddRecipeModal, setShowAddRecipeModal] = useState(false);
    const [showLogin, setShowLogin] = useState(false);
    const [showRegister, setShowRegister] = useState(false);
    const [currentUser, setCurrentUser] = useState(localStorage.getItem('username'));

    useEffect(() => {
        if (currentUser) {
            // Check if the user exists in the backend
            fetch(`http://localhost:5000/user_exists?username=${currentUser}`)
                .then(response => response.json())
                .then(data => {
                    if (!data.exists) {
                        // If the user does not exist, clear local storage and set currentUser to null
                        localStorage.removeItem('username');
                        setCurrentUser(null);
                        setShowLogin(true); // Show login form
                    }
                })
                .catch(error => console.error('Error checking user existence:', error));
        }
    }, [currentUser]);

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

    const handleEditRecipe = updatedRecipe => {
        const updatedRecipes = recipes.map(recipe =>
            recipe.id === updatedRecipe.id ? updatedRecipe : recipe
        );
        setRecipes(updatedRecipes);
    };

    const handleAddRecipe = newRecipe => {
        setShowAddRecipeModal(false);
        // Optionally add the recipe to the state if you want to display it immediately
    };

    const toggleAddRecipeModal = () => {
        setShowAddRecipeModal(!showAddRecipeModal);
    };

    const handleLoginSuccess = (username) => {
        localStorage.setItem('username', username);
        setCurrentUser(username);
        setShowLogin(false);
    };

    const handleLogout = () => {
        localStorage.removeItem('username');
        setCurrentUser(null);
    };

    return (
        <div className="App">
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
            <RecipeList 
                recipes={recipes}
                onSelectRecipe={handleSelectRecipe} 
                currentUser={currentUser}
                onEdit={handleEditRecipe}  // Passing down the handleEditRecipe function
            />         
            {selectedRecipe && <RecipeDetails recipe={selectedRecipe} onClose={handleCloseModal} onDelete={handleDeleteRecipe} onEdit={handleEditRecipe} currentUser={currentUser} />}
            {showAddRecipeModal && <AddRecipe 
                onAddRecipe={handleAddRecipe} 
                onCancel={() => setShowAddRecipeModal(false)} 
                isLoggedIn={!!currentUser} 
                currentUser={currentUser} 
            />}
            {showLogin && <LoginForm onClose={() => setShowLogin(false)} onLoginSuccess={handleLoginSuccess} />}
            {showRegister && <RegisterForm onClose={() => setShowRegister(false)} />}
            {currentUser && <h2 className="saved-recipes-header"> {currentUser}'s Saved Recipes</h2>}
            <SavedRecipes 
                currentUser={currentUser} 
                setSelectedRecipe={setSelectedRecipe}  // Pass the setter function
            />
        </div>
    );
}

export default App;
