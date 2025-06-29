import React, { createContext, useState, useEffect } from "react";

// Create the context
export const AuthContext = createContext();

// Create the provider
export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [user, setUser] = useState(null);

  // Auto-fetch user when token is available
  useEffect(() => {
    if (token) {
      fetch("http://127.0.0.1:5000/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((r) => {
          if (!r.ok) throw new Error("Unauthorized");
          return r.json();
        })
        .then((data) => setUser(data))
        .catch(() => {
          setUser(null);
          setToken(null);
          localStorage.removeItem("token");
        });
    }
  }, [token]);

  const login = (newToken) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ token, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};