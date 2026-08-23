🧠 MetricMind

> **Automated Anomaly Detection & AI-Powered Executive Alerting Engine**

[![Daily MetricWatcher AI Execution](https://github.com/ravi-kumar195/MetricMind/actions/workflows/daily_watcher.yml/badge.svg)](https://github.com/ravi-kumar195/MetricMind/actions/workflows/daily_watcher.yml)
![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![Docker Ready](https://img.shields.io/badge/docker-ready-blue.svg?logo=docker)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**MetricMind** is an enterprise-grade operational watchdog engineered to solve alert fatigue and noisy dashboard monitoring. It continuously ingests business KPI datasets, computes 7-day rolling statistical baselines, isolates metric variances, translates raw anomaly tables into executive natural language summaries via the **Google Gemini API**, and delivers conditionally styled HTML alerts.

---

## 🌟 Key Features

- **📊 Statistical Anomaly Engine:** Calculates 7-day rolling averages, percentage shifts, and Z-score variances against historical baselines.
- **🤖 AI Narrative Translation:** Leverages Google Gemini LLM to convert raw tabular anomalies into concise, 3-sentence root-cause executive summaries.
- **⚡ Smart Circuit-Breaker:** Suppresses false positives and eliminates email spam by triggering dispatches only when significant anomalies breach defined thresholds.
- **📧 High-Impact HTML Reports:** Renders responsive, dark/light styled HTML email digest cards complete with metric variance tables and executive summaries.
- **🐳 Portable Docker Containerization:** Pre-packaged with `Dockerfile` and `docker-compose.yml` for isolated, reproducible execution across local or cloud environments.
- **⏰ Serverless Cloud Schedule:** Fully automated execution every morning at 08:00 UTC (1:30 PM IST) using GitHub Actions cron workflows with encrypted environment secrets.
- **📜 Persistent Audit Trail:** Maintains an automated `alert_history.json` log recording alert timestamps, metric counts, and system execution health.

---

## 🏗️ Architecture & Pipeline Flow

```text
┌──────────────────────┐     ┌────────────────────────┐     ┌────────────────────────┐
│  Daily Data Sources  │ ──> │   Pandas Engine        │ ──> │   Google Gemini LLM    │
│  (Excel / CSV Files) │     │ (Rolling Mean, Z-Score)│     │  (Executive Digest)    │
└──────────────────────┘     └────────────────────────┘     └────────────────────────┘
                                                                        │
┌──────────────────────┐     ┌────────────────────────┐                 ▼
│ Persistent Audit Log │ <── │  GitHub Actions /      │ <── ┌────────────────────────┐
│ (alert_history.json) │     │  Docker Container      │     │ HTML Email Dispatcher  │
└──────────────────────┘     └────────────────────────┘     │   (SMTP TLS Circuit)   │
                                                            └────────────────────────┘
```
