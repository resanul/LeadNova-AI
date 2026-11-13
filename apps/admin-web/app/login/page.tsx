"use client";

import React, { useState } from "react";
import { Lock, Mail, ArrowRight, ShieldCheck, Sparkles, AlertCircle } from "lucide-react";

export default function LoginPage() {
  const [email, setEmail] = useState("admin@globallead.ai");
  const [password, setPassword] = useState("AdminPassword123!");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [tokenInfo, setTokenInfo] = useState<any>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const res = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || "Authentication failed");
      }

      const data = await res.json();
      localStorage.setItem("access_token", data.access_token);
      setTokenInfo(data);

      // Redirect to main command center
      setTimeout(() => {
        window.location.href = "/";
      }, 1000);
    } catch (err: any) {
      setError(err.message || "Failed to connect to backend gateway");
    } finally {
      setLoading(false);
    }
  };

  const handleQuickAdminLogin = () => {
    setEmail("admin@globallead.ai");
    setPassword("AdminPassword123!");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#070b14] p-4 text-slate-100">
      <div className="w-full max-w-md space-y-8 rounded-2xl border border-slate-800 bg-[#0e1526]/90 p-8 shadow-2xl backdrop-blur-xl">
        {/* Brand Header */}
        <div className="text-center space-y-2">
          <div className="inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-600 text-white font-bold text-xl shadow-lg shadow-blue-500/30">
            GL
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white">GlobalLead AI</h1>
          <p className="text-xs text-blue-400 font-medium tracking-wider uppercase">
            Antigravity Enterprise Authentication
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="flex items-center space-x-2 rounded-lg border border-red-500/20 bg-red-500/10 p-3 text-xs text-red-400">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Success Alert */}
        {tokenInfo && (
          <div className="flex items-center space-x-2 rounded-lg border border-emerald-500/20 bg-emerald-500/10 p-3 text-xs text-emerald-400">
            <ShieldCheck className="h-4 w-4 shrink-0" />
            <span>Authenticated successfully! Redirecting to Command Center...</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleLogin} className="space-y-4">
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-300">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full rounded-xl border border-slate-700 bg-slate-900/80 px-9 py-2 text-sm text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                placeholder="admin@globallead.ai"
              />
            </div>
          </div>

          <div className="space-y-1">
            <div className="flex items-center justify-between">
              <label className="text-xs font-medium text-slate-300">Password</label>
              <button
                type="button"
                onClick={handleQuickAdminLogin}
                className="text-[11px] text-blue-400 hover:text-blue-300 transition"
              >
                Fill Default Credentials
              </button>
            </div>
            <div className="relative">
              <Lock className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full rounded-xl border border-slate-700 bg-slate-900/80 px-9 py-2 text-sm text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                placeholder="••••••••••••"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center space-x-2 rounded-xl bg-blue-600 py-2.5 text-sm font-semibold text-white shadow-lg shadow-blue-500/25 hover:bg-blue-500 transition disabled:opacity-50"
          >
            <span>{loading ? "Authenticating..." : "Sign In to Platform"}</span>
            <ArrowRight className="h-4 w-4" />
          </button>
        </form>

        {/* Antigravity SSO Mock Option */}
        <div className="relative my-4">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-slate-800"></div>
          </div>
          <div className="relative flex justify-center text-xs">
            <span className="bg-[#0e1526] px-2 text-slate-500 uppercase tracking-wider text-[10px]">
              Or Continue With
            </span>
          </div>
        </div>

        <button
          type="button"
          onClick={handleLogin}
          className="w-full flex items-center justify-center space-x-2 rounded-xl border border-slate-700 bg-slate-800/80 py-2.5 text-sm font-medium text-slate-200 hover:bg-slate-800 hover:border-slate-600 transition"
        >
          <Sparkles className="h-4 w-4 text-blue-400" />
          <span>Antigravity One-Click Login</span>
        </button>

        {/* Footer info */}
        <div className="pt-2 text-center text-[11px] text-slate-500">
          <p>Super Admin: <code className="text-slate-400">admin@globallead.ai</code></p>
          <p>Password: <code className="text-slate-400">AdminPassword123!</code></p>
        </div>
      </div>
    </div>
  );
}
