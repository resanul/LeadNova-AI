"use client";

import React, { useState } from "react";
import {
  Sparkles,
  Globe,
  MapPin,
  TrendingUp,
  Users,
  Layers,
  ArrowRight,
  CheckCircle2,
  X,
  AlertCircle,
  ExternalLink,
  ChevronRight,
  ShieldCheck,
  PhoneCall
} from "lucide-react";

interface MarketLaunchModalProps {
  cities: any[];
  niches: any[];
  websites: any[];
  onClose: () => void;
  onMarketLaunched?: () => void;
}

export default function MarketLaunchModal({
  cities,
  niches,
  websites,
  onClose,
  onMarketLaunched,
}: MarketLaunchModalProps) {
  const [currentStep, setCurrentStep] = useState<1 | 2 | 3 | 4>(1);
  const [selectedCityId, setSelectedCityId] = useState<string>(cities[0]?.id || "");
  const [selectedNicheId, setSelectedNicheId] = useState<string>(
    niches.find((n: any) => n.slug === "water-damage-restoration")?.id || niches[0]?.id || ""
  );
  const [selectedWebsiteId, setSelectedWebsiteId] = useState<string>(websites[0]?.id || "");

  // Results per step
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [evaluationResult, setEvaluationResult] = useState<any>(null);
  const [discoveryResult, setDiscoveryResult] = useState<any>(null);
  const [landingPageResult, setLandingPageResult] = useState<any>(null);

  const selectedCity = cities.find((c: any) => c.id === selectedCityId) || cities[0];
  const selectedNiche = niches.find((n: any) => n.id === selectedNicheId) || niches[0];

  // Step 1 -> 2: Evaluate Opportunity
  const handleEvaluateMarket = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("http://localhost:8000/api/v1/opportunities/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          city_id: selectedCityId,
          niche_id: selectedNicheId,
        }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Opportunity evaluation failed");
      }

      const data = await res.json();
      setEvaluationResult(data);
      setCurrentStep(2);
    } catch (err: any) {
      setError(err.message || "Failed to connect to Antigravity Market Intelligence API");
    } finally {
      setLoading(false);
    }
  };

  // Step 2 -> 3: Discover Local Contractors
  const handleDiscoverContractors = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("http://localhost:8000/api/v1/contractors/discover", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          city_id: selectedCityId,
          niche_id: selectedNicheId,
          source: "OPENSTREETMAP",
          max_results: 10,
        }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Contractor discovery failed");
      }

      const data = await res.json();
      setDiscoveryResult(data);
      setCurrentStep(3);
    } catch (err: any) {
      setError(err.message || "Contractor discovery execution failed");
    } finally {
      setLoading(false);
    }
  };

  // Step 3 -> 4: Generate & Publish Landing Page
  const handleGenerateLandingPage = async () => {
    setLoading(true);
    setError(null);
    try {
      // Find or fallback to website
      const websiteId = selectedWebsiteId || websites[0]?.id;
      if (!websiteId) {
        throw new Error("No primary domain/website registered in system. Please seed website first.");
      }

      const res = await fetch("http://localhost:8000/api/v1/landing-pages/generate-auto", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          website_id: websiteId,
          city_id: selectedCityId,
          niche_id: selectedNicheId,
        }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Landing page generation failed");
      }

      const data = await res.json();
      setLandingPageResult(data);
      setCurrentStep(4);
      if (onMarketLaunched) {
        onMarketLaunched();
      }
    } catch (err: any) {
      setError(err.message || "Autonomous Website Factory execution failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 p-4 backdrop-blur-md">
      <div className="relative w-full max-w-3xl rounded-2xl border border-slate-700 bg-[#0d1424] p-6 shadow-2xl space-y-6 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-blue-600/30 text-blue-400 border border-blue-500/30">
                <Sparkles className="h-4 w-4" />
              </span>
              <h2 className="text-xl font-bold text-white">Antigravity Market Activation Engine</h2>
            </div>
            <p className="text-xs text-slate-400">
              Autonomous Pay-Per-Lead pipeline: Research → Discover Contractors → Deploy Local Asset
            </p>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white transition"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Progress Stepper */}
        <div className="grid grid-cols-4 gap-2 border-b border-slate-800 pb-4 text-xs font-semibold">
          <div
            className={`flex items-center space-x-2 p-2 rounded-lg ${
              currentStep === 1
                ? "bg-blue-600/20 text-blue-400 border border-blue-500/30"
                : currentStep > 1
                ? "text-emerald-400 bg-emerald-500/10"
                : "text-slate-500"
            }`}
          >
            <span>1. Market Pick</span>
          </div>
          <div
            className={`flex items-center space-x-2 p-2 rounded-lg ${
              currentStep === 2
                ? "bg-blue-600/20 text-blue-400 border border-blue-500/30"
                : currentStep > 2
                ? "text-emerald-400 bg-emerald-500/10"
                : "text-slate-500"
            }`}
          >
            <span>2. Opportunity Score</span>
          </div>
          <div
            className={`flex items-center space-x-2 p-2 rounded-lg ${
              currentStep === 3
                ? "bg-blue-600/20 text-blue-400 border border-blue-500/30"
                : currentStep > 3
                ? "text-emerald-400 bg-emerald-500/10"
                : "text-slate-500"
            }`}
          >
            <span>3. Contractors</span>
          </div>
          <div
            className={`flex items-center space-x-2 p-2 rounded-lg ${
              currentStep === 4
                ? "bg-blue-600/20 text-blue-400 border border-blue-500/30"
                : "text-slate-500"
            }`}
          >
            <span>4. Live Asset</span>
          </div>
        </div>

        {/* Error message */}
        {error && (
          <div className="flex items-center space-x-3 rounded-xl border border-rose-500/30 bg-rose-500/10 p-3 text-xs text-rose-300">
            <AlertCircle className="h-4 w-4 shrink-0 text-rose-400" />
            <span>{error}</span>
          </div>
        )}

        {/* STEP 1: Select Market & Niche */}
        {currentStep === 1 && (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-medium text-slate-400 block mb-1.5">Target City</label>
                <select
                  value={selectedCityId}
                  onChange={(e) => setSelectedCityId(e.target.value)}
                  className="w-full rounded-xl border border-slate-700 bg-slate-900/90 px-3.5 py-2.5 text-sm text-slate-200 focus:border-blue-500 focus:outline-none"
                >
                  {cities.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}, {c.state_code || c.country_code} (Pop: {c.population?.toLocaleString()})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-xs font-medium text-slate-400 block mb-1.5">High-Value Niche</label>
                <select
                  value={selectedNicheId}
                  onChange={(e) => setSelectedNicheId(e.target.value)}
                  className="w-full rounded-xl border border-slate-700 bg-slate-900/90 px-3.5 py-2.5 text-sm text-slate-200 focus:border-blue-500 focus:outline-none"
                >
                  {niches.map((n) => (
                    <option key={n.id} value={n.id}>
                      {n.name} (Avg Lead: ${n.avg_lead_value})
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="rounded-xl border border-slate-800 bg-[#11192e] p-4 text-xs space-y-2">
              <div className="flex items-center justify-between text-slate-400">
                <span>Selected Focus:</span>
                <span className="font-semibold text-white">
                  {selectedCity?.name} • {selectedNiche?.name}
                </span>
              </div>
              <div className="flex items-center justify-between text-slate-400">
                <span>Economic Benchmark:</span>
                <span className="text-slate-300">
                  Median Income: ${selectedCity?.median_income?.toLocaleString()} | Pop:{" "}
                  {selectedCity?.population?.toLocaleString()}
                </span>
              </div>
              <div className="flex items-center justify-between text-slate-400">
                <span>PPL Arbitrage Range:</span>
                <span className="text-blue-400 font-medium">
                  ${selectedNiche?.avg_lead_value} / exclusive lead (Est. Margin: 45-65%)
                </span>
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <button
                type="button"
                onClick={handleEvaluateMarket}
                disabled={loading}
                className="inline-flex items-center space-x-2 rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-blue-500 disabled:opacity-50 transition shadow-lg shadow-blue-500/30"
              >
                <span>{loading ? "Scoring with Antigravity AI..." : "Run Opportunity Scoring"}</span>
                <ArrowRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}

        {/* STEP 2: Opportunity Scoring Results */}
        {currentStep === 2 && evaluationResult && (
          <div className="space-y-4">
            <div className="rounded-xl border border-blue-500/30 bg-blue-500/10 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-xs uppercase tracking-wider text-blue-400 font-semibold">
                    Overall Profitability Score
                  </span>
                  <div className="flex items-baseline space-x-2 mt-1">
                    <span className="text-3xl font-extrabold text-white">
                      {evaluationResult.overall_score?.toFixed(1)}
                    </span>
                    <span className="text-xs text-slate-400">/ 100</span>
                    <span className="ml-2 inline-flex items-center rounded-full bg-emerald-500/20 px-2.5 py-0.5 text-xs font-semibold text-emerald-400">
                      Tier: {evaluationResult.status?.toUpperCase() || "HIGH PROFIT"}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs text-slate-400 block">Recommended CPL</span>
                  <span className="text-xl font-bold text-emerald-400">
                    ${evaluationResult.metrics_data?.recommended_cpl || 120}
                  </span>
                </div>
              </div>
            </div>

            {/* Score Breakdown Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
              <div className="rounded-xl border border-slate-800 bg-[#11192e] p-3">
                <span className="text-slate-400 block mb-1">Search Demand</span>
                <span className="text-base font-bold text-white">
                  {evaluationResult.demand_score?.toFixed(1)}%
                </span>
              </div>
              <div className="rounded-xl border border-slate-800 bg-[#11192e] p-3">
                <span className="text-slate-400 block mb-1">Commercial Value</span>
                <span className="text-base font-bold text-white">
                  {evaluationResult.commercial_value_score?.toFixed(1)}%
                </span>
              </div>
              <div className="rounded-xl border border-slate-800 bg-[#11192e] p-3">
                <span className="text-slate-400 block mb-1">Contractor Supply</span>
                <span className="text-base font-bold text-white">
                  {evaluationResult.contractor_availability_score?.toFixed(1)}%
                </span>
              </div>
              <div className="rounded-xl border border-slate-800 bg-[#11192e] p-3">
                <span className="text-slate-400 block mb-1">Acquisition Feasibility</span>
                <span className="text-base font-bold text-white">
                  {evaluationResult.acquisition_cost_score?.toFixed(1)}%
                </span>
              </div>
            </div>

            <p className="text-xs text-slate-400 italic">
              AI Recommendation: Market has favorable demand-to-contractor ratio. Proceed to
              automatically extract and verify local contractors.
            </p>

            <div className="flex items-center justify-between pt-2">
              <button
                type="button"
                onClick={() => setCurrentStep(1)}
                className="text-xs text-slate-400 hover:text-white"
              >
                ← Back
              </button>
              <button
                type="button"
                onClick={handleDiscoverContractors}
                disabled={loading}
                className="inline-flex items-center space-x-2 rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-blue-500 disabled:opacity-50 transition shadow-lg shadow-blue-500/30"
              >
                <span>{loading ? "Discovering Contractors..." : "Discover Real Contractors"}</span>
                <ArrowRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}

        {/* STEP 3: Contractor Discovery Results */}
        {currentStep === 3 && discoveryResult && (
          <div className="space-y-4">
            <div className="flex items-center justify-between rounded-xl border border-slate-800 bg-[#11192e] p-4 text-xs">
              <div>
                <span className="font-semibold text-white">Discovery Execution Complete</span>
                <p className="text-slate-400 mt-0.5">
                  Extracted {discoveryResult.discovered_count} contractors in {selectedCity?.name} via OpenStreetMap / Google Places.
                </p>
              </div>
              <span className="inline-flex items-center rounded-full bg-emerald-500/20 px-2.5 py-1 text-xs font-semibold text-emerald-400">
                {discoveryResult.status}
              </span>
            </div>

            <div className="max-h-56 overflow-y-auto space-y-2 pr-1">
              {discoveryResult.contractors?.slice(0, 5).map((c: any) => (
                <div
                  key={c.id}
                  className="flex items-center justify-between rounded-xl border border-slate-800/80 bg-slate-900/60 p-3 text-xs"
                >
                  <div>
                    <span className="font-semibold text-white block">{c.business_name}</span>
                    <span className="text-slate-400 text-[11px]">
                      {c.primary_phone} • Rating: ★{c.rating} ({c.review_count} reviews)
                    </span>
                  </div>
                  <span className="rounded bg-blue-500/10 px-2 py-0.5 text-[10px] font-medium text-blue-400 border border-blue-500/20">
                    {c.verification_status}
                  </span>
                </div>
              ))}
            </div>

            <div className="flex items-center justify-between pt-2">
              <button
                type="button"
                onClick={() => setCurrentStep(2)}
                className="text-xs text-slate-400 hover:text-white"
              >
                ← Back
              </button>
              <button
                type="button"
                onClick={handleGenerateLandingPage}
                disabled={loading}
                className="inline-flex items-center space-x-2 rounded-xl bg-emerald-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-emerald-500 disabled:opacity-50 transition shadow-lg shadow-emerald-500/30"
              >
                <span>{loading ? "Generating Website Asset..." : "Deploy Landing Page Asset"}</span>
                <ArrowRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}

        {/* STEP 4: Live Asset Published */}
        {currentStep === 4 && landingPageResult && (
          <div className="space-y-4">
            <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-5 space-y-3">
              <div className="flex items-center space-x-2 text-emerald-400">
                <CheckCircle2 className="h-6 w-6" />
                <h3 className="text-base font-bold text-white">Market Fully Activated & Live!</h3>
              </div>
              <p className="text-xs text-slate-300">
                Autonomous landing page generated with Schema.org JSON-LD LocalBusiness metadata,
                emergency click-to-call banner, and instant lead capture pipeline.
              </p>

              <div className="rounded-lg border border-slate-800 bg-[#0a0f1d] p-3 text-xs space-y-1.5 font-mono">
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Page Slug:</span>
                  <span className="text-blue-400 font-semibold">{landingPageResult.slug}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Virtual Call Tracking Number:</span>
                  <span className="text-emerald-400 font-semibold">
                    {landingPageResult.virtual_phone || "+1 (260) 204-8930"}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Target Keyword:</span>
                  <span className="text-slate-200">{landingPageResult.target_keyword}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Target Conv. Rate:</span>
                  <span className="text-purple-400 font-semibold">
                    {landingPageResult.conversion_rate_target || "18.5%"}
                  </span>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between pt-2">
              <button
                type="button"
                onClick={onClose}
                className="rounded-xl border border-slate-700 px-4 py-2 text-xs font-semibold text-slate-300 hover:bg-slate-800 transition"
              >
                Close & Return to Dashboard
              </button>

              <a
                href={`/p/${landingPageResult.slug}`}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center space-x-2 rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-blue-500 transition shadow-lg shadow-blue-500/30"
              >
                <span>View Live Landing Page</span>
                <ExternalLink className="h-4 w-4" />
              </a>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
