import React, { useState, useEffect } from 'react';

function Recipe() {
    const [recipe, setRecipe] = useState({});

    useEffect(() => {
        fetch('http://localhost:5000/recipe') // Adjust the URL based on your Flask route
            .then(response => response.json())
            .then(data => setRecipe(data))
            .catch(error => console.error('Error fetching data: ', error));
    }, []);

    return (
        <div>
            <h2>{recipe.name}</h2>
            <p>{recipe.description}</p>
            <img src={recipe.image} alt={recipe.name} style={{ width: '300px' }} />
        </div>
    );
}

export default Recipe;
