import React from 'react';

function RecipeCard({ recipe, onClick }) {
  return (
    <div className="recipe-card" onClick={() => onClick(recipe)}>
      <img src={`/food_imgs/${recipe.recipe_img_name}`} alt={recipe.recipe_name} />
      <p>{recipe.name}</p>
    </div>
  );
}

export default RecipeCard;
