import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import WeatherForm from "./Components/WeatherForm";
import WeatherDisplay from "./Components/WeatherDisplay";
import RegisterForm from "./Components/RegisterForm";
import { AuthProvider } from "./context";
import Login from "./Components/Login";
import Favorites from "./Components/Favorites";
import "./App.css";

function App() {
  const [weather, setWeather] = useState(null);
  const [error, setError] = useState(null);

  const handleSearch = async (city) => {
    try {
      const res = await fetch(`http://127.0.0.1:5000/weather?city=${city}`);
      const data = await res.json();

      if (res.ok) {
        setWeather(data);
        setError(null);
      } else {
        setError(data.error);
        setWeather(null);
      }
    } catch (err) {
      setError("Something went wrong.");
    }
  };

  return (
    <AuthProvider>
      <Router>
        <nav>
          <Link to="/">Weather</Link> | <Link to="/register">Register</Link> | <Link to="/login">Login</Link> | <Link to="/favorites">Favorites</Link>
        </nav>

        <Routes>
          <Route
            path="/"
            element={
              <>
                <WeatherForm onSearch={handleSearch} />
                <WeatherDisplay weather={weather} error={error} />
              </>
            }
          />
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/login" element={<Login />} />
          <Route path="/favorites" element={<Favorites />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;