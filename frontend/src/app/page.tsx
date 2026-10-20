import React from "react";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col p-8 max-w-7xl mx-auto space-y-8">
      {/* Top Header */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-[#1F2937] pb-6">
        <div>
          <div className="flex items-center gap-3">
            <span className="bg-blue-600/20 text-blue-400 border border-blue-500/30 text-xs font-semibold px-2.5 py-1 rounded">
              DECISION-SUPPORT PLATFORM
            </span>
            <span className="text-xs text-neutral-400">National Scope (India) • NCO-2015</span>
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-white mt-2">
            LABREX Intelligence Platform
          </h1>
          <p className="text-sm text-neutral-400 mt-1">
            Labour Market Intelligence, Workforce Forecasting & Constrained Policy Optimization
          </p>
        </div>
        <div className="mt-4 md:mt-0 flex gap-3">
          <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            System Ready
          </span>
        </div>
      </header>

      {/* KPI Overview Grid */}
      <section className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-[#111827] border border-[#1F2937] rounded-lg p-5">
          <div className="text-xs font-medium text-neutral-400 uppercase tracking-wider">National Demand Index</div>
          <div className="text-3xl font-bold text-white mt-2 font-mono">74.2 <span className="text-xs text-neutral-400 font-normal">/ 100</span></div>
          <div className="text-xs text-emerald-400 mt-1 flex items-center gap-1">↑ +4.8% QoQ Momentum</div>
        </div>

        <div className="bg-[#111827] border border-[#1F2937] rounded-lg p-5">
          <div className="text-xs font-medium text-neutral-400 uppercase tracking-wider">National Supply Index</div>
          <div className="text-3xl font-bold text-white mt-2 font-mono">61.5 <span className="text-xs text-neutral-400 font-normal">/ 100</span></div>
          <div className="text-xs text-neutral-400 mt-1 flex items-center gap-1">Effective Training Pipeline</div>
        </div>

        <div className="bg-[#111827] border border-[#1F2937] rounded-lg p-5">
          <div className="text-xs font-medium text-neutral-400 uppercase tracking-wider">Critical Shortages (RADAR)</div>
          <div className="text-3xl font-bold text-red-400 mt-2 font-mono">14 <span className="text-xs text-neutral-400 font-normal">Clusters</span></div>
          <div className="text-xs text-red-400 mt-1">High Demand + Stagnant Capacity</div>
        </div>

        <div className="bg-[#111827] border border-[#1F2937] rounded-lg p-5">
          <div className="text-xs font-medium text-neutral-400 uppercase tracking-wider">Forecast Confidence</div>
          <div className="text-3xl font-bold text-blue-400 mt-2 font-mono">87.4%</div>
          <div className="text-xs text-neutral-400 mt-1">Walk-Forward Validated</div>
        </div>
      </section>

      {/* Primary Intelligence Pillars */}
      <section className="bg-[#111827] border border-[#1F2937] rounded-lg p-6">
        <h2 className="text-lg font-semibold text-white mb-4">Core Platform Capabilities</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="border border-[#1F2937] bg-[#0B0F17] p-4 rounded-md">
            <h3 className="text-sm font-semibold text-blue-400">1. India Skill Map</h3>
            <p className="text-xs text-neutral-300 mt-2 leading-relaxed">
              Spatial PostGIS exploration mapping Demand and Supply indices across India's 36 States and 700+ districts with granular drill-down.
            </p>
          </div>

          <div className="border border-[#1F2937] bg-[#0B0F17] p-4 rounded-md">
            <h3 className="text-sm font-semibold text-emerald-400">2. Forecast Studio</h3>
            <p className="text-xs text-neutral-300 mt-2 leading-relaxed">
              Champion-vs-Challenger walk-forward forecasting comparing Seasonal Naive, LightGBM, and TimesFM-3 with explicit prediction intervals.
            </p>
          </div>

          <div className="border border-[#1F2937] bg-[#0B0F17] p-4 rounded-md">
            <h3 className="text-sm font-semibold text-amber-400">3. Policy Optimizer</h3>
            <p className="text-xs text-neutral-300 mt-2 leading-relaxed">
              Google OR-Tools MILP solver calculating the optimal allocation of new training seats under fiscal and centre capacity constraints.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
