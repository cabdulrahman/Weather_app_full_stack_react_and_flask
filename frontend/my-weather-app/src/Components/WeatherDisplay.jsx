import React, { useContext } from "react";
import "./WeatherDisplay.css";
import { AuthContext } from "../context";

function WeatherDisplay({ weather, error }) {
  const { user } = useContext(AuthContext);

  const handleAddFavorite = async () => {
    if (!user) {
      alert("You must be logged in to save favorites.");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:5000/favorites", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          user_id: user.id,
          city_name: weather.city,
        }),
      });

      const data = await res.json();

      if (res.ok) {
        alert("City added to favorites!");
      } else {
        alert(data.error || "Failed to add favorite.");
      }
    } catch (err) {
      alert("Something went wrong.");
    }
  };

  if (error) return <p>{error}</p>;
  if (!weather) return null;

  return (
    <div className="weather-display">
      <h2>{weather.city}</h2>
      <p>Temperature: {weather.temperature}°C</p>
      <p>Condition: {weather.description}</p>
      {user && (
        <button onClick={handleAddFavorite}>Add to Favorites</button>
      )}
    </div>
  );
}

export default WeatherDisplay;