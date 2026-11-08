---
name: agent-gateway-security
description: Enforces strict blast-radius containment, immutable subsystem boundaries, and mandatory read-only SQLite URI modes across the Pierre Quant multi-agent architecture.
metadata:
  version: "1.0.0"
  category: SystemReliabilityAndSecurity
---

# 🛡️ Agent Gateway Security & Blast-Radius Containment

## Overview
The `agent-gateway-security` skill governs all agent file access, process execution, and database queries within the Pierre Quant platform. It guarantees that live trading swarms, spatial HUD interfaces, daemon configurations, and production ledgers remain completely isolated from accidental writes, mutations, or lock contentions.

---

## 🔒 1. Protected Subsystems & Zero-Touch Zones

Before executing any file write, deletion, refactoring, or database query tool call, the agent MUST evaluate the target path against the following **Zero-Touch Subsystems**:

| Subsystem | File System Path Pattern | Allowed Operations | Forbidden Operations |
| :--- | :--- | :--- | :--- |
| **OpenClaw Swarm & Daemons** | `C:\Users\Pierre\.openclaw\**` | Read-Only inspection (bounded) | `write_to_file`, `replace_file_content`, schema migrations, daemon restarts |
| **Julie Core Spatial HUD** | `C:\Users\Pierre\.openclaw\workspace\Julie-Core\**`, `app_eel.py` | Read-Only inspection | Frontend refactoring, socket port alteration, process killing |
| **War Room Production Dashboard** | `C:\Users\Pierre\Desktop\pierre_stock_warroom\**` | Version-controlled audited edits | Unverified writes, asset deletions, port reassignment |
| **Persistence Database** | `pierre_quant.db`, `state.db` | Read-Only via `?mode=ro` URI | Direct writes, `CREATE TABLE`, `DROP`, `UPDATE`, un-parameterized queries |
| **Telemetry & Intel Buffers** | `chronos_intel_buffer.json`, `hud_telemetry_buffer.json` | Read-Only inspection (bounded) | Truncation, manual key deletion |

---

## 🛑 2. Mandatory Read-Only SQLite Enforcement (`?mode=ro`)

Whenever an agent or diagnostic script connects to `pierre_quant.db`, it MUST enforce SQLite URI mode with `?mode=ro`:

### Standard Python Invariant:
```python
import sqlite3

# MANDATORY: Always use file URI with ?mode=ro and uri=True
db_path = r'file:C:\Users\Pierre\.openclaw\workspace\pierre-quant\pierre_quant.db?mode=ro'
conn = sqlite3.connect(db_path, uri=True)
try:
    cursor = conn.cursor()
    # Read-only query execution
    res = cursor.execute("SELECT ...").fetchall()
finally:
    conn.close()
```

### Safety Rationale:
- Connecting without `mode=ro` attempts to acquire a shared or reserved lock in WAL mode, which can block live daemon checkpointing (`WAL` -> `DB`) and cause `database is locked` panics in Agent 01/Supervisor.
- With `?mode=ro`, SQLite guarantees that no transaction journal or write locks are ever requested from the OS kernel.

---

## 🚦 3. Pre-Flight Boundary Verification Protocol

Before invoking any file write or replacement tool (`write_to_file`, `replace_file_content`, `multi_replace_file_content`):

1. **Path Boundary Check:**
   - Verify `TargetFile` is inside the designated project scope (`C:\Anti-Gravity-Core\` or explicitly authorized feature repositories).
   - If `TargetFile` matches `C:\Users\Pierre\.openclaw\`: **ABORT IMMEDIATELY.**
2. **Database Query Check:**
   - If running a database inspection command via `run_command`, confirm the connection string contains `?mode=ro` and `uri=True`.
3. **Daemon Safety Check:**
   - Never kill or restart background processes listening on ports `11111` (Moomoo OpenD), `8080` (Julie Core HUD), `3888` (War Room Gateway), or `11434` (Ollama Local).

---

## 4. Verification Check Script

To verify that a database connection is provably read-only:
```python
import sqlite3

def verify_readonly_connection(db_uri: str) -> bool:
    try:
        conn = sqlite3.connect(db_uri, uri=True)
        # Attempt a dry write to prove write-protection
        try:
            conn.execute("CREATE TABLE _sec_test (id INT);")
            conn.close()
            return False  # Failed: write succeeded on a protected database!
        except sqlite3.OperationalError:
            conn.close()
            return True   # Passed: write was strictly blocked by SQLite engine
    except Exception as e:
        return False
```
