# Observability Stack for a Containerized Service

## 1. Project Overview

### Project Name

**Observability Stack for a Containerized Service**

### Project Type

DevOps / Cloud / Monitoring / Observability

### Goal

Build an end-to-end observability platform for a containerized Flask web application using:

- Docker
- Docker Compose
- Prometheus
- Grafana
- Loki
- Promtail
- Alertmanager
- Node Exporter
- Slack

The system will collect and visualize:

- Application request metrics
- Request latency
- HTTP error rates
- CPU utilization
- Memory utilization
- Application logs
- Log volume
- Application health

It will also detect abnormal conditions and send notifications through Slack.

---

# 2. Problem Statement

Traditional applications often require developers to manually inspect logs and system resources when something goes wrong.

This creates problems such as:

- Errors may go unnoticed.
- Manual log inspection is time-consuming.
- Performance degradation may not be detected quickly.
- Logs are scattered across containers.
- Historical performance is difficult to analyze.
- There is no centralized monitoring system.
- There is no automated incident notification mechanism.

This project solves these problems by creating a centralized observability platform.

```text
Application
     |
     +---- Metrics ----> Prometheus
     |                       |
     |                       v
     |                    Grafana
     |
     +---- Logs -------> Promtail
                             |
                             v
                           Loki
                             |
                             v
                          Grafana

Prometheus
     |
     v
Alertmanager
     |
     v
Slack
```

---

# 3. Project Objectives

The project must:

- [ ] Containerize a Flask application.
- [ ] Run all components using Docker Compose.
- [ ] Expose Prometheus application metrics.
- [ ] Monitor request count.
- [ ] Monitor request rate.
- [ ] Monitor request latency.
- [ ] Monitor HTTP error rates.
- [ ] Monitor CPU utilization.
- [ ] Monitor memory utilization.
- [ ] Collect application logs.
- [ ] Centralize logs using Loki.
- [ ] Collect logs using Promtail.
- [ ] Visualize metrics using Grafana.
- [ ] Visualize logs using Grafana.
- [ ] Create four Grafana dashboards.
- [ ] Configure Prometheus alert rules.
- [ ] Configure Alertmanager.
- [ ] Send notifications to Slack.
- [ ] Simulate application failures.
- [ ] Simulate latency problems.
- [ ] Validate automated incident detection.
- [ ] Document the entire project.

---

# 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Flask | Demo web application |
| Gunicorn | Production-style WSGI server |
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| Prometheus | Metrics collection |
| Grafana | Visualization |
| Loki | Log aggregation |
| Promtail | Log collection |
| Alertmanager | Alert management |
| Node Exporter | System metrics |
| Slack | Notifications |
| PromQL | Prometheus queries |
| LogQL | Loki queries |
| Git/GitHub | Version control |

---

# 5. Final Architecture

```text
                         USER
                           |
                           | HTTP
                           v
                +----------------------+
                | Flask Application    |
                | Docker Container     |
                +----------+-----------+
                           |
                +----------+----------+
                |                     |
             Metrics                  Logs
                |                     |
                v                     v
         +-------------+       +-------------+
         | Prometheus  |       |  Promtail   |
         +------+------+       +------+------+
                |                     |
                |                     v
                |                +---------+
                |                |  Loki   |
                |                +----+----+
                |                     |
                +----------+----------+
                           |
                           v
                    +-------------+
                    |   Grafana   |
                    +-------------+

                    Prometheus
                         |
                         v
                  +-------------+
                  | Alertmanager |
                  +------+------+
                         |
                         v
                       Slack


                   System Metrics
                         |
                         v
                  +-------------+
                  |Node Exporter|
                  +------+------+
                         |
                         v
                    Prometheus
```

---

# 6. Repository Structure

Create the following structure:

```text
observability-stack/
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── prometheus/
│   ├── prometheus.yml
│   └── alerts.yml
│
├── grafana/
│   └── provisioning/
│       ├── datasources/
│       │   └── datasource.yml
│       │
│       └── dashboards/
│           └── dashboard.yml
│
├── loki/
│   └── loki-config.yml
│
├── promtail/
│   └── promtail-config.yml
│
├── alertmanager/
│   └── alertmanager.yml
│
├── screenshots/
│   ├── application.png
│   ├── prometheus.png
│   ├── grafana-overview.png
│   ├── latency-dashboard.png
│   ├── error-dashboard.png
│   ├── infrastructure-dashboard.png
│   ├── log-dashboard.png
│   └── slack-alert.png
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
└── plan.md
```

---

# 7. Phase 1 — Create Flask Application

## Objective

Build a lightweight application specifically designed to generate useful observability data.

The application should provide:

```text
/
 /health
 /api/data
 /error
 /slow
 /metrics
```

---

## 7.1 `/`

Normal application endpoint.

Expected response:

```json
{
  "service": "observability-demo",
  "status": "running"
}
```

---

## 7.2 `/health`

Health-check endpoint.

Expected:

```json
{
  "status": "healthy"
}
```

---

## 7.3 `/api/data`

Simulate a normal API request.

This endpoint should:

- Return JSON.
- Generate an application log.
- Generate Prometheus request metrics.

---

## 7.4 `/error`

Intentionally generate HTTP 500 responses.

Purpose:

- Generate errors.
- Increase error rate.
- Generate ERROR logs.
- Test alerting.

---

## 7.5 `/slow`

Intentionally delay the response.

Purpose:

- Simulate slow requests.
- Increase latency.
- Generate WARNING logs.
- Test latency alerts.

---

# 8. Phase 2 — Application Metrics

Install the Prometheus Flask client.

The application should expose:

```text
/metrics
```

Important metrics:

```text
flask_http_request_total
flask_http_request_duration_seconds
flask_http_request_duration_seconds_bucket
```

These metrics will be used to calculate:

- Total requests
- Requests per second
- Average latency
- P95 latency
- P99 latency
- HTTP status distribution
- Error rate

---

# 9. Phase 3 — Application Logging

Use Python's `logging` module.

Generate logs such as:

```text
INFO    Home endpoint accessed
INFO    Health check successful
INFO    API data requested
WARNING Slow request detected
ERROR   Simulated application error
```

Make sure logs are written to stdout/stderr so Docker can collect them.

The logging flow will be:

```text
Flask
  |
  v
Docker Logs
  |
  v
Promtail
  |
  v
Loki
  |
  v
Grafana
```

---

# 10. Phase 4 — Create Application Dockerfile

Create:

```text
app/Dockerfile
```

The Dockerfile should:

1. Use a Python base image.
2. Set the working directory.
3. Copy requirements.
4. Install dependencies.
5. Copy application source.
6. Expose port 5000.
7. Run Gunicorn.

The final application should be production-style rather than using Flask's development server.

---

# 11. Phase 5 — Create Docker Compose

Create:

```text
docker-compose.yml
```

Services:

```text
app
prometheus
grafana
loki
promtail
alertmanager
node-exporter
```

All services should share a monitoring network.

Concept:

```text
monitoring-network
│
├── app
├── prometheus
├── grafana
├── loki
├── promtail
├── alertmanager
└── node-exporter
```

---

# 12. Phase 6 — Configure Docker Networking

Use Docker service names for communication.

Examples:

```text
prometheus:9090
grafana:3000
loki:3100
alertmanager:9093
node-exporter:9100
app:5000
```

Do not use `localhost` for service-to-service communication inside Docker Compose.

For example:

```text
Correct:
http://prometheus:9090

Incorrect:
http://localhost:9090
```

---

# 13. Phase 7 — Start Application

Build:

```bash
docker compose build
```

Start:

```bash
docker compose up -d
```

Check:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs app
```

Test:

```text
http://localhost:5000
```

Health:

```text
http://localhost:5000/health
```

Metrics:

```text
http://localhost:5000/metrics
```

---

# 14. Phase 8 — Configure Prometheus

Create:

```text
prometheus/prometheus.yml
```

Prometheus should scrape:

```text
Flask application
Node Exporter
```

Application target:

```text
app:5000
```

Node Exporter:

```text
node-exporter:9100
```

Use a reasonable scrape interval such as:

```text
5 seconds
```

---

# 15. Phase 9 — Test Prometheus

Open:

```text
http://localhost:9090
```

Check:

```text
Status → Targets
```

Expected:

```text
application       UP
node-exporter     UP
```

Run:

```promql
flask_http_request_total
```

Verify that metrics are returned.

Also test:

```promql
up
```

---

# 16. Phase 10 — Configure Grafana

Grafana will be the main visualization layer.

Open:

```text
http://localhost:3000
```

Configure Prometheus datasource:

```text
http://prometheus:9090
```

Configure Loki datasource:

```text
http://loki:3100
```

Use Grafana provisioning where possible so datasources can be recreated automatically.

---

# 17. Phase 11 — Grafana Dashboard 1

## Request Latency Dashboard

Name:

```text
Application Request Latency
```

Panels:

```text
Average Latency
P95 Latency
P99 Latency
Requests Per Second
```

Average latency:

```promql
rate(flask_http_request_duration_seconds_sum[5m])
/
rate(flask_http_request_duration_seconds_count[5m])
```

P95:

```promql
histogram_quantile(
  0.95,
  sum(
    rate(flask_http_request_duration_seconds_bucket[5m])
  ) by (le)
)
```

P99:

```promql
histogram_quantile(
  0.99,
  sum(
    rate(flask_http_request_duration_seconds_bucket[5m])
  ) by (le)
)
```

Requests/sec:

```promql
rate(flask_http_request_total[5m])
```

---

# 18. Phase 12 — Grafana Dashboard 2

## Error Rate Dashboard

Name:

```text
Application Error Monitoring
```

Panels:

```text
Total Requests
Error Rate
5xx Requests
HTTP Status Distribution
Errors Over Time
```

Error rate:

```promql
100 *
(
  sum(rate(flask_http_request_total{status=~"5.."}[5m]))
  /
  sum(rate(flask_http_request_total[5m]))
)
```

Status distribution:

```promql
sum by (status) (
  rate(flask_http_request_total[5m])
)
```

---

# 19. Phase 13 — Deploy Node Exporter

Node Exporter provides system-level metrics.

Monitor:

```text
CPU
Memory
Disk
Network
System activity
```

Prometheus target:

```text
node-exporter:9100
```

---

# 20. Phase 14 — Grafana Dashboard 3

## Infrastructure Monitoring

Name:

```text
Infrastructure Monitoring
```

Panels:

```text
CPU Usage
Memory Usage
CPU Trend
Memory Trend
```

CPU query:

```promql
100 -
(
  avg(
    rate(node_cpu_seconds_total{mode="idle"}[5m])
  ) * 100
)
```

Memory query:

```promql
100 *
(
  1 -
  node_memory_MemAvailable_bytes
  /
  node_memory_MemTotal_bytes
)
```

---

# 21. Phase 15 — Deploy Loki

Create:

```text
loki/loki-config.yml
```

Run Loki on:

```text
3100
```

Loki will provide centralized log storage.

Architecture:

```text
Application
    |
    v
Docker Logs
    |
    v
Promtail
    |
    v
Loki
```

---

# 22. Phase 16 — Deploy Promtail

Create:

```text
promtail/promtail-config.yml
```

Promtail should:

- Read Docker container logs.
- Add useful labels.
- Track log positions.
- Forward logs to Loki.

Loki endpoint:

```text
http://loki:3100/loki/api/v1/push
```

---

# 23. Phase 17 — Verify Loki

Open Grafana.

Select:

```text
Explore
→ Loki
```

Run:

```logql
{job="docker"}
```

Verify application logs appear.

Test:

```logql
{job="docker"} |= "ERROR"
```

Test:

```logql
{job="docker"} |= "WARNING"
```

---

# 24. Phase 18 — Grafana Dashboard 4

## Application Log Monitoring

Name:

```text
Application Log Monitoring
```

Panels:

```text
Total Log Volume
ERROR Logs
WARNING Logs
INFO Logs
Logs Over Time
Recent Application Logs
```

Log volume:

```logql
count_over_time(
  {job="docker"}[5m]
)
```

Error logs:

```logql
{job="docker"} |= "ERROR"
```

Warning logs:

```logql
{job="docker"} |= "WARNING"
```

---

# 25. Phase 19 — Create Prometheus Alert Rules

Create:

```text
prometheus/alerts.yml
```

---

## Alert 1 — High Error Rate

Condition:

```text
Error rate > 5%
```

Duration:

```text
30 seconds
```

Name:

```text
HighErrorRate
```

Severity:

```text
critical
```

---

# 26. Alert 2 — High Request Latency

Condition:

```text
P95 latency > 1 second
```

Duration:

```text
30 seconds
```

Name:

```text
HighRequestLatency
```

Severity:

```text
warning
```

---

# 27. Alert 3 — Application Down

Use:

```promql
up{job="application"} == 0
```

Name:

```text
ApplicationDown
```

Severity:

```text
critical
```

---

# 28. Optional Alerts

After the core alerts work, add:

### High CPU

```text
CPU > 80%
```

### High Memory

```text
Memory > 80%
```

### Container Availability

Detect unavailable monitoring targets.

---

# 29. Phase 20 — Configure Alertmanager

Create:

```text
alertmanager/alertmanager.yml
```

Alertmanager receives alerts from Prometheus.

Architecture:

```text
Prometheus
    |
    | Alerts
    v
Alertmanager
    |
    | Routing
    v
Slack
```

Alertmanager should handle:

- Alert grouping
- Routing
- Notification
- Resolved alerts
- Notification deduplication

---

# 30. Phase 21 — Slack Integration

Create a Slack channel:

```text
#observability-alerts
```

Create the required Slack webhook.

Store it securely.

Create:

```text
.env
```

Example:

```text
SLACK_WEBHOOK_URL=your_webhook_url
```

Create:

```text
.env.example
```

Containing:

```text
SLACK_WEBHOOK_URL=
```

Never commit the real webhook.

---

# 31. Phase 22 — Security

Never commit:

```text
Slack webhook
API keys
Passwords
Tokens
Credentials
.env
```

`.gitignore` should contain:

```text
.env
*.log
__pycache__/
*.pyc
.vscode/
.idea/
```

Use environment variables for secrets.

---

# 32. Phase 23 — Health Checks

Add Docker health checks where appropriate.

Monitor:

```text
Application
Prometheus
Grafana
Loki
Alertmanager
```

The application health endpoint should be:

```text
/health
```

Expected:

```json
{
  "status": "healthy"
}
```

---

# 33. Phase 24 — Persistent Storage

Use Docker volumes where useful.

At minimum, consider persistence for:

```text
Grafana
Prometheus
Loki
Alertmanager
```

This prevents important monitoring data/configuration from disappearing when containers restart.

---

# 34. Phase 25 — Normal Traffic Test

Send requests to:

```text
/
```

and:

```text
/api/data
```

Expected:

```text
Normal request rate
Normal latency
Low error rate
Normal logs
```

Verify the dashboards update.

---

# 35. Phase 26 — Error Spike Test

Generate repeated requests to:

```text
/error
```

PowerShell:

```powershell
for ($i=1; $i -le 100; $i++) {
    try {
        Invoke-WebRequest http://localhost:5000/error
    }
    catch {}
}
```

Expected:

```text
HTTP 500
    ↓
Prometheus
    ↓
Error rate increases
    ↓
HighErrorRate
    ↓
Alertmanager
    ↓
Slack
```

---

# 36. Phase 27 — Latency Spike Test

Call:

```text
/slow
```

repeatedly.

Expected:

```text
Response latency increases
        ↓
P95 increases
        ↓
Prometheus detects threshold
        ↓
HighRequestLatency
        ↓
Alertmanager
        ↓
Slack
```

---

# 37. Phase 28 — Application Down Test

Stop the application container:

```bash
docker compose stop app
```

Prometheus should eventually detect:

```promql
up{job="application"} == 0
```

Expected:

```text
ApplicationDown
```

Restart:

```bash
docker compose start app
```

Verify recovery.

---

# 38. Phase 29 — Log Test

Generate:

```text
INFO
WARNING
ERROR
```

logs.

Verify in Grafana:

```logql
{job="docker"}
```

Error logs:

```logql
{job="docker"} |= "ERROR"
```

Warning logs:

```logql
{job="docker"} |= "WARNING"
```

---

# 39. Phase 30 — Measure Incident Detection Time

Do not claim a specific detection time without testing it.

Record:

```text
T1 = Incident generation time
T2 = Slack notification time
```

Calculate:

```text
Detection Time = T2 - T1
```

Example:

```text
Incident: 20:10:05
Slack:    20:10:37

Detection time = 32 seconds
```

Use your **actual measured result** in the final README and resume.

---

# 40. Phase 31 — Dashboard Validation

Verify all four dashboards.

## Dashboard 1

```text
Application Request Latency
```

Must show:

- Average latency
- P95 latency
- P99 latency
- Requests/sec

## Dashboard 2

```text
Application Error Monitoring
```

Must show:

- Total requests
- Error rate
- 5xx requests
- Status codes
- Error trends

## Dashboard 3

```text
Infrastructure Monitoring
```

Must show:

- CPU
- Memory
- CPU trends
- Memory trends

## Dashboard 4

```text
Application Log Monitoring
```

Must show:

- Log volume
- Errors
- Warnings
- Recent logs

---

# 41. Phase 32 — Complete Docker Compose Test

Run:

```bash
docker compose down
```

Then:

```bash
docker compose up -d --build
```

Check:

```bash
docker compose ps
```

Every required service should be running.

Expected services:

```text
app
prometheus
grafana
loki
promtail
alertmanager
node-exporter
```

---

# 42. Phase 33 — Troubleshooting

## Check all containers

```bash
docker compose ps
```

## Check application

```bash
docker compose logs app
```

## Check Prometheus

```bash
docker compose logs prometheus
```

## Check Grafana

```bash
docker compose logs grafana
```

## Check Loki

```bash
docker compose logs loki
```

## Check Promtail

```bash
docker compose logs promtail
```

## Check Alertmanager

```bash
docker compose logs alertmanager
```

## Check Node Exporter

```bash
docker compose logs node-exporter
```

---

# 43. Phase 34 — Common Problems

## Prometheus target DOWN

Check:

```text
prometheus.yml
```

Make sure the target uses the Docker service name:

```text
app:5000
```

not:

```text
localhost:5000
```

---

## Grafana cannot connect to Prometheus

Use:

```text
http://prometheus:9090
```

not:

```text
http://localhost:9090
```

---

## Grafana cannot connect to Loki

Use:

```text
http://loki:3100
```

---

## Logs not appearing

Check:

```bash
docker compose logs promtail
```

Then check the Promtail configuration and Docker log path.

---

## Slack alerts not arriving

Check:

1. Alert rule is firing.
2. Prometheus is connected to Alertmanager.
3. Alertmanager configuration is valid.
4. Slack webhook is correct.
5. Webhook is not expired/revoked.

---

# 44. Phase 35 — GitHub Repository

Recommended repository name:

```text
observability-stack
```

Recommended description:

```text
Docker-based observability platform using Prometheus, Grafana, Loki, Promtail, Alertmanager, and Node Exporter to monitor a containerized Flask application.
```

---

# 45. Phase 36 — Git Initialization

Run:

```bash
git init
```

Create `.gitignore`.

Then:

```bash
git add .
```

Commit:

```bash
git commit -m "Initial observability stack"
```

---

# 46. Phase 37 — GitHub Push

Create:

```text
observability-stack
```

Then:

```bash
git branch -M main
```

Add remote:

```bash
git remote add origin https://github.com/AswinArun321/observability-stack.git
```

Push:

```bash
git push -u origin main
```

---

# 47. Phase 38 — Screenshots

Capture screenshots of:

### Application

```text
Flask application
```

### Prometheus

```text
Prometheus targets
Prometheus query
```

### Grafana

Capture:

```text
Latency dashboard
Error dashboard
Infrastructure dashboard
Log dashboard
```

### Alertmanager

Capture:

```text
Firing alert
```

### Slack

Capture:

```text
Slack notification
```

Store them in:

```text
screenshots/
```

---

# 48. Phase 39 — README Documentation

README should contain:

1. Project overview
2. Problem statement
3. Architecture
4. Technologies
5. Project structure
6. Setup instructions
7. Docker Compose commands
8. Prometheus configuration
9. Grafana dashboards
10. Loki and Promtail
11. Alertmanager
12. Slack integration
13. Failure simulations
14. Screenshots
15. Results
16. Future enhancements

---

# 49. Phase 40 — Final Demonstration

Use this sequence for your project presentation.

## Step 1 — Architecture

Explain:

```text
Application
→ Prometheus
→ Grafana
```

and:

```text
Application
→ Promtail
→ Loki
→ Grafana
```

and:

```text
Prometheus
→ Alertmanager
→ Slack
```

---

## Step 2 — Show Docker

```bash
docker compose ps
```

Explain all seven services.

---

## Step 3 — Show Application

Open:

```text
http://localhost:5000
```

Then:

```text
/health
```

---

## Step 4 — Show Prometheus

Open:

```text
http://localhost:9090
```

Show:

```text
Targets
Metrics
Queries
```

---

## Step 5 — Show Grafana

Open:

```text
http://localhost:3000
```

Show all four dashboards.

---

## Step 6 — Generate Errors

Use:

```text
/error
```

Show:

```text
Error rate increases
```

---

## Step 7 — Show Logs

Open Grafana Explore.

Run:

```logql
{job="docker"} |= "ERROR"
```

---

## Step 8 — Generate Latency

Use:

```text
/slow
```

Show the latency dashboard.

---

## Step 9 — Show Alert

Show:

```text
Prometheus
→ Alertmanager
→ Slack
```

---

## Step 10 — Demonstrate Recovery

Stop the application:

```bash
docker compose stop app
```

Show the application-down alert.

Restart:

```bash
docker compose start app
```

Show the recovery.

---

# 50. Final Testing Checklist

## Application

- [ ] Flask application works.
- [ ] `/` works.
- [ ] `/health` works.
- [ ] `/api/data` works.
- [ ] `/error` produces 500.
- [ ] `/slow` produces latency.
- [ ] `/metrics` exposes metrics.
- [ ] Logs are generated.

## Docker

- [ ] Dockerfile works.
- [ ] Image builds.
- [ ] Docker Compose works.
- [ ] All containers start.
- [ ] Network communication works.
- [ ] Volumes work where required.

## Prometheus

- [ ] Prometheus starts.
- [ ] Application target is UP.
- [ ] Node Exporter is UP.
- [ ] Metrics are collected.
- [ ] PromQL works.
- [ ] Alert rules load.

## Grafana

- [ ] Grafana starts.
- [ ] Prometheus datasource works.
- [ ] Loki datasource works.
- [ ] Latency dashboard works.
- [ ] Error dashboard works.
- [ ] Infrastructure dashboard works.
- [ ] Log dashboard works.

## Loki

- [ ] Loki starts.
- [ ] Promtail starts.
- [ ] Logs arrive in Loki.
- [ ] LogQL works.

## Alerting

- [ ] Alertmanager starts.
- [ ] Prometheus sends alerts.
- [ ] Error alert works.
- [ ] Latency alert works.
- [ ] Application-down alert works.
- [ ] Slack notification works.
- [ ] Recovery notification works.

## Documentation

- [ ] README completed.
- [ ] Architecture documented.
- [ ] Screenshots added.
- [ ] Setup instructions tested.
- [ ] Failure scenarios documented.
- [ ] Actual detection time measured.
- [ ] GitHub repository complete.

---

# 51. Final Architecture Verification

The completed project should achieve this complete flow:

```text
                         USER
                           |
                           v
                  Flask Application
                           |
              +------------+------------+
              |                         |
           Metrics                     Logs
              |                         |
              v                         v
        Prometheus                  Promtail
              |                         |
              |                         v
              |                       Loki
              |                         |
              +------------+------------+
                           |
                           v
                        Grafana
                           |
                           |
Prometheus --------------+
    |
    v
Alertmanager
    |
    v
  Slack
```

Node Exporter:

```text
Node Exporter
     |
     v
Prometheus
     |
     v
Grafana
```

---

# 52. Definition of Done

The project is complete when:

- [ ] Flask application is containerized.
- [ ] Docker Compose launches the complete stack.
- [ ] Prometheus collects application metrics.
- [ ] Node Exporter provides system metrics.
- [ ] Grafana displays metrics.
- [ ] Loki stores application logs.
- [ ] Promtail forwards Docker logs.
- [ ] Grafana displays logs.
- [ ] Four dashboards are working.
- [ ] Prometheus alert rules are configured.
- [ ] Alertmanager routes alerts.
- [ ] Slack notifications work.
- [ ] Error spike is detected.
- [ ] Latency spike is detected.
- [ ] Application failure is detected.
- [ ] Recovery is verified.
- [ ] Incident detection time is measured.
- [ ] Screenshots are captured.
- [ ] README is complete.
- [ ] GitHub repository is pushed successfully.

---

# 53. Recommended Implementation Order

Do not build all components simultaneously.

Follow this exact order:

```text
1. Flask Application
        ↓
2. Application Logging
        ↓
3. Prometheus Metrics
        ↓
4. Dockerfile
        ↓
5. Docker Compose
        ↓
6. Prometheus
        ↓
7. Grafana
        ↓
8. Node Exporter
        ↓
9. Loki
        ↓
10. Promtail
        ↓
11. Four Grafana Dashboards
        ↓
12. Prometheus Alert Rules
        ↓
13. Alertmanager
        ↓
14. Slack
        ↓
15. Failure Simulation
        ↓
16. Testing
        ↓
17. Screenshots
        ↓
18. README
        ↓
19. GitHub Push
        ↓
20. Final Demo
```

This order ensures that each layer is tested before the next one is added.

---

# 54. Portfolio Result

After completion, the project should demonstrate practical knowledge of:

```text
Docker
Docker Compose
Prometheus
PromQL
Grafana
Loki
LogQL
Promtail
Alertmanager
Node Exporter
Slack
Python
Flask
Gunicorn
Linux
Git
GitHub
DevOps
Monitoring
Observability
Incident Detection
```

The key story of the project is:

```text
                    DETECT
                       ↓
                    ANALYZE
                       ↓
                     ALERT
                       ↓
                    NOTIFY
                       ↓
                 TROUBLESHOOT
                       ↓
                    RECOVER
```

The uploaded specification also explicitly defines the intended outcome as an end-to-end observability workflow covering metrics, logs, dashboards, alerts, Slack notifications, and failure simulation.