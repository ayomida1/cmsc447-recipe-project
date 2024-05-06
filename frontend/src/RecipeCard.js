import React from 'react';

function RecipeCard({ recipe, onClick }) {
  return (
    <div className="recipe-card" onClick={() => onClick(recipe)}>
      <img src={recipe.image || "placeholder_image_url"} alt={recipe.name} />
      <p>{recipe.name}</p>
    </div>
  );
}

export default RecipeCard;
