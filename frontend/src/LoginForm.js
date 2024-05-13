import React, { useState } from 'react';

function LoginForm({ onClose, onLoginSuccess }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert('Login successful');
                onLoginSuccess(username); // Call the onLoginSuccess function passing the username
                onClose(); // Close the form
            } else {
                alert(data.error || 'Login failed');
            }
        })
        .catch(error => {
            console.error('Error logging in:', error);
            alert('Error logging in');
        });
    };

    return (
        <div className="modal-backdrop">
            <div className="modal-content">
                <h2>Login</h2>
                <form onSubmit={handleSubmit}>
                    <label>Username:
                        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
                    </label>
                    <label>Password:
                        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                    </label>
                    <button type="submit">Login</button>
                    <button type="button" onClick={onClose}>Cancel</button>
                </form>
            </div>
        </div>
    );
}

export default LoginForm;
