import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context.jsx";
import { useNavigate } from "react-router-dom";

const Favorites = () => {
  const { token, user } = useContext(AuthContext);
  const [favorites, setFavorites] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate("/login");
      return;
    }

    fetch("http://127.0.0.1:5000/favorites", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}` // ✅ Corrected this line
      },
      credentials: "include"
    })
      .then((r) => {
        if (!r.ok) {
          throw new Error("Failed to fetch favorites");
        }
        return r.json();
      })
      .then(setFavorites)
      .catch((err) => console.log("Fetch error:", err));
  }, [token, user]);

  return (
    <div>
      <h2>Your Favorite Cities</h2>
      {favorites.length === 0 ? (
        <p>No favorites yet.</p>
      ) : (
        <ul>
          {favorites.map((fav) => (
            <li key={fav.id}>{fav.city_name}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Favorites;