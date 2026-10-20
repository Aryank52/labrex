# ADR-0006: Google OR-Tools for Constrained Policy Optimization

**Status:** APPROVED  
**Date:** 2026-10-20  
**Deciders:** Principal Engineering Agent  

---

## Context
A primary differentiator of LABREX is prescriptive capability: calculating the optimal allocation of new training seats and courses under fiscal budget constraints, training centre physical limits, and regional equity requirements. Relying on simple heuristic sorting or unconstrained greedy algorithms produces sub-optimal resource allocation and ignores combinatorial trade-offs.

## Decision
We integrate **Google OR-Tools** (using the CBC Mixed-Integer Programming solver and CP-SAT engine) in `services/optimization/`. 
The problem is mathematically formulated as an integer linear program that minimizes future weighted skill shortages subject to:
1. Total fiscal budget constraint.
2. Training centre physical intake limits.
3. Minimum viable class/cohort sizes.
4. Program launch binary decisions ($x \in \{0, 1\}$).
The solver has a strict timeout budget of 5.0 seconds and outputs ranked options, Pareto trade-offs, and sensitivity indicators.

## Consequences
### Positive
- Mathematically proven optimal or bounded solutions.
- High performance (sub-second solve times for typical state/district candidate sets).
- Transparent, explainable constraint modeling without black-box guessing.

### Negative / Trade-offs
- Infeasible constraint sets must be detected gracefully with clear diagnostics explaining which constraints conflicted.
