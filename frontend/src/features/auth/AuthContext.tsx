import React, { createContext, useContext, useEffect, useState } from "react";
import api from "@/services/api";
import tokenStorage from "@/services/tokenStorage";

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
      const userData = await api.get<User>("/users/me");
      setUser(userData);
    } catch (error) {
      console.error("Failed to fetch user session:", error);
      setUser(null);
      tokenStorage.clearTokens();
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Check canonical token storage on startup
    if (tokenStorage.hasAccessToken()) {
      fetchUserMe();
    } else {
      setLoading(false);
    }

    // Subscribe to session expiration events (e.g. 401 intercepted in api client)
    const unsubscribe = tokenStorage.onAuthExpired(() => {
      setUser(null);
      setLoading(false);
    });

    return () => {
      unsubscribe();
    };
  }, []);

  const login = async (access_token: string, refresh_token: string) => {
    tokenStorage.setTokens(access_token, refresh_token);
    await fetchUserMe();
  };

  const logout = () => {
    tokenStorage.clearTokens();
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
