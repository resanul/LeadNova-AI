"use client";

import React, { useState } from "react";
import { PhoneCall, ShieldCheck, CheckCircle2, AlertCircle, ArrowRight, Clock } from "lucide-react";

interface LeadFormProps {
  cityId: string;
  nicheId: string;
  trackingPhone: string;
  cityName: string;
  nicheName: string;
}

export default function LeadCaptureForm({
  cityId,
  nicheId,
  trackingPhone,
  cityName,
  nicheName,
}: LeadFormProps) {
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [details, setDetails] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await fetch("http://localhost:8000/api/v1/leads/capture", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          city_id: cityId,
          niche_id: nicheId,
          customer_name: name,
          customer_phone: phone,
          customer_email: email || undefined,
          lead_source: "PUBLIC_LANDING_PAGE",
          details: details || `Emergency request in ${cityName} for ${nicheName}`,
        }),
      });

      if (!res.ok) {
        throw new Error("Unable to submit emergency inquiry. Please call directly.");
      }

      setSubmitted(true);
    } catch (err: any) {
      setError(err.message || "Failed to submit request. Please call our hotline immediately.");
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="rounded-2xl border border-emerald-500/40 bg-emerald-950/40 p-8 text-center space-y-4 shadow-xl">
        <div className="inline-flex h-16 w-16 items-center justify-center rounded-full bg-emerald-500/20 text-emerald-400">
          <CheckCircle2 className="h-10 w-10" />
        </div>
        <h3 className="text-2xl font-bold text-white">Emergency Request Dispatched!</h3>
        <p className="text-sm text-slate-300 max-w-md mx-auto">
          A licensed local {nicheName.toLowerCase()} specialist serving {cityName} has been alerted and will contact you directly at <span className="font-semibold text-emerald-400">{phone}</span> within 5–15 minutes.
        </p>
        <div className="pt-2">
          <a
            href={`tel:${trackingPhone}`}
            className="inline-flex items-center space-x-2 rounded-xl bg-emerald-600 px-6 py-3 font-semibold text-white shadow-lg hover:bg-emerald-500 transition"
          >
            <PhoneCall className="h-5 w-5 animate-pulse" />
            <span>Need Faster Response? Call {trackingPhone}</span>
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-slate-700/80 bg-[#0e1628]/95 p-6 md:p-8 shadow-2xl backdrop-blur-xl">
      <div className="mb-6 space-y-2 text-center md:text-left">
        <div className="inline-flex items-center space-x-1.5 rounded-full bg-red-500/10 px-3 py-1 text-xs font-semibold text-red-400 border border-red-500/20">
          <Clock className="h-3.5 w-3.5 animate-pulse" />
          <span>Average Dispatch Time: Under 15 Minutes</span>
        </div>
        <h3 className="text-xl md:text-2xl font-bold text-white">
          Request Rapid Local Assistance in {cityName}
        </h3>
        <p className="text-xs text-slate-400">
          Fill out this form for immediate phone dispatch to an on-duty specialist. No obligations.
        </p>
      </div>

      {error && (
        <div className="mb-4 flex items-center space-x-2 rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-xs text-red-400">
          <AlertCircle className="h-4 w-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-300">Your Name *</label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Michael Scott"
              className="w-full rounded-xl border border-slate-700 bg-slate-900/90 px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-300">Callback Phone Number *</label>
            <input
              type="tel"
              required
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="(260) 555-0199"
              className="w-full rounded-xl border border-slate-700 bg-slate-900/90 px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>
        </div>

        <div className="space-y-1">
          <label className="text-xs font-medium text-slate-300">Email Address (Optional)</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="michael@example.com"
            className="w-full rounded-xl border border-slate-700 bg-slate-900/90 px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>

        <div className="space-y-1">
          <label className="text-xs font-medium text-slate-300">Describe the Emergency Issue *</label>
          <textarea
            required
            rows={3}
            value={details}
            onChange={(e) => setDetails(e.target.value)}
            placeholder={`e.g. Basement flooded from water heater burst, urgent water extraction needed in ${cityName}...`}
            className="w-full rounded-xl border border-slate-700 bg-slate-900/90 px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          ></textarea>
        </div>

        <div className="pt-2">
          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center space-x-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 py-3.5 text-sm font-bold text-white shadow-lg shadow-blue-500/30 hover:from-blue-500 hover:to-indigo-500 transition disabled:opacity-50"
          >
            <span>{loading ? "Alerting On-Call Specialist..." : "Dispatch Specialist to My Location"}</span>
            <ArrowRight className="h-4 w-4" />
          </button>
        </div>

        <div className="flex items-center justify-center space-x-2 text-[11px] text-slate-400 text-center pt-2">
          <ShieldCheck className="h-4 w-4 text-emerald-400 shrink-0" />
          <span>Your privacy is protected. Inquiries are matched exclusively with licensed {cityName} specialists.</span>
        </div>
      </form>
    </div>
  );
}
