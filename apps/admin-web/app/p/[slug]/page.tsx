import React from "react";
import {
  PhoneCall,
  ShieldCheck,
  Clock,
  MapPin,
  CheckCircle,
  Award,
  Zap,
  ArrowRight,
  HelpCircle,
} from "lucide-react";
import LeadCaptureForm from "./LeadCaptureForm";

export const revalidate = 0;

async function getLandingPageData(slug: string) {
  try {
    const res = await fetch(`http://localhost:8000/api/v1/landing-pages/${slug}/preview`, {
      cache: "no-store",
    });
    if (res.ok) {
      return await res.json();
    }
  } catch (err) {
    // Fallback if backend is restarting
  }

  // Fallback defaults for Fort Wayne Water Damage
  return {
    slug: "fort-wayne-water-damage-restoration",
    seo_title: "Water Damage Restoration in Fort Wayne, IN | 24/7 Rapid Dispatch",
    seo_description: "Urgent water damage mitigation in Fort Wayne. Connect with local licensed specialists immediately.",
    headline: "Emergency Water Damage Restoration in Fort Wayne",
    tracking_phone: "+12605550188",
    click_to_call_href: "tel:+12605550188",
    city_name: "Fort Wayne",
    niche_name: "Water Damage Restoration",
    schema_org: {
      "@context": "https://schema.org",
      "@type": "HomeAndConstructionBusiness",
      "name": "Fort Wayne Water Damage Restoration Network",
      "telephone": "+12605550188",
      "areaServed": "Fort Wayne",
    },
  };
}

// Fetch active city and niche IDs from backend to pass to the form
async function getCityAndNiche() {
  try {
    const [citiesRes, nichesRes] = await Promise.all([
      fetch("http://localhost:8000/api/v1/cities", { cache: "no-store" }),
      fetch("http://localhost:8000/api/v1/niches", { cache: "no-store" }),
    ]);
    if (citiesRes.ok && nichesRes.ok) {
      const cities = await citiesRes.json();
      const niches = await nichesRes.json();
      const city = cities[0] || { id: "default_city", name: "Fort Wayne" };
      const niche = niches.find((n: any) => n.slug === "water-damage-restoration") || niches[0];
      return { cityId: city.id, nicheId: niche.id, cityName: city.name, nicheName: niche.name };
    }
  } catch (err) {}
  return {
    cityId: "default_city",
    nicheId: "default_niche",
    cityName: "Fort Wayne",
    nicheName: "Water Damage Restoration",
  };
}

export default async function PublicLandingPage({
  params,
}: {
  params: { slug: string };
}) {
  const pageData = await getLandingPageData(params.slug);
  const context = await getCityAndNiche();

  const trackingPhone = pageData.tracking_phone || "+12605550188";
  const cityName = context.cityName || "Fort Wayne";
  const nicheName = context.nicheName || "Water Damage Restoration";

  return (
    <div className="min-h-screen bg-[#060a14] text-slate-100 selection:bg-blue-600 selection:text-white">
      {/* Schema.org JSON-LD Script for Search Engines */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(pageData.schema_org) }}
      />

      {/* Top Floating Emergency Bar */}
      <div className="sticky top-0 z-50 flex items-center justify-between border-b border-blue-500/30 bg-[#0a1224]/95 px-4 md:px-8 py-3 backdrop-blur-md">
        <div className="flex items-center space-x-2">
          <span className="flex h-3 w-3 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
          </span>
          <span className="text-xs md:text-sm font-semibold tracking-wide text-white">
            {cityName} EMERGENCY HOTLINE ACTIVE
          </span>
        </div>
        <a
          href={`tel:${trackingPhone}`}
          className="flex items-center space-x-2 rounded-full bg-emerald-600 px-4 py-1.5 text-xs md:text-sm font-bold text-white shadow-lg shadow-emerald-500/30 hover:bg-emerald-500 transition"
        >
          <PhoneCall className="h-4 w-4 animate-bounce" />
          <span>CALL {trackingPhone}</span>
        </a>
      </div>

      {/* Hero Section */}
      <section className="relative overflow-hidden px-4 md:px-8 py-12 md:py-20 lg:py-24 max-w-6xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
          {/* Left Column: Headline and Value Props */}
          <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
            <div className="inline-flex items-center space-x-2 rounded-full bg-blue-500/10 border border-blue-500/20 px-3.5 py-1 text-xs font-semibold text-blue-400">
              <MapPin className="h-3.5 w-3.5" />
              <span>Serving All Neighborhoods in {cityName} & Surrounding Areas</span>
            </div>

            <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold tracking-tight text-white leading-tight">
              Emergency <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">{nicheName}</span> in {cityName}
            </h1>

            <p className="text-base sm:text-lg text-slate-300 max-w-xl mx-auto lg:mx-0">
              Immediate on-site response for residential and commercial properties. Licensed, certified local specialists equipped to stop damage, extract water, and restore your property fast.
            </p>

            {/* Direct Call Button */}
            <div className="pt-2 flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4">
              <a
                href={`tel:${trackingPhone}`}
                className="w-full sm:w-auto flex items-center justify-center space-x-3 rounded-2xl bg-gradient-to-r from-emerald-600 to-teal-600 px-8 py-4 text-base font-extrabold text-white shadow-xl shadow-emerald-500/25 hover:from-emerald-500 hover:to-teal-500 transition scale-100 hover:scale-105"
              >
                <PhoneCall className="h-5 w-5" />
                <span>Call Now: {trackingPhone}</span>
              </a>
              <span className="text-xs text-slate-400 font-medium">
                ⚡ 24/7 Live Operator Available
              </span>
            </div>

            {/* Trust Badges */}
            <div className="pt-6 grid grid-cols-3 gap-3 border-t border-slate-800 text-left">
              <div className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4 text-emerald-400 shrink-0" />
                <span className="text-xs font-medium text-slate-300">Licensed & Insured</span>
              </div>
              <div className="flex items-center space-x-2">
                <Clock className="h-4 w-4 text-blue-400 shrink-0" />
                <span className="text-xs font-medium text-slate-300">45-Min Arrival</span>
              </div>
              <div className="flex items-center space-x-2">
                <Award className="h-4 w-4 text-amber-400 shrink-0" />
                <span className="text-xs font-medium text-slate-300">Free Estimates</span>
              </div>
            </div>
          </div>

          {/* Right Column: Lead Form */}
          <div className="lg:col-span-5">
            <LeadCaptureForm
              cityId={context.cityId}
              nicheId={context.nicheId}
              trackingPhone={trackingPhone}
              cityName={cityName}
              nicheName={nicheName}
            />
          </div>
        </div>
      </section>

      {/* 4-Step Process Section */}
      <section className="border-t border-slate-800/80 bg-[#090e1c] py-16 px-4 md:px-8">
        <div className="max-w-6xl mx-auto space-y-10">
          <div className="text-center space-y-2">
            <h2 className="text-2xl md:text-3xl font-bold text-white">How Our Rapid Response Network Works</h2>
            <p className="text-sm text-slate-400">Streamlined emergency service delivery from the first call to complete restoration.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 space-y-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600/20 text-blue-400 font-bold">1</div>
              <h3 className="text-base font-semibold text-white">Call or Submit Inquiry</h3>
              <p className="text-xs text-slate-400">Call our 24/7 hotline or fill out the emergency form with your location in {cityName}.</p>
            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 space-y-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-600/20 text-indigo-400 font-bold">2</div>
              <h3 className="text-base font-semibold text-white">Instant Specialist Match</h3>
              <p className="text-xs text-slate-400">We immediately route your request to the closest on-duty licensed specialist.</p>
            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 space-y-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-600/20 text-purple-400 font-bold">3</div>
              <h3 className="text-base font-semibold text-white">Rapid On-Site Arrival</h3>
              <p className="text-xs text-slate-400">A verified technician arrives on-site equipped with commercial diagnostic gear.</p>
            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 space-y-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-600/20 text-emerald-400 font-bold">4</div>
              <h3 className="text-base font-semibold text-white">Complete Restoration</h3>
              <p className="text-xs text-slate-400">Upfront quote, comprehensive mitigation, and direct insurance billing assistance.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Local FAQ Section */}
      <section className="py-16 px-4 md:px-8 max-w-4xl mx-auto space-y-8">
        <div className="text-center space-y-2">
          <h2 className="text-2xl md:text-3xl font-bold text-white">Frequently Asked Questions in {cityName}</h2>
          <p className="text-sm text-slate-400">Everything you need to know about emergency service calls and dispatch.</p>
        </div>

        <div className="space-y-4">
          <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5 space-y-2">
            <h4 className="text-sm font-semibold text-white flex items-center space-x-2">
              <HelpCircle className="h-4 w-4 text-blue-400 shrink-0" />
              <span>How quickly will a technician arrive at my property in {cityName}?</span>
            </h4>
            <p className="text-xs text-slate-400 pl-6">
              In most emergency cases within {cityName} city limits, on-call partner crews arrive within 45 to 90 minutes. High storm volume may affect exact arrival times.
            </p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5 space-y-2">
            <h4 className="text-sm font-semibold text-white flex items-center space-x-2">
              <HelpCircle className="h-4 w-4 text-blue-400 shrink-0" />
              <span>Does homeowners insurance cover emergency water damage?</span>
            </h4>
            <p className="text-xs text-slate-400 pl-6">
              Sudden and accidental water discharge (such as frozen burst pipes, water heater failure, or appliance overflows) is typically covered by standard homeowners insurance policies. Our partners assist with full photographic documentation.
            </p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-5 space-y-2">
            <h4 className="text-sm font-semibold text-white flex items-center space-x-2">
              <HelpCircle className="h-4 w-4 text-blue-400 shrink-0" />
              <span>Are there upfront fees for calling the dispatch number?</span>
            </h4>
            <p className="text-xs text-slate-400 pl-6">
              No. Calling our tracking hotline and speaking with our local dispatch team is 100% free. Any repair costs are quoted upfront by the licensed contractor before work begins.
            </p>
          </div>
        </div>
      </section>

      {/* Footer / Legal Compliance Disclosure */}
      <footer className="border-t border-slate-800 bg-[#040810] py-8 px-4 text-center text-xs text-slate-500 space-y-2">
        <p>© 2026 {cityName} Emergency Contractor Network • All Rights Reserved.</p>
        <p className="max-w-2xl mx-auto text-[11px] text-slate-600">
          Disclaimer: This website acts as an independent referral and lead dispatch service connecting consumers with licensed, local independent contractors. All contractors are independent business entities, and this platform does not guarantee work or warrant contractor licenses directly.
        </p>
      </footer>
    </div>
  );
}
