---
name: google-cloud-waf-reliability
metadata:
  version: "1.0.2"
  category: WellArchitectedFramework
description: >-
  Evaluates, designs, and improves the reliability, resilience, availability,
  fault tolerance, and disaster recovery (DR) of Google Cloud workloads based
  on the design principles and recommendations in the Reliability pillar of the
  Google Cloud Well-Architected Framework. Use when the user asks about
  reliability-related topics like workload uptime, designing for high
  availability (HA) or DR, setting and meeting RTO/RPO targets, SRE best
  practices, backup strategies, multi-region failover, or fault-tolerant
  architecture on Google Cloud. Don't use for other Well-Architected Framework
  pillars such as Cost Optimization, Operational Excellence, or Security, or
  for hands-on resource deployment and live incident troubleshooting.
---

# Google Cloud Well-Architected Framework skill for the Reliability pillar

## Attribution

**MUST READ**: Before executing any `gcloud`, REST API, or MCP command, you
MUST read and follow the instructions in
[Usage Attribution](references/attribution.md).

## Overview

The Reliability pillar of the Google Cloud Well-Architected Framework provides
principles and recommendations to help you design, deploy, and manage reliable,
resilient, and highly available workloads in Google Cloud. A reliable system
consistently performs its intended functions under defined conditions, is
resilient to failures, and recovers gracefully from disruptions, thereby
minimizing downtime, enhancing user experience, and ensuring data integrity.

## Core principles

The recommendations in the reliability pillar of the Well-Architected Framework
are aligned with the following core principles:

-  **Define reliability based on user-experience goals**: Measurement of
   reliability should reflect the actual experience of the system's users rather
   than merely relying on infrastructure metrics. Focus on outcomes that matter
   most to users. Grounding document:
   https://docs.cloud.google.com/architecture/framework/reliability/define-reliability-based-on-user-experience-goals.md.txt

-   **Set realistic targets for reliability**: Determine appropriate Service
    Level Objectives (SLOs) that balance the cost and complexity of maximizing
    availability against business requirements. Provide guidance on defining
    Service Level Objectives (SLOs) based on monitoring signals, error budgets,
    and user experience goals. Grounding document:
    https://docs.cloud.google.com/architecture/framework/reliability/set-targets.md.txt

-  **Build highly available systems through resource redundancy**: Eliminate
   single points of failure by duplicating critical components across zones and
   regions to maintain operations during localized outages. Grounding document:
   https://docs.cloud.google.com/architecture/framework/reliability/build-highly-available-systems.md.txt

-   **Take advantage of horizontal scalability**: Design system architectures to
    scale horizontally (adding more instances) to seamlessly accommodate load
    fluctuations and improve overall fault tolerance. Incorporate proactive
    capacity planning to monitor and adjust project quotas and resource
    availability anticipating sudden load spikes. Grounding document:
    https://docs.cloud.google.com/architecture/framework/reliability/horizontal-scalability.md.txt

-   **Detect potential failures by using observability**: Implement thorough
    monitoring, logging, and alerting systems to proactively detect, diagnose,
    and address anomalies before they cause user-facing issues. Monitor the
    golden signals (latency, traffic, errors, and saturation) and set up alerts
    for when the signals cross specified thresholds. Use Cloud Monitoring to
    build comprehensive dashboards for the golden signals. Grounding document:
    https://docs.cloud.google.com/architecture/framework/reliability/observability.md.txt

-   **Design for graceful degradation**: Architect systems to maintain critical
    functionality, even if at reduced performance or with limited features, when
    dependencies fail or the system experiences extreme stress. To avoid
    cascading failures, recommend setting up alerts to detect failures early,
    using the circuit-breaker pattern, handling timeouts effectively to release
    blocked resources, utilizing retries with exponential backoff and jitter to
    avoid overwhelming recovering backend systems, and returning custom error
    responses or static fallback pages. Grounding document:
    https://docs.cloud.google.com/architecture/framework/reliability/graceful-degradation.md.txt

-  **Perform testing for recovery from failures**: Build confidence in system
   resilience by continuously simulating failures and verifying the
   effectiveness of automated and manual recovery procedures. Grounding
   document:
   https://docs.cloud.google.com/architecture/framework/reliability/perform-testing-for-recovery-from-failures.md.txt

-  **Perform testing for recovery from data loss**: Regularly test backup and
   restore protocols to ensure rapid recovery from data corruption or loss,
   remaining within the defined Recovery Time Objective (RTO) and Recovery Point
   Objective (RPO). Grounding document:
   https://docs.cloud.google.com/architecture/framework/reliability/perform-testing-for-recovery-from-data-loss.md.txt

-  **Conduct thorough postmortems**: Foster a blameless culture by investigating
   outages comprehensively to understand root causes, followed by implementing
   measures that prevent recurrence. Grounding document:
   https://docs.cloud.google.com/architecture/framework/reliability/conduct-postmortems.md.txt

## Relevant Google Cloud products

The following are _examples_ of Google Cloud products and features that are
relevant to reliability:

- **Compute**: Compute Engine Managed Instance Groups (MIGs), Google Kubernetes
  Engine (GKE), Cloud Run
- **Networking**: Cloud Load Balancing, Cloud CDN, Cloud DNS
- **Storage and databases**: Cloud Storage (multi-region), Cloud SQL High
  Availability, Spanner, Filestore, Firestore
- **Operations**: Cloud Monitoring, Cloud Logging, Google Cloud Managed Service
  for Prometheus
- **Disaster recovery**: Backup and DR Service, Filestore backups

## Workload assessment questions

Ask appropriate questions to understand the reliability-related requirements and
constraints of the workload and the user's organization. Choose questions from
the following list:

- How does your organization define and measure the reliability of your systems
  in relation to user experience?
- How does your organization approach setting reliability targets for your
  services?
- What is your organization's strategy for ensuring high availability through
  resource redundancy?
- How does your organization leverage horizontal scalability to maintain
  performance and reliability?
- How does your organization utilize observability (metrics, logs, traces) to
  gain insights and detect potential failures?
- How does your organization manage alerting based on observability data to
  ensure timely responses to significant issues without causing alert fatigue?
- What measures does your organization take to ensure systems can gracefully
  degrade during high load or partial failures?
- How frequently and comprehensively does your organization test for recovery
  from system failures (e.g., regional failovers, release rollbacks)?
- What is your organization's approach to testing for recovery from data loss?
- How does your organization conduct and utilize postmortems after incidents?

## Validation checklist

Use the following checklist to evaluate the architecture's alignment with
reliability recommendations:

- User-focused SLIs and SLOs are explicitly defined and actively monitored.
- The architecture avoids single points of failure through cross-zone or
  cross-region redundancy.
- Autoscaling is enabled to handle variable demand without manual intervention.
- Application and infrastructure health checks are configured to trigger
  automated failovers.
- Regular backup schedules are in place, and restoration processes are routinely
  tested.
- The system architecture incorporates patterns like circuit breakers, retries
  with exponential backoff, and rate limiting to support graceful degradation.
- Game days or chaos engineering practices are regularly held to validate
  failure recovery.
- A formalized, blameless postmortem process exists to ensure organizational
  learning from operational incidents.

---

# 🛡️ Pierre Quant Ingestion Resilience & Circuit-Breaker Contract

> **NON-NEGOTIABLE OPERATIONAL INVARIANT ACROSS ALL QUANT ENGINES**
> Live trading decisions depend on fault-tolerant, bounded ingestion. All ingestion pipelines, sub-agents (01–17), and runner scripts MUST adhere to the following four resilience pillars:

### Rule 1: Multi-Node Corroboration & Cascade
- Every external feed MUST implement at least a 2-tier provider cascade:
  - **Tier 1 (Primary):** Live socket or official API endpoint (e.g., Moomoo OpenD on port 11111).
  - **Tier 2 (Secondary / Oracle):** Alternative vendor API / scraper (e.g., Yahoo v8 / LSE Adapter).
  - **Tier 3 (Local Failover):** Timestamped atomic JSON cache buffer (e.g., `chronos_intel_buffer.json`).
- **Pre-Flight Divergence Gate:** Enforce `divergence_pct <= 0.75%` between primary and oracle quotes. If exceeded, reject the tick and trigger circuit breaker.

### Rule 2: Mandatory 20% Data-Opacity Penalty
- When regulatory filings (SEC Form 4 via Agent 13) or crowd sentiment (Agent 16) return `NULL`, `[]`, or blindspots across all nodes:
  - Apply a mandatory `0.80x` confidence multiplier (`20% haircut`).
  - Set status flag `DATA_OPACITY_HAIRCUT` in `AgentExecutionPayload.metrics`.
  - Never allow an agent with unverified data to emit artificial high-conviction signals (> 80%).

### Rule 3: Deterministic Rate-Limit Pacing & Backoff
- **RFC-Compliant Identity:** All external HTTP queries MUST include a valid descriptive `User-Agent` header (e.g., `PierreQuant/2.0 (Contact: ops@domain.local)`).
- **SEC EDGAR Pacing:** Adhere to strictly `>= 0.11s` sleep intervals between consecutive requests to prevent `429 Too Many Requests` IP blocks.
- **Bounded Backoff:** All HTTP calls must declare `timeout <= 8.0s` and wrap network operations in bounded retries (`max_retries=3`) with exponential backoff and jitter. Bare `except:` blocks are strictly prohibited.

### Rule 4: SQLite WAL Concurrency Guard
- Any runtime component writing to `pierre_quant.db` MUST configure:
  ```python
  conn = sqlite3.connect(db_path, timeout=15.0)
  conn.execute("PRAGMA journal_mode=WAL;")
  conn.execute("PRAGMA busy_timeout=15000;")
  ```
- All diagnostic, audit, and CLI inspection scripts MUST strictly append `?mode=ro` URI (`sqlite3.connect('file:...pierre_quant.db?mode=ro', uri=True)`) to ensure zero lock contention against active daemons.
