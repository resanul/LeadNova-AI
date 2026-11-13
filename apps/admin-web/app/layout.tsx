import "./globals.css";
import React from "react";

export const metadata = {
  title: "GlobalLead AI - Autonomous Lead Gen & Business OS",
  description: "Enterprise Autonomous Pay-Per-Lead and Local Service Arbitrage Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#070b14] text-slate-100 antialiased selection:bg-blue-600 selection:text-white">
        {children}
      </body>
    </html>
  );
}
