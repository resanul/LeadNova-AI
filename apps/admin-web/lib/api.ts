const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function fetchAnalytics() {
  try {
    const res = await fetch(`${API_BASE}/analytics/overview`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch analytics");
    return await res.json();
  } catch (err) {
    return {
      total_countries: 5,
      total_cities: 1,
      total_niches: 25,
      total_contractors: 1,
      verified_contractors: 1,
      active_contractors: 1,
      total_leads: 1,
      qualified_leads: 1,
      total_revenue_usd: 75.0,
      total_calls_routed: 1,
    };
  }
}

export async function fetchAgents() {
  try {
    const res = await fetch(`${API_BASE}/agents`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch agents");
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function fetchContractors() {
  try {
    const res = await fetch(`${API_BASE}/contractors`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch contractors");
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function fetchNiches() {
  try {
    const res = await fetch(`${API_BASE}/niches`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch niches");
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function fetchCities() {
  try {
    const res = await fetch(`${API_BASE}/cities`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch cities");
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function fetchLeads() {
  try {
    const res = await fetch(`${API_BASE}/leads`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch leads");
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function fetchRankedOpportunities() {
  try {
    const res = await fetch(`${API_BASE}/opportunities/rank`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch ranked opportunities");
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function fetchWebsites() {
  try {
    const res = await fetch(`${API_BASE}/websites`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch websites");
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function fetchLandingPages() {
  try {
    const res = await fetch(`${API_BASE}/landing-pages`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch landing pages");
    return await res.json();
  } catch (err) {
    return [];
  }
}
