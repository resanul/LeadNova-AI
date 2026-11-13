"use client";

import React, { useState } from "react";
import { Mail, MessageSquare, PhoneCall, Copy, Check, X, Sparkles } from "lucide-react";

interface OutreachModalProps {
  contractor: any;
  onClose: () => void;
}

export default function OutreachModal({ contractor, onClose }: OutreachModalProps) {
  const [activeTab, setActiveTab] = useState<"email" | "sms" | "call">("email");
  const [pitchData, setPitchData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState<string | null>(null);

  React.useEffect(() => {
    if (contractor) {
      setLoading(true);
      fetch(`http://localhost:8000/api/v1/contractors/${contractor.id}/generate-pitch`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      })
        .then((res) => res.json())
        .then((data) => setPitchData(data))
        .catch(() => {})
        .finally(() => setLoading(false));
    }
  }, [contractor]);

  const copyToClipboard = (text: string, type: string) => {
    navigator.clipboard.writeText(text);
    setCopied(type);
    setTimeout(() => setCopied(null), 2000);
  };

  if (!contractor) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4 backdrop-blur-sm">
      <div className="relative w-full max-w-2xl rounded-2xl border border-slate-700 bg-[#0e1628] p-6 shadow-2xl space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <Sparkles className="h-4 w-4 text-blue-400" />
              <h3 className="text-lg font-bold text-white">Antigravity B2B Outreach Pitch</h3>
            </div>
            <p className="text-xs text-slate-400">
              Contractor: <span className="font-semibold text-slate-200">{contractor.business_name}</span> ({contractor.city}, {contractor.state})
            </p>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-800 hover:text-white transition"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Tab Selection */}
        <div className="flex space-x-2 border-b border-slate-800 pb-2">
          <button
            onClick={() => setActiveTab("email")}
            className={`flex items-center space-x-2 rounded-lg px-4 py-2 text-xs font-semibold transition ${
              activeTab === "email"
                ? "bg-blue-600 text-white"
                : "text-slate-400 hover:bg-slate-800 hover:text-white"
            }`}
          >
            <Mail className="h-4 w-4" />
            <span>Cold Email Pitch</span>
          </button>
          <button
            onClick={() => setActiveTab("sms")}
            className={`flex items-center space-x-2 rounded-lg px-4 py-2 text-xs font-semibold transition ${
              activeTab === "sms"
                ? "bg-blue-600 text-white"
                : "text-slate-400 hover:bg-slate-800 hover:text-white"
            }`}
          >
            <MessageSquare className="h-4 w-4" />
            <span>Direct SMS Pitch</span>
          </button>
          <button
            onClick={() => setActiveTab("call")}
            className={`flex items-center space-x-2 rounded-lg px-4 py-2 text-xs font-semibold transition ${
              activeTab === "call"
                ? "bg-blue-600 text-white"
                : "text-slate-400 hover:bg-slate-800 hover:text-white"
            }`}
          >
            <PhoneCall className="h-4 w-4" />
            <span>60-Sec Call Script</span>
          </button>
        </div>

        {/* Tab Content */}
        {loading ? (
          <div className="py-12 text-center text-xs text-slate-400">
            Generating customized partnership pitch using Antigravity AI Engine...
          </div>
        ) : pitchData ? (
          <div className="space-y-4">
            {activeTab === "email" && (
              <div className="space-y-3">
                <div className="flex items-center justify-between rounded-lg bg-slate-900/80 px-3 py-2 text-xs border border-slate-800">
                  <span className="text-slate-400">Subject: <span className="text-slate-200 font-medium">{pitchData.cold_email.subject}</span></span>
                  <button
                    onClick={() => copyToClipboard(pitchData.cold_email.subject, "subject")}
                    className="flex items-center space-x-1 text-blue-400 hover:text-blue-300"
                  >
                    {copied === "subject" ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                    <span>{copied === "subject" ? "Copied" : "Copy"}</span>
                  </button>
                </div>
                <div className="relative">
                  <pre className="max-h-60 overflow-y-auto whitespace-pre-wrap rounded-xl border border-slate-800 bg-slate-900/90 p-4 text-xs font-mono text-slate-300">
                    {pitchData.cold_email.body}
                  </pre>
                  <button
                    onClick={() => copyToClipboard(pitchData.cold_email.body, "email_body")}
                    className="absolute top-3 right-3 flex items-center space-x-1.5 rounded-lg bg-blue-600/20 px-3 py-1.5 text-xs font-semibold text-blue-400 border border-blue-500/30 hover:bg-blue-600/30 transition"
                  >
                    {copied === "email_body" ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                    <span>{copied === "email_body" ? "Copied" : "Copy Full Email"}</span>
                  </button>
                </div>
              </div>
            )}

            {activeTab === "sms" && (
              <div className="space-y-3">
                <div className="relative rounded-xl border border-slate-800 bg-slate-900/90 p-4 text-sm text-slate-200 leading-relaxed">
                  {pitchData.sms_pitch}
                  <div className="mt-4 pt-3 flex justify-end border-t border-slate-800">
                    <button
                      onClick={() => copyToClipboard(pitchData.sms_pitch, "sms")}
                      className="flex items-center space-x-1.5 rounded-lg bg-blue-600 px-3.5 py-1.5 text-xs font-semibold text-white shadow hover:bg-blue-500 transition"
                    >
                      {copied === "sms" ? <Check className="h-3.5 w-3.5 text-white" /> : <Copy className="h-3.5 w-3.5" />}
                      <span>{copied === "sms" ? "Copied SMS" : "Copy SMS Pitch"}</span>
                    </button>
                  </div>
                </div>
              </div>
            )}

            {activeTab === "call" && (
              <div className="space-y-3">
                <div className="relative">
                  <pre className="max-h-60 overflow-y-auto whitespace-pre-wrap rounded-xl border border-slate-800 bg-slate-900/90 p-4 text-xs font-mono text-slate-300">
                    {pitchData.cold_call_script}
                  </pre>
                  <button
                    onClick={() => copyToClipboard(pitchData.cold_call_script, "call_script")}
                    className="absolute top-3 right-3 flex items-center space-x-1.5 rounded-lg bg-blue-600 px-3 py-1.5 text-xs font-semibold text-white shadow hover:bg-blue-500 transition"
                  >
                    {copied === "call_script" ? <Check className="h-3.5 w-3.5 text-white" /> : <Copy className="h-3.5 w-3.5" />}
                    <span>{copied === "call_script" ? "Copied Script" : "Copy Call Script"}</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="py-8 text-center text-xs text-red-400">Failed to load pitch data.</div>
        )}

        {/* Footer */}
        <div className="flex justify-end pt-2 border-t border-slate-800">
          <button
            onClick={onClose}
            className="rounded-xl border border-slate-700 bg-slate-800 px-4 py-2 text-xs font-semibold text-slate-300 hover:bg-slate-700 transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
