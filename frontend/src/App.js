import React from 'react';
import Recipe from './Recipe';
import AddRecipe from './AddRecipe';

function App() {
  return (
    <div>
      <header>
        <h1>Welcome to the Recipe App</h1>
      </header>
      <main>
        <p>Here you can find and share amazing recipes!</p>
        <Recipe /> 
        <p>Add your own recipe down below</p>
        <AddRecipe />
      </main>
      <footer>

      </footer>
    </div>
  );
}

export default App;
