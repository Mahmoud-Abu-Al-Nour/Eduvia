import React, { useEffect, useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "./AuthContext";
import api from "@/services/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Lock, Mail, ShieldAlert, UserCheck } from "lucide-react";

export const LoginPage: React.FC = () => {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (user) {
      const from = (location.state as any)?.from?.pathname || "/dashboard";
      navigate(from, { replace: true });
    }
  }, [user, navigate, location]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await api.post<{ access_token: string; refresh_token: string }>("/auth/login", formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      const accessToken = response.access_token || (response as any).data?.access_token;
      const refreshToken = response.refresh_token || (response as any).data?.refresh_token;
      await login(accessToken, refreshToken);

      const from = (location.state as any)?.from?.pathname || "/dashboard";
      navigate(from, { replace: true });
    } catch (err: any) {
      setError(
        err.message ||
        err.response?.data?.message ||
        err.response?.data?.detail ||
        "Invalid credentials. Please verify your email and password."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const fillDemoAccount = (demoEmail: string, demoPass: string) => {
    setEmail(demoEmail);
    setPassword(demoPass);
    setError("");
  };

  return (
    <div className="min-h-screen bg-[#faf8f5] flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <Link
          to="/"
          className="inline-flex items-center text-xs font-semibold text-slate-500 hover:text-slate-800 transition-colors mb-6"
        >
          <ArrowLeft className="w-3.5 h-3.5 mr-1" />
          Back to Eduvia overview
        </Link>

        <div className="flex items-center justify-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-xl bg-brand-800 text-white flex items-center justify-center font-bold text-xl shadow-xs">
            E
          </div>
          <span className="text-2xl font-bold tracking-tight text-slate-900">Eduvia</span>
        </div>
        <p className="text-center text-sm text-slate-600">
          Teacher &amp; Administrator Learning Workspace
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <Card className="border-slate-200/90 shadow-sm bg-white">
          <CardHeader className="pb-4">
            <CardTitle className="text-lg font-bold text-slate-900">Sign in to your account</CardTitle>
            <CardDescription className="text-xs">
              Access your classroom cohort, curriculum maps, and adaptive insights.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {error && (
              <Alert variant="destructive" className="py-2.5">
                <ShieldAlert className="w-4 h-4" />
                <AlertDescription className="text-xs font-medium">{error}</AlertDescription>
              </Alert>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-1.5">
                <label htmlFor="email" className="block text-xs font-semibold text-slate-700">
                  Email Address
                </label>
                <div className="relative">
                  <Input
                    id="email"
                    type="email"
                    required
                    placeholder="teacher@eduvia.app"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="pl-9 text-sm"
                  />
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3 pointer-events-none" />
                </div>
              </div>

              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <label htmlFor="password" className="block text-xs font-semibold text-slate-700">
                    Password
                  </label>
                </div>
                <div className="relative">
                  <Input
                    id="password"
                    type="password"
                    required
                    placeholder="••••••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="pl-9 text-sm"
                  />
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3 pointer-events-none" />
                </div>
              </div>

              <Button
                type="submit"
                variant="default"
                size="default"
                className="w-full font-semibold"
                isLoading={isLoading}
              >
                Sign In to Workspace
              </Button>
            </form>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-slate-200" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-white px-2 text-slate-500 font-semibold tracking-wider text-[10px]">
                  Quick Demo Accounts
                </span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => fillDemoAccount("teacher@eduvia.app", "strongpassword123")}
                className="flex flex-col items-start p-2.5 rounded-lg border border-slate-200 hover:border-brand-300 hover:bg-brand-50/50 transition-all text-left group"
              >
                <div className="flex items-center gap-1.5 text-xs font-bold text-slate-800 group-hover:text-brand-800">
                  <UserCheck className="w-3.5 h-3.5 text-brand-700" />
                  <span>Teacher Demo</span>
                </div>
                <span className="text-[10px] text-slate-500 font-mono mt-0.5 truncate w-full">
                  teacher@eduvia.app
                </span>
              </button>

              <button
                type="button"
                onClick={() => fillDemoAccount("admin@eduvia.app", "adminpassword123")}
                className="flex flex-col items-start p-2.5 rounded-lg border border-slate-200 hover:border-slate-300 hover:bg-slate-50 transition-all text-left group"
              >
                <div className="flex items-center gap-1.5 text-xs font-bold text-slate-800">
                  <Badge variant="outline" className="px-1 py-0 text-[9px] uppercase">Admin</Badge>
                  <span>Admin Demo</span>
                </div>
                <span className="text-[10px] text-slate-500 font-mono mt-0.5 truncate w-full">
                  admin@eduvia.app
                </span>
              </button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
