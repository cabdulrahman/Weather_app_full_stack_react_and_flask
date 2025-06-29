import React, { useState, useContext } from "react";
import { AuthContext } from "../context";

const RegisterForm = () => {
  const { login } = useContext(AuthContext);
  const [username, setUsername] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    fetch("http://127.0.0.1:5000/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username }),
    })
      .then((r) => r.json())
      .then((data) => {
        if (data.token) {
          login(data.token);
          setError("");
        } else {
          setError(data.error || "Registration failed");
        }
      })
      .catch(() => setError("An error occurred during registration"));
  };

  return (
    <div className="auth-form">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter username..."
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <button type="submit">Register</button>
        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
};

export default RegisterForm;
