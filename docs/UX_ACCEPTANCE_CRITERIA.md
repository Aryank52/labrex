# LABREX Frontend UX & Page Acceptance Criteria

**Document Version:** 1.0  
**Authority:** Master Directive Section 80  
**Standard:** No frontend page or component is considered complete until all criteria are verified.  

---

## 1. Global Verification Gate for All Pages

Every page in LABREX must pass the following 7 gates prior to sign-off:

1. **TypeScript Typecheck**: Zero TypeScript errors (`npm.cmd run typecheck` passes with `strict: true`).
2. **Production Build**: Zero build errors or warnings (`npm.cmd run build` generates optimized bundle).
3. **Console Cleanliness**: Zero JavaScript exceptions, unhandled Promise rejections, or React hydration warnings in browser console.
4. **Browser Verification**: Tested in Chrome via Chrome DevTools MCP or `browser_subagent`.
5. **State Completeness**:
   - **Loading State**: Clean, non-layout-shifting skeleton loader.
   - **Error State**: User-friendly error card with retry button and machine-readable error code.
   - **Empty State**: Informative empty illustration and explanation when no records match filter.
6. **Responsive Layout**: Validated at Desktop (1440px), Tablet (1024px), and Mobile (390px).
7. **Accessibility (WCAG 2.1 AA)**:
   - Full keyboard navigability (visible focus rings on interactive elements).
   - ARIA labels on chart visualizers and icon buttons.
   - Contrast ratio $\ge 4.5:1$ on text elements.
   - High information density without overlapping cards.

---

## 2. Page-Specific Acceptance Criteria

| Page Route | Required Elements | Critical Acceptance Condition |
| :--- | :--- | :--- |
| **`/` (Overview)** | KPI cards, India Skill Gap summary, Top Shortages list, Radar ticker | First Contentful Paint < 1.2s; clicking any shortage card deep-links to district detail. |
| **`/map` (India Skill Map)** | MapLibre GeoJSON map, state/district boundaries, metric toggles | Smooth pan/zoom at 60fps; hovering over district displays tooltip with Demand & Supply Index. |
| **`/forecast` (Forecast Studio)**| Historical line chart, 80%/95% confidence bands, model comparison toggle | User can toggle between Seasonal Naive, LightGBM, and TimesFM with dynamic metric updates. |
| **`/radar` (LABREX Radar)** | Risk cards sorted by severity, filter by state/sector, early warning drivers | Critical shortage alerts clearly display root cause badges and confidence scores. |
| **`/scenarios` (Scenario Studio)**| Counterfactual slider controls, before-vs-after delta chart, clone button | Adjusting seat inputs recalculates net gap and estimated budget in < 500ms client-side. |
| **`/optimizer` (Optimizer UI)** | Budget input, constraint checkboxes, ranked intervention cards, Pareto plot | Submitting budget returns optimal solution or infeasibility explanation within 5 seconds. |
| **`/copilot` (AI Copilot)** | Chat drawer, suggested prompts, tool activity pills, verified evidence links | Copilot displays real-time execution steps (Analyzing -> Querying Data -> Ready); zero hallucinated numbers. |
| **`/lineage` (Data Lineage)** | Interactive DAG showing source -> batch -> feature -> model -> forecast | Clicking any node displays SHA-256 checksum, authority, ingest timestamp, and schema version. |
