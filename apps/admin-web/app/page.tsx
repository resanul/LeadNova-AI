import React from "react";
import {
  fetchAnalytics,
  fetchAgents,
  fetchContractors,
  fetchNiches,
  fetchCities,
  fetchLeads,
  fetchRankedOpportunities,
  fetchWebsites,
  fetchLandingPages,
} from "@/lib/api";
import DashboardClient from "@/components/DashboardClient";

export const revalidate = 0;

export default async function DashboardPage() {
  const [
    analytics,
    agents,
    contractors,
    niches,
    cities,
    leads,
    opportunities,
    websites,
    landingPages,
  ] = await Promise.all([
    fetchAnalytics(),
    fetchAgents(),
    fetchContractors(),
    fetchNiches(),
    fetchCities(),
    fetchLeads(),
    fetchRankedOpportunities(),
    fetchWebsites(),
    fetchLandingPages(),
  ]);

  return (
    <DashboardClient
      initialAnalytics={analytics}
      initialAgents={agents}
      initialContractors={contractors}
      initialNiches={niches}
      initialCities={cities}
      initialLeads={leads}
      initialOpportunities={opportunities}
      initialWebsites={websites}
      initialLandingPages={landingPages}
    />
  );
}
