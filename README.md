# Observability Stack for a Containerized Service

> **End-to-end observability platform** for a containerized Flask application using Prometheus, Grafana, Loki, Promtail, Alertmanager, Node Exporter, and Slack.

---

## Project Overview

This project implements a production-grade observability platform that provides:

- **Metrics** — Request counts, latency (P95/P99), error rates, CPU and memory utilisation
- **Logs** — Centralised log aggregation with structured log levels
- **Dashboards** — Four purpose-built Grafana dashboards
- **Alerting** — Automated Slack notifications for high error rate, high latency, and application downtime

---

## Problem Statement

Without observability, container-based services suffer from:

- Errors going unnoticed until users report them
- Manual log inspection across multiple containers
- No early warning for performance degradation
- No automated incident notification

This stack solves these problems with a centralised, automated observability pipeline.

---

## Architecture

```
                         USER
                           |
                           v
                  Flask Application  (port 5000)
                           |
               +-----------+-----------+
               |                       |
            Metrics                   Logs
               |                       |
               v                       v
         Prometheus (9090)       Promtail (9080)
               |                       |
               |                       v
               |                  Loki (3100)
               |                       |
               +-----------+-----------+
                           |
                           v
                     Grafana (3000)

         Prometheus ─────────────────> Alertmanager (9093)
                                              |
                                              v
                                           Slack

         Node Exporter (9100) ──────> Prometheus
```

---

## Technology Stack

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.12 | Application runtime |
| Flask | 3.0.3 | Web framework |
| Gunicorn | 22.0.0 | WSGI server |
| Docker | 24+ | Containerisation |
| Docker Compose | v2 | Multi-service orchestration |
| Prometheus | 2.54.1 | Metrics collection |
| Grafana | 11.2.2 | Visualisation |
| Loki | 3.2.0 | Log aggregation |
| Promtail | 3.2.0 | Log collection |
| Alertmanager | 0.27.0 | Alert management |
| Node Exporter | 1.8.2 | System metrics |

---

## Project Structure

```
observability-stack/
│
├── app/
│   ├── app.py                    # Flask application
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile                # Application image
│
├── prometheus/
│   ├── prometheus.yml            # Scrape configuration
│   └── alerts.yml                # Alert rules
│
├── grafana/
│   └── provisioning/
│       ├── datasources/
│       │   └── datasource.yml    # Prometheus + Loki datasources
│       └── dashboards/
│           ├── dashboard.yml     # Dashboard provider config
│           ├── latency-dashboard.json
│           ├── error-dashboard.json
│           ├── infrastructure-dashboard.json
│           └── log-dashboard.json
│
├── loki/
│   └── loki-config.yml           # Loki configuration
│
├── promtail/
│   └── promtail-config.yml       # Log scrape config
│
├── alertmanager/
│   └── alertmanager.yml          # Alert routing + Slack
│
├── screenshots/                  # Project screenshots
├── .env.example                  # Environment variable template
├── .gitignore
├── docker-compose.yml            # Full stack definition
├── README.md
└── plan.md
```

---

## Quick Start

### Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose v2)
- A Slack workspace with an Incoming Webhook URL

### 1. Clone the repository

```bash
git clone https://github.com/AswinArun321/observability-stack-for-a-containerized-service.git
cd observability-stack-for-a-containerized-service
```

### 2. Configure Slack webhook

```bash
cp .env.example .env
# Edit .env and set your Slack webhook URL:
# SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

### 3. Start the stack

```bash
docker compose up -d --build
```

### 4. Verify all services are running

```bash
docker compose ps
```

Expected output — all 7 services should be **Up**:

```
NAME                          STATUS
observability-app             Up (healthy)
observability-prometheus      Up (healthy)
observability-grafana         Up (healthy)
observability-loki            Up (healthy)
observability-promtail        Up
observability-alertmanager    Up (healthy)
observability-node-exporter   Up
```

---

## Service URLs

| Service | URL | Credentials |
|---|---|---|
| Flask Application | http://localhost:5000 | — |
| Prometheus | http://localhost:9090 | — |
| Grafana | http://localhost:3000 | admin / admin |
| Loki | http://localhost:3100 | — |
| Alertmanager | http://localhost:9093 | — |
| Node Exporter | http://localhost:9100 | — |

---

## Application Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Application status |
| `/health` | GET | Health check |
| `/api/data` | GET | Normal API request |
| `/error` | GET | Generates HTTP 500 |
| `/slow` | GET | Adds 1–3s latency |
| `/metrics` | GET | Prometheus metrics |

---

## Docker Compose Commands

```bash
# Start all services
docker compose up -d

# Build and start
docker compose up -d --build

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# View logs
docker compose logs -f app
docker compose logs -f prometheus
docker compose logs -f grafana

# Restart a single service
docker compose restart prometheus
```

---

## Prometheus Configuration

Prometheus scrapes metrics every **5 seconds** from:

| Target | Address | Job |
|---|---|---|
| Flask app | `app:5000` | `application` |
| Node Exporter | `node-exporter:9100` | `node-exporter` |
| Prometheus itself | `localhost:9090` | `prometheus` |

Alert rules are loaded from `prometheus/alerts.yml`.

### Useful PromQL queries

```promql
# Request rate
rate(flask_http_request_total[5m])

# Error rate (%)
100 * (sum(rate(flask_http_request_total{status=~"5.."}[5m])) / sum(rate(flask_http_request_total[5m])))

# P95 latency
histogram_quantile(0.95, sum(rate(flask_http_request_duration_seconds_bucket[5m])) by (le))

# CPU usage (%)
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage (%)
100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)
```

---

## Grafana Dashboards

All four dashboards are provisioned automatically on startup.

### Dashboard 1 — Application Request Latency

Panels: Average Latency · P95 Latency · P99 Latency · Requests/sec

### Dashboard 2 — Application Error Monitoring

Panels: Total Requests · Error Rate · 5xx Requests · HTTP Status Distribution · Errors Over Time

### Dashboard 3 — Infrastructure Monitoring

Panels: CPU Usage Gauge · Memory Usage Gauge · CPU Trend · Memory Trend

### Dashboard 4 — Application Log Monitoring

Panels: Total Log Volume · ERROR Logs · WARNING Logs · INFO Logs · Logs Over Time · Recent Logs

---

## Loki and Promtail

Promtail reads Docker container logs from `/var/lib/docker/containers/` and forwards them to Loki.

### Useful LogQL queries

```logql
# All logs
{job="docker"}

# Error logs only
{job="docker"} |= "ERROR"

# Warning logs
{job="docker"} |= "WARNING"

# App container logs
{job="docker", container_name="observability-app"}
```

---

## Alert Rules

| Alert | Condition | Duration | Severity |
|---|---|---|---|
| HighErrorRate | Error rate > 5% | 30s | critical |
| HighRequestLatency | P95 > 1s | 30s | warning |
| ApplicationDown | `up == 0` | 30s | critical |
| HighCPUUsage | CPU > 80% | 2m | warning |
| HighMemoryUsage | Memory > 80% | 2m | warning |
| MonitoringTargetDown | Any target down | 1m | warning |

---

## Alertmanager

Alertmanager receives alerts from Prometheus and routes them to Slack.

Configuration file: `alertmanager/alertmanager.yml`

Slack channel: `#observability-alerts`

Alert grouping: by `alertname` and `severity`

Resolved alerts are also sent to Slack.

---

## Slack Integration

### Setup

1. Go to your Slack workspace → **Manage Apps** → **Incoming Webhooks**
2. Create a new webhook for channel `#observability-alerts`
3. Copy the webhook URL
4. Add it to `.env`:
   ```
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
   ```

> ⚠️ Never commit `.env` to version control.

---

## Failure Simulations

### Error spike test

```powershell
for ($i=1; $i -le 100; $i++) {
    try { Invoke-WebRequest http://localhost:5000/error } catch {}
}
```

Expected: HighErrorRate alert → Slack notification within ~40 seconds.

### Latency spike test

```powershell
for ($i=1; $i -le 50; $i++) {
    Invoke-WebRequest http://localhost:5000/slow
}
```

Expected: HighRequestLatency alert → Slack notification.

### Application down test

```bash
docker compose stop app
# Wait ~30–60 seconds
# Check Prometheus: up{job="application"} == 0
# ApplicationDown alert fires
docker compose start app
# Resolved notification sent to Slack
```

---

## Incident Detection Time

The detection pipeline:

```
Incident occurs
     ↓
Prometheus scrape (5s interval)
     ↓
Alert rule evaluation (5s interval)
     ↓
Alert fires after 30s (for)
     ↓
Alertmanager group_wait (10s)
     ↓
Slack notification

Total estimated time: ~45–60 seconds
```

> Measure your actual detection time: record T1 (incident start) and T2 (Slack notification time). Detection time = T2 − T1.

---

## Troubleshooting

### Prometheus target shows DOWN

Ensure `prometheus.yml` uses Docker service names:

```yaml
# ✅ Correct
targets: ["app:5000"]

# ❌ Wrong
targets: ["localhost:5000"]
```

### Grafana cannot connect to Prometheus

Datasource URL must be `http://prometheus:9090`, not `http://localhost:9090`.

### Logs not appearing in Loki

```bash
docker compose logs promtail
```

Check that `/var/lib/docker/containers` is accessible.

### Slack alerts not arriving

1. Verify `SLACK_WEBHOOK_URL` in `.env`
2. Check Alertmanager UI at `http://localhost:9093`
3. Check Prometheus alert status at `http://localhost:9090/alerts`
4. Check Alertmanager logs: `docker compose logs alertmanager`

---

## Future Enhancements

- Jaeger distributed tracing integration
- Kubernetes deployment with Helm charts
- Grafana OnCall for on-call scheduling
- mTLS between services
- VictoriaMetrics for long-term storage
- Custom business metrics

---

## Screenshots

Located in `screenshots/` directory.

---

## License

MIT
