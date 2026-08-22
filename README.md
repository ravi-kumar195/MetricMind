# 📈 MetricWatcher AI — Automated Business Anomaly Detection & Executive Alert System

An end-to-end Python automated pipeline that monitors daily business KPIs, identifies statistical anomalies using rolling baselines, generates executive narrative summaries using **Google Gemini LLM**, and dispatches responsive HTML email alerts to stakeholders via SMTP.

---

## 💡 Overview

Modern teams often miss critical metric shifts due to noisy dashboards and alert fatigue. **MetricWatcher AI** solves this by establishing a automated 3-stage pipeline:

1. **Statistical Anomaly Engine**: Calculates 7-day rolling baselines, percentage variance, and statistical thresholds to detect true metric deviations (Revenue drops, conversion spikes, system outages).
2. **AI Narrative Translation**: Sends raw anomaly tables to **Google Gemini** to synthesize complex data points into concise, action-oriented executive summaries.
3. **Automated HTML Alert Dispatcher**: Renders conditionally styled HTML email reports with visual urgency indicators and dispatches them via secure TLS SMTP.
4. **Audit Trail Logging**: Maintains a persistent local JSON record (`alert_history.json`) for observability and tracking.

---

## 🛠️ Architecture & Workflow

```text
  ┌───────────────────────┐
  │  Excel / CSV Ingestion│
  └───────────┬───────────┘
              │
              ▼
  ┌───────────────────────┐
  │ Math & Baseline Engine│  <-- 7-Day Rolling Averages, % Shift Calculation,
  └───────────┬───────────┘      Anomaly Circuit Breaker
              │
              ▼
  ┌───────────────────────┐
  │  Gemini AI Synthesis  │  <-- Natural Language Executive Summaries
  └───────────┬───────────┘
              │
              ▼
  ┌───────────────────────┐
  │ HTML Email Dispatcher │  <-- Conditional Styling, Dynamic Tables,
  └───────────┬───────────┘      SMTP TLS Connection
              │
              ▼
  ┌───────────────────────┐
  │ Local Audit Log (JSON)│  <-- History Tracking & Record Keeping
  └───────────────────────┘