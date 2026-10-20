# LABREX UI/UX Design System Brief

**Document Version:** 1.0  
**Design Standard:** National Intelligence & Decision-Support Platform  
**Target:** Clean, Restrained, High Data Density, Accessible  

---

## 1. Visual Philosophy & Design Directives

LABREX is an enterprise-grade policy intelligence system used by senior government administrators and data analysts.
- **NO Generic SaaS Aesthetics**: Avoid purple glow, trendy frosted glassmorphism that obscures text, floating neon gradients, and decorative 3D models.
- **High Information Density**: Present structured data cleanly with compact typography, tight tabular grids, and scannable visual cues.
- **Data-Driven Visuals**: Animations are functional (indicating loading, calculation, or state changes), never purely decorative.
- **Color Independence**: Status, risk, and critical warnings must never rely solely on color. Always pair colors with clear textual badges, icons, and numerical ratings.

---

## 2. Curated Color Palette & Tokens

The color palette is engineered for prolonged analytical work with high contrast ratios exceeding WCAG AA (minimum 4.5:1 for normal text):

| Token Name | Hex Code / HSL | Usage & Intent |
| :--- | :--- | :--- |
| **`bg-canvas`** | `#0B0F17` (Dark) / `#F8FAFC` (Light) | Base application background |
| **`bg-card`** | `#111827` (Dark) / `#FFFFFF` (Light) | Card and container panels |
| **`border-subtle`** | `#1F2937` (Dark) / `#E2E8F0` (Light) | Data grid dividers and card borders |
| **`text-primary`** | `#F9FAFB` (Dark) / `#0F172A` (Light) | Headings, primary metrics, active values |
| **`text-secondary`**| `#9CA3AF` (Dark) / `#475569` (Light) | Labels, metadata, axis text, subtitles |
| **`brand-accent`** | `#2563EB` (Royal Blue) | Primary interactive actions, active tabs |
| **`risk-critical`** | `#DC2626` (Crimson) | Severe shortage, urgent intervention needed |
| **`risk-high`** | `#EA580C` (Deep Orange) | Significant deficit, high momentum |
| **`risk-emerging`**| `#D97706` (Amber) | Early acceleration, supply stagnation |
| **`risk-watch`** | `#CA8A04` (Warm Gold) | Moderate shortage, monitor |
| **`risk-normal`** | `#16A34A` (Emerald) | Balanced labour equilibrium |
| **`risk-oversupply`**| `#0284C7` (Cyan Blue) | Training surplus exceeding demand |

---

## 3. Typography & Hierarchy

- **Primary Font Family**: `Inter`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, sans-serif.
- **Tabular & Code Font Family**: `JetBrains Mono`, `Fira Code`, monospace for numerical tables, codes (NCO, NSQF), and confidence intervals.
- **Hierarchy Scale**:
  - `Display / KPI`: 32px / 1.2 line-height / SemiBold (e.g. Demand Index, Net Gap).
  - `H1 / Page Title`: 22px / 1.3 line-height / SemiBold.
  - `H2 / Section Title`: 16px / 1.4 line-height / Medium.
  - `Body / Data Table`: 13px / 1.5 line-height / Regular.
  - `Caption / Badge`: 11px / 1.4 line-height / Medium.

---

## 4. Layout Structure & Navigation

```
+--------------------------------------------------------------------------------------------------+
| LABREX TOPBAR: System Title | National Scope | Active Quarter | Notifications | Copilot Toggle   |
+-----------+--------------------------------------------------------------------------------------+
| SIDEBAR   | MAIN WORKSPACE CANVAS                                                                |
|           |                                                                                      |
| • Overview| [KPI Row: Demand Index | Supply Index | Net Deficit | Radar Alert Count | Conf %]   |
| • SkillMap|--------------------------------------------------------------------------------------|
| • Demand  | [Primary Workspace View: MapLibre Interactive Map / ECharts Time-Series Grid]        |
| • Supply  |                                                                                      |
| • Forecast|--------------------------------------------------------------------------------------|
| • Gaps    | [Detail Panel / Data Table: Occupations, NSQF Levels, District Metrics, Interventions]|
| • Radar   |                                                                                      |
| • Scenario|                                                                                      |
| • Optimize|                                                                                      |
| • Copilot |                                                                                      |
| • Admin   |                                                                                      |
+-----------+--------------------------------------------------------------------------------------+
```

---

## 5. Responsive Behavior

- **Desktop (>= 1280px)**: Multi-column analytical workspace. Interactive map and drill-down panels side-by-side.
- **Tablet (768px – 1279px)**: Stacked view with collapsible inspector panel and responsive charts.
- **Mobile (< 768px)**: Streamlined executive intelligence mode displaying key indicators, critical radar alerts, and summary tables. Heavy spatial map tools recommend desktop view.
