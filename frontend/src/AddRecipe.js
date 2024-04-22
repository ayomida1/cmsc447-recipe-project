import React, { useState } from 'react';

function AddRecipe() {
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        ingredients: '',
        instructions: '',
      //  user_id: 0  // Assuming a static user_id for now; adjust as needed
    });

    // Function to update state with form input
    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    // Function to handle form submission
    const handleSubmit = (event) => {
        event.preventDefault(); // Prevent default form submission behavior
        console.log('Submitting:', formData);  // Optional: Log the data being submitted

        // Perform the POST request to the backend
        console.log(JSON.stringify(formData)); //REMOVE LATERS
        fetch('http://localhost:5000/add_recipe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok, status: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            alert(data.message); // Show success message from server
        })
        .catch(error => {
            console.error('Error adding recipe:', error);
            alert('Error adding recipe: ' + error.message); // Show error message
        });
    };

    // JSX for the component
    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="name">Recipe Name:</label>
            <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Enter recipe name"
                required
            />

            <label htmlFor="description">Description:</label>
            <input
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="Describe the recipe"
                required
            />

            <label htmlFor="ingredients">Ingredients:</label>
            <input
                id="ingredients"
                name="ingredients"
                value={formData.ingredients}
                onChange={handleChange}
                placeholder="List ingredients"
                required
            />

            <label htmlFor="instructions">Instructions:</label>
            <input
                id="instructions"
                name="instructions"
                value={formData.instructions}
                onChange={handleChange}
                placeholder="Cooking instructions"
                required
            />

            <button type="submit">Add Recipe</button>
        </form>
    );
}

export default AddRecipe;
