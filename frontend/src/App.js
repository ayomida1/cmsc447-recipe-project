import React from 'react';
import RecipeList from './RecipeList';
import AddRecipe from './AddRecipe';

function App() {
  return (
    <div>
      <header>
        <h1>Welcome to the Recipe App</h1>
      </header>
      <main>
        <RecipeList /> 
        <p>Add your own recipe down below</p>
        <AddRecipe />
      </main>
      <footer>

      </footer>
    </div>
  );
}

export default App;
