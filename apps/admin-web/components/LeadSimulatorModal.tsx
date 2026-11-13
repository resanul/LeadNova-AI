"use client";

import React, { useState } from "react";
import { Zap, CheckCircle2, PhoneCall, DollarSign, X, ArrowRight, ShieldCheck, AlertCircle } from "lucide-react";

interface LeadSimulatorProps {
  cities: any[];
  niches: any[];
  onClose: () => void;
  onLeadProcessed?: () => void;
}

export default function LeadSimulatorModal({
  cities,
  niches,
  onClose,
  onLeadProcessed,
}: LeadSimulatorProps) {
  const [selectedCity, setSelectedCity] = useState(cities[0]?.id || "");
  const [selectedNiche, setSelectedNiche] = useState(
    niches.find((n: any) => n.slug === "water-damage-restoration")?.id || niches[0]?.id || ""
  );
  const [customerName, setCustomerName] = useState("David Miller");
  const [customerPhone, setCustomerPhone] = useState("+12605550" + Math.floor(100 + Math.random() * 900));
  const [emergencyDetails, setEmergencyDetails] = useState("Sump pump failed during storm, 3 inches of water in basement. Need emergency extraction!");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSimulate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch("http://localhost:8000/api/v1/leads/capture", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          city_id: selectedCity,
          niche_id: selectedNiche,
          customer_name: customerName,
          customer_phone: customerPhone,
          customer_email: "david@example.com",
          lead_source: "SIMULATOR_TEST",
          details: emergencyDetails,
        }),
      });

      if (!res.ok) {
        throw new Error("Lead simulation failed. Check backend connection.");
      }

      const leadData = await res.json();
      setResult(leadData);
      if (onLeadProcessed) onLeadProcessed();
    } catch (err: any) {
      setError(err.message || "Failed to simulate lead");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 p-4 backdrop-blur-sm">
      <div className="relative w-full max-w-lg rounded-2xl border border-slate-700 bg-[#0e1628] p-6 shadow-2xl space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center space-x-2">
            <Zap className="h-5 w-5 text-amber-400" />
            <h3 className="text-lg font-bold text-white">Live Lead & Call Arbitrage Simulator</h3>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-800 hover:text-white transition"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {error && (
          <div className="flex items-center space-x-2 rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-xs text-red-400">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {result ? (
          <div className="rounded-xl border border-emerald-500/30 bg-emerald-950/30 p-5 space-y-4">
            <div className="flex items-center space-x-2 text-emerald-400 font-bold text-sm">
              <CheckCircle2 className="h-5 w-5" />
              <span>Lead Processed & Dispatched in Real Time!</span>
            </div>

            <div className="space-y-2 text-xs divide-y divide-slate-800 text-slate-300">
              <div className="pt-2 flex justify-between">
                <span className="text-slate-400">Lead ID:</span>
                <span className="font-mono text-slate-200">{result.id.slice(0, 8)}...</span>
              </div>
              <div className="pt-2 flex justify-between">
                <span className="text-slate-400">Customer Name:</span>
                <span className="font-semibold text-white">{result.customer_name}</span>
              </div>
              <div className="pt-2 flex justify-between">
                <span className="text-slate-400">Customer Phone:</span>
                <span className="font-mono text-emerald-400">{result.customer_phone}</span>
              </div>
              <div className="pt-2 flex justify-between">
                <span className="text-slate-400">Qualification Status:</span>
                <span className="inline-flex rounded-full bg-emerald-500/20 px-2 py-0.5 font-bold text-emerald-400 border border-emerald-500/30">
                  {result.qualification_status}
                </span>
              </div>
              <div className="pt-2 flex justify-between">
                <span className="text-slate-400">Arbitrage Action:</span>
                <span className="text-blue-400 font-medium">Matched & Billed to Active Contractor Wallet</span>
              </div>
            </div>

            <div className="pt-2 flex justify-end space-x-2">
              <button
                onClick={() => {
                  setResult(null);
                  setCustomerPhone("+12605550" + Math.floor(100 + Math.random() * 900));
                }}
                className="rounded-lg bg-blue-600 px-4 py-2 text-xs font-semibold text-white hover:bg-blue-500 transition"
              >
                Simulate Another Lead
              </button>
              <button
                onClick={() => {
                  onClose();
                  window.location.reload();
                }}
                className="rounded-lg border border-slate-700 bg-slate-800 px-4 py-2 text-xs font-semibold text-slate-300 hover:bg-slate-700 transition"
              >
                Done
              </button>
            </div>
          </div>
        ) : (
          <form onSubmit={handleSimulate} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1">
                <label className="text-xs font-medium text-slate-300">Target City</label>
                <select
                  value={selectedCity}
                  onChange={(e) => setSelectedCity(e.target.value)}
                  className="w-full rounded-xl border border-slate-700 bg-slate-900/90 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                >
                  {cities.map((c: any) => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-medium text-slate-300">Target Niche</label>
                <select
                  value={selectedNiche}
                  onChange={(e) => setSelectedNiche(e.target.value)}
                  className="w-full rounded-xl border border-slate-700 bg-slate-900/90 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                >
                  {niches.map((n: any) => (
                    <option key={n.id} value={n.id}>{n.name} (${Number(n.avg_lead_value).toFixed(0)})</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1">
                <label className="text-xs font-medium text-slate-300">Customer Name</label>
                <input
                  type="text"
                  required
                  value={customerName}
                  onChange={(e) => setCustomerName(e.target.value)}
                  className="w-full rounded-xl border border-slate-700 bg-slate-900/90 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-medium text-slate-300">Customer Phone</label>
                <input
                  type="tel"
                  required
                  value={customerPhone}
                  onChange={(e) => setCustomerPhone(e.target.value)}
                  className="w-full rounded-xl border border-slate-700 bg-slate-900/90 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-medium text-slate-300">Emergency Details</label>
              <textarea
                rows={2}
                value={emergencyDetails}
                onChange={(e) => setEmergencyDetails(e.target.value)}
                className="w-full rounded-xl border border-slate-700 bg-slate-900/90 px-3 py-2 text-xs text-white focus:border-blue-500 focus:outline-none"
              ></textarea>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center space-x-2 rounded-xl bg-gradient-to-r from-amber-500 to-orange-500 py-3 text-xs font-bold text-white shadow-lg shadow-amber-500/25 hover:from-amber-400 hover:to-orange-400 transition disabled:opacity-50"
            >
              <span>{loading ? "Simulating Emergency Ingestion..." : "Dispatch Simulated Lead Now"}</span>
              <ArrowRight className="h-4 w-4" />
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
