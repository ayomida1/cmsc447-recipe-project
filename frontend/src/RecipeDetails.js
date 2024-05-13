import React, { useState } from 'react';

function RecipeDetails({ recipe, onClose, onDelete, onEdit, currentUser }) {
    const [editMode, setEditMode] = useState(false);
    const [formData, setFormData] = useState({
        name: recipe.name,
        description: recipe.description,
        ingredients: recipe.ingredients,
        instructions: recipe.instructions
    });

    const handleDelete = () => {
        if (!currentUser) {
            alert('You must be logged in to delete recipes.');
            return;
        }
    
        fetch(`http://localhost:5000/delete_recipe/${recipe.id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: currentUser })  // Send username in the request body
        }).then(response => {
            if (response.ok) {
                
                onClose(); // Close the modal after deletion
            } else {
                alert('Failed to delete recipe');
            }
        }).catch(error => {
            console.error('Error deleting recipe:', error);
            alert('Error deleting recipe.');
        });
    };

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleEdit = () => {
        setEditMode(true);
    };

    const handleSave = async () => {
        const response = await fetch(`http://localhost:5000/update_recipe/${recipe.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ...formData, username: currentUser })
        });
        if (response.ok) {
            onEdit(formData);
            setEditMode(false);
        } else {
            alert('Failed to update recipe');
        }
    };

    const handleCancelEdit = () => {
        setEditMode(false);
        setFormData({
            name: recipe.name,
            description: recipe.description,
            ingredients: recipe.ingredients,
            instructions: recipe.instructions
        });
    };

    return (
        <div className="modal-backdrop">
            <div className="modal-content">
                {editMode ? (
                    <>
                        <textarea
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleChange}
                            required
                        />
                        <textarea
                            name="description"
                            value={formData.description}
                            onChange={handleChange}
                            required
                        />
                        <textarea
                            name="ingredients"
                            value={formData.ingredients}
                            onChange={handleChange}
                            required
                        />
                        <textarea
                            name="instructions"
                            value={formData.instructions}
                            onChange={handleChange}
                            required
                        />
                        <button onClick={handleSave}>Save</button>
                        <button onClick={handleCancelEdit}>Cancel</button>
                    </>
                ) : (
                    <>
                        <h2>{recipe.name}</h2>
                        <p>{recipe.description}</p>
                        <p>{recipe.ingredients}</p>
                        <p>{recipe.instructions}</p>
                        <button onClick={handleEdit}>Edit Recipe</button>                        
                        <button onClick={onClose}>Close</button>
                        <button onClick={handleDelete} style={{ backgroundColor: 'red', color: 'white' }}>
                            Delete Recipe
                        </button>
                    </>
                )}
            </div>
        </div>
    );
}

export default RecipeDetails;
