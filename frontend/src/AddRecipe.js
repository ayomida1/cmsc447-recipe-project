import React, { useState } from 'react';
import Select from 'react-select'

function AddRecipe({ onAddRecipe, onCancel }) {
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        ingredients: '',
        instructions: '',
        tags: []
    });

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const response = await fetch('http://localhost:5000/add_recipe', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        if (response.ok) {
            onAddRecipe(formData);
            setFormData({ name: '', description: '', ingredients: '', instructions: '' , tags: []}); // Reset form
        } else {
            alert('Failed to add recipe');
        }
    };

    const handleCancel = () => {
        setFormData({ name: '', description: '', ingredients: '', instructions: '', tags: []}); // Reset form
        onCancel(); // Call onCancel to hide the form
    };

    const handleSelectChange = (selectedOptions) => {
        // Extracting only values from selected options
        const selectedTags = selectedOptions.map(option => option.value);
        setFormData({ ...formData, tags: selectedTags });
    };

    const tags = [
        { value: 'Breakfast', label: 'Breakfast' },
        { value: 'Lunch', label: 'Lunch' },
        { value: 'Dinner', label: 'Dinner' }
      ]

    return (
        <form className="add-recipe-form" onSubmit={handleSubmit}>
            <h2>Add a New Recipe</h2>
            <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Recipe Name"
                required
            />
            <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="Description"
                required
            />
            <textarea
                name="ingredients"
                value={formData.ingredients}
                onChange={handleChange}
                placeholder="Ingredients"
                required
            />
            <textarea
                name="instructions"
                value={formData.instructions}
                onChange={handleChange}
                placeholder="Instructions"
                required
            />
            <label htmlFor="tags">Select Tags (Optional):</label>
            <Select
                name = "tags"
                value={tags.filter(option => formData.tags.includes(option.value))}
                onChange={handleSelectChange}
                options={tags}
                isMulti
            />
            <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'space-between' }}>
                <button type="submit">Add Recipe</button>
                <button type="button" onClick={handleCancel} style={{ background: '#f44336', borderColor: '#f44336' }}>Cancel</button>
            </div>
        </form>
    );
}

export default AddRecipe;