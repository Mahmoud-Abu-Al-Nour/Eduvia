import React, { createContext, useContext, useEffect, useState } from "react";
import api from "@/services/api";

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: "admin" | "teacher";
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (access_token: string, refresh_token: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchUserMe = async () => {
    try {
      const response = await api.get<User>("/users/me");
      setUser(response.data);
    } catch (error) {
      console.error("Failed to fetch user:", error);
      setUser(null);
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      fetchUserMe();
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (access_token: string, refresh_token: string) => {
    localStorage.setItem("access_token", access_token);
    localStorage.setItem("refresh_token", refresh_token);
    await fetchUserMe();
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
