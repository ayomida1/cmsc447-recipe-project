import React from 'react';

function RecipeDetails({ recipe, onClose, onDelete }) {
    if (!recipe) return null;

    const handleDelete = () => {
        fetch(`http://localhost:5000/delete_recipe/${recipe.id}`, {
            method: 'DELETE'
        }).then(response => {
            if (response.ok) {
                onDelete();  // This is where it seems to fail
                onClose(); // Close the modal after deletion
            } else {
                alert('Failed to delete recipe');
            }
        }).catch(error => {
            console.error('Error deleting recipe:', error);
            alert('Error deleting recipe.');
        });
    };

    return (
        <div className="modal-backdrop">
            <div className="modal-content">
                <h2>{recipe.name}</h2>
                <img src={recipe.image || 'https://via.placeholder.com/150'} alt={recipe.name} style={{ width: '100%' }} />
                <p>Description: {recipe.description}</p>
                <p>Ingredients: {recipe.ingredients}</p>
                <p>Instructions: {recipe.instructions}</p>
                <div>
                    <button onClick={onClose}>Close</button>
                    <button onClick={handleDelete} style={{ backgroundColor: 'red', color: 'white' }}>
                        Delete Recipe
                    </button>
                </div>
            </div>
        </div>
    );
}

export default RecipeDetails;
