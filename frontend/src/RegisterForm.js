import React, { useState } from 'react';

function RegisterForm({ onClose }) {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        if (password !== repeatPassword) {
            alert('Passwords do not match!');
            return;
        }
        fetch('http://localhost:5000/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, email })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert('Registration successful');
                onClose(); // Close the form
            } else {
                alert(data.error || 'Registration failed');
            }
        })
        .catch(error => {
            console.error('Error registering:', error);
            alert('Error registering');
        });
    };

    return (
        <div className="modal-backdrop">
            <div className="modal-content">
                <h2>Register</h2>
                <form onSubmit={handleSubmit}>
                    <label>Username:
                        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
                    </label>
                    <label>Email:
                        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                    </label>
                    <label>Password:
                        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                    </label>
                    <label>Repeat Password:
                        <input type="password" value={repeatPassword} onChange={(e) => setRepeatPassword(e.target.value)} />
                    </label>
                    <button type="submit">Register</button>
                    <button type="button" onClick={onClose}>Cancel</button>
                </form>
            </div>
        </div>
    );
}

export default RegisterForm;
