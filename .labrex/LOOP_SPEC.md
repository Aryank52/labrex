# LABREX Autonomous Engineering Loop Specification

**Document Version:** 1.0  
**Authority:** Master Directive Section 4, 91 & 100  

---

## 1. Loop Philosophy & Core Cycle

The engineering workflow for LABREX operates as a persistent, resumable loop:

```
  DISCOVER
     │
     ▼
   READ
     │
     ▼
   PLAN
     │
     ▼
 IMPLEMENT
     │
     ▼
    RUN
     │
     ▼
   TEST
     │
     ▼
  OBSERVE
     │
     ▼
  DIAGNOSE
     │
     ▼
    FIX
     │
     ▼
   RETEST
     │
     ▼
   VERIFY
     │
     ▼
   REVIEW
     │
     ▼
  DOCUMENT
     │
     ▼
   COMMIT
     │
     ▼
  NEXT TASK
```

---

## 2. Persistent State Directory

All state across agent sessions is stored in `.labrex/`:
- `LOOP_STATE.md`: Active phase, active task, current loop iteration count, blocker status.
- `TASK_QUEUE.md`: Authoritative machine-readable queue with tasks, dependencies, acceptance criteria, and status.
- `ITERATION_LOG.md`: Chronological audit log of every loop iteration, actions taken, and test results.
- `BLOCKERS.md`: Documented blockers, reproduction steps, and required human intervention.
- `DECISIONS.md`: Log of technical trade-offs and minor decisions made during implementation.
- `MEMORY.md`: Runtime learnings, command patterns, and technical gotchas.

---

## 3. Failure Escalation Protocol

If a task encounters an execution or test failure:
1. **First Failure**: Investigate logs, trace error stack, check inputs and dependencies.
2. **Second Failure**: Isolate root cause with targeted minimal reproduction test.
3. **Third Failure**: Attempt alternate architectural implementation or fallback path.
4. **Repeated Failure**: Mark task `BLOCKED`, write a diagnostic entry in `.labrex/BLOCKERS.md`, and request human guidance. **Never repeat the same failing command endlessly.**

---

## 4. Task Stop & Phase Completion Conditions

- **Task Completion Gate**: A task can only transition from `IN_PROGRESS` to `VERIFIED` and `DONE` if:
  1. All acceptance criteria pass.
  2. Automated tests pass with zero regressions.
  3. Documentation is updated.
  4. Code changes pass security and secret inspection.
- **Phase Completion Gate**: A phase is marked `DONE` only when all constituent tasks are `DONE`, phase documentation is signed off, and regression tests pass.
