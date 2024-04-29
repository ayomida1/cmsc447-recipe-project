import React, { useState } from 'react';

function SearchBar({ onSelectRecipe }) {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = async () => {
        if (!query) return;
        try {
            const response = await fetch(`http://localhost:5000/search?query=${encodeURIComponent(query)}`);
            if (response.ok) {
                const data = await response.json();
                setResults(data);
            } else {
                console.error('Failed to fetch recipes');
                setResults([]);
            }
        } catch (error) {
            console.error('Error fetching recipes:', error);
            setResults([]);
        }
    };

    return (
        <div className="search-bar">
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyUp={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Enter search term..."
            />
            <button onClick={handleSearch}>Search</button>
            {results.length > 0 && (
                <ul className="search-results">
                    {results.map(result => (
                        <li key={result.id} onClick={() => onSelectRecipe(result)}>
                            {result.name}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default SearchBar;