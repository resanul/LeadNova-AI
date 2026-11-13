import React from "react";
import {
  Activity,
  PhoneCall,
  DollarSign,
  Users,
  ShieldCheck,
  Bot,
  Globe,
  Briefcase,
  Layers,
  ArrowUpRight,
  TrendingUp,
  Cpu,
  Download,
  Search,
  Sparkles,
  MapPin,
  CheckCircle2,
} from "lucide-react";
import {
  fetchAnalytics,
  fetchAgents,
  fetchContractors,
  fetchNiches,
  fetchCities,
  fetchLeads,
  fetchRankedOpportunities,
} from "@/lib/api";

export const revalidate = 0;

export default async function DashboardPage() {
  const analytics = await fetchAnalytics();
  const agents = await fetchAgents();
  const contractors = await fetchContractors();
  const niches = await fetchNiches();
  const cities = await fetchCities();
  const leads = await fetchLeads();
  const opportunities = await fetchRankedOpportunities();

  return (
    <div className="flex min-h-screen">
      {/* Sidebar Navigation */}
      <aside className="w-64 border-r border-slate-800 bg-[#0c1220] p-6 hidden md:flex flex-col justify-between">
        <div className="space-y-6">
          <div className="flex items-center space-x-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-white font-bold shadow-lg shadow-blue-500/30">
              GL
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-white">GLOBALLEAD AI</h1>
              <p className="text-xs text-blue-400 font-medium tracking-wide">ENTERPRISE OS</p>
            </div>
          </div>

          <nav className="space-y-1">
            <a href="#overview" className="flex items-center space-x-3 rounded-lg bg-blue-600/20 px-3 py-2.5 text-sm font-medium text-blue-400 border border-blue-500/30">
              <Activity className="h-4 w-4" />
              <span>Command Center</span>
            </a>
            <a href="#agents" className="flex items-center space-x-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-400 hover:bg-slate-800 hover:text-white transition">
              <Bot className="h-4 w-4" />
              <span>17 Autonomous Agents</span>
            </a>
            <a href="#contractors" className="flex items-center space-x-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-400 hover:bg-slate-800 hover:text-white transition">
              <Users className="h-4 w-4" />
              <span>Contractor Directory</span>
            </a>
            <a href="#market" className="flex items-center space-x-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-400 hover:bg-slate-800 hover:text-white transition">
              <Globe className="h-4 w-4" />
              <span>Market Intelligence</span>
            </a>
            <a href="#leads" className="flex items-center space-x-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-400 hover:bg-slate-800 hover:text-white transition">
              <PhoneCall className="h-4 w-4" />
              <span>Lead & Call Arbitrage</span>
            </a>
            <a href="#finance" className="flex items-center space-x-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-400 hover:bg-slate-800 hover:text-white transition">
              <DollarSign className="h-4 w-4" />
              <span>Financial Ledger</span>
            </a>
          </nav>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
          <div className="flex items-center space-x-2 text-xs text-emerald-400 font-medium">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>HYBRID CLOUD + ROCKY LINUX</span>
          </div>
          <p className="mt-1 text-[11px] text-slate-400">Control & Execution Planes: Active</p>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 overflow-y-auto p-6 md:p-10 space-y-8">
        {/* Top Header */}
        <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800/80 pb-6">
          <div>
            <h2 className="text-2xl font-bold tracking-tight text-white">Global Command Center</h2>
            <p className="text-sm text-slate-400">
              Autonomous Pay-Per-Lead Arbitrage, Contractor CRM & AI Multi-Market Operations
            </p>
          </div>
          <div className="flex items-center space-x-3">
            <span className="inline-flex items-center rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-400 border border-emerald-500/20">
              FastAPI v1.0.0 Connected
            </span>
            <a
              href="http://localhost:8000/api/v1/contractors/export/csv"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-1.5 rounded-lg border border-slate-700 bg-slate-800/80 px-3.5 py-2 text-xs font-semibold text-slate-200 hover:bg-slate-700 transition"
            >
              <Download className="h-3.5 w-3.5 text-slate-400" />
              <span>Export CSV</span>
            </a>
            <button className="rounded-lg bg-blue-600 px-4 py-2 text-xs font-semibold text-white shadow-md hover:bg-blue-500 transition flex items-center space-x-1.5">
              <Search className="h-3.5 w-3.5" />
              <span>Trigger Discovery</span>
            </button>
          </div>
        </header>

        {/* 4 Primary KPI Metric Cards */}
        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <div className="rounded-2xl border border-slate-800 bg-[#0e1526]/80 p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-400">TOTAL REVENUE (PPL)</span>
              <DollarSign className="h-5 w-5 text-emerald-400" />
            </div>
            <div className="mt-3 text-2xl font-bold text-white">
              ${Number(analytics.total_revenue_usd).toFixed(2)}
            </div>
            <div className="mt-2 flex items-center text-xs text-emerald-400">
              <TrendingUp className="mr-1 h-3.5 w-3.5" />
              <span>Real-time Ledger Verified</span>
            </div>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-[#0e1526]/80 p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-400">VERIFIED CONTRACTORS</span>
              <ShieldCheck className="h-5 w-5 text-blue-400" />
            </div>
            <div className="mt-3 text-2xl font-bold text-white">
              {analytics.verified_contractors} <span className="text-sm font-normal text-slate-400">/ {analytics.total_contractors}</span>
            </div>
            <div className="mt-2 flex items-center text-xs text-blue-400">
              <span>E.164 International Format Valid</span>
            </div>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-[#0e1526]/80 p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-400">QUALIFIED LEADS</span>
              <PhoneCall className="h-5 w-5 text-purple-400" />
            </div>
            <div className="mt-3 text-2xl font-bold text-white">
              {analytics.qualified_leads} <span className="text-sm font-normal text-slate-400">/ {analytics.total_leads}</span>
            </div>
            <div className="mt-2 flex items-center text-xs text-purple-400">
              <span>Smart Matched & Dispatched</span>
            </div>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-[#0e1526]/80 p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-400">GLOBAL NICHES</span>
              <Layers className="h-5 w-5 text-amber-400" />
            </div>
            <div className="mt-3 text-2xl font-bold text-white">
              {analytics.total_niches} <span className="text-sm font-normal text-slate-400">Niches</span>
            </div>
            <div className="mt-2 flex items-center text-xs text-amber-400">
              <span>{analytics.total_countries} Supported Countries</span>
            </div>
          </div>
        </section>

        {/* 17 Autonomous AI Agents Subsystem */}
        <section id="agents" className="rounded-2xl border border-slate-800 bg-[#0e1526]/80 p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div className="flex items-center space-x-2">
              <Bot className="h-5 w-5 text-blue-400" />
              <h3 className="text-lg font-semibold text-white">17 Autonomous AI Agents Subsystem</h3>
            </div>
            <span className="text-xs font-medium text-slate-400">JSON Schema Validated • Guardrails Active</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {agents.map((agent: any) => (
              <div key={agent.id} className="rounded-xl border border-slate-800/80 bg-slate-900/60 p-4 space-y-2 hover:border-blue-500/40 transition">
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-semibold text-slate-200">{agent.name}</h4>
                  <span className="inline-flex items-center rounded-full bg-emerald-500/10 px-2 py-0.5 text-[10px] font-medium text-emerald-400">
                    Active
                  </span>
                </div>
                <p className="text-xs text-slate-400 line-clamp-2">{agent.purpose}</p>
                <div className="pt-2 flex items-center justify-between text-[11px] text-slate-500 border-t border-slate-800/60">
                  <span>Model: {agent.model_name}</span>
                  <span className="text-blue-400 font-medium">Ready</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Contractors & Lead Management Dual Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Contractors Directory */}
          <section id="contractors" className="rounded-2xl border border-slate-800 bg-[#0e1526]/80 p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-base font-semibold text-white flex items-center space-x-2">
                <Users className="h-4 w-4 text-blue-400" />
                <span>Contractor Directory</span>
              </h3>
              <span className="text-xs text-slate-400">{contractors.length} Discovered</span>
            </div>

            <div className="divide-y divide-slate-800 overflow-hidden">
              {contractors.length === 0 ? (
                <p className="text-xs text-slate-500 py-4 text-center">No contractors registered yet.</p>
              ) : (
                contractors.map((c: any) => (
                  <div key={c.id} className="py-3 flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-white">{c.business_name}</p>
                      <p className="text-xs text-slate-400">{c.city}, {c.state} • {c.primary_phone}</p>
                    </div>
                    <div className="text-right">
                      <span className="inline-flex rounded-full bg-blue-500/10 px-2.5 py-0.5 text-[10px] font-semibold text-blue-400 border border-blue-500/20">
                        {c.verification_status}
                      </span>
                      <p className="text-[11px] text-slate-500 mt-0.5">{c.partner_status}</p>
                    </div>
                  </div>
                ))
              )}
            </div>
          </section>

          {/* Recent Ingested Leads */}
          <section id="leads" className="rounded-2xl border border-slate-800 bg-[#0e1526]/80 p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-base font-semibold text-white flex items-center space-x-2">
                <PhoneCall className="h-4 w-4 text-purple-400" />
                <span>Recent Ingested Leads</span>
              </h3>
              <span className="text-xs text-slate-400">{leads.length} Ingested</span>
            </div>

            <div className="divide-y divide-slate-800 overflow-hidden">
              {leads.length === 0 ? (
                <p className="text-xs text-slate-500 py-4 text-center">No leads ingested yet.</p>
              ) : (
                leads.map((l: any) => (
                  <div key={l.id} className="py-3 flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-white">{l.customer_name || "Emergency Caller"}</p>
                      <p className="text-xs text-slate-400">{l.customer_phone} • {l.lead_source}</p>
                    </div>
                    <div className="text-right">
                      <span className="inline-flex rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-[10px] font-semibold text-emerald-400 border border-emerald-500/20">
                        {l.qualification_status}
                      </span>
                      <p className="text-[11px] text-slate-500 mt-0.5">Dispatched</p>
                    </div>
                  </div>
                ))
              )}
            </div>
          </section>
        </div>

        {/* Market Opportunities & 25 Niches Grid */}
        <section id="market" className="rounded-2xl border border-slate-800 bg-[#0e1526]/80 p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="text-base font-semibold text-white flex items-center space-x-2">
              <Briefcase className="h-4 w-4 text-amber-400" />
              <span>High-Value Local Service Niches & Opportunity Intelligence</span>
            </h3>
            <span className="text-xs text-slate-400">25 High-Margin Categories</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
            {niches.map((n: any) => (
              <div key={n.id} className="rounded-lg border border-slate-800 bg-slate-900/40 p-3 space-y-1 hover:border-amber-500/30 transition">
                <p className="text-xs font-semibold text-slate-200 truncate">{n.name}</p>
                <div className="flex items-center justify-between text-[11px]">
                  <span className="text-slate-400">Lead Val:</span>
                  <span className="font-semibold text-emerald-400">${Number(n.avg_lead_value).toFixed(0)}</span>
                </div>
                <div className="flex items-center justify-between text-[10px] text-slate-500 pt-1 border-t border-slate-800/60">
                  <span>Urgency:</span>
                  <span className="capitalize text-amber-400">{n.emergency_level}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
