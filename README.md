# Observability Stack for a Containerized Service

## 1. Project Overview

### Project Name

**Observability Stack for a Containerized Service**

### Project Type

DevOps / Cloud / Monitoring / Observability

### Project Goal

Build a complete observability platform for a containerized web application using **Docker Compose, Prometheus, Grafana, Loki, Promtail, Alertmanager, and Node Exporter**.

The system will collect and visualize:

- Application request metrics
- Request latency
- HTTP error rates
- CPU utilization
- Memory utilization
- Application logs
- Log volume
- Application health

The system will also automatically detect abnormal conditions and send notifications through **Slack** using Alertmanager.

---

# 2. Problem Statement

In a traditional application deployment, developers or administrators may need to manually inspect application logs and system resources when a problem occurs.

This creates several problems:

- Errors may go unnoticed.
- Manual log inspection is time-consuming.
- Performance degradation may not be detected immediately.
- There is no centralized monitoring system.
- It is difficult to understand historical performance.
- There is no automatic incident notification mechanism.

This project solves these problems by implementing a centralized observability stack.

The application generates telemetry, Prometheus collects metrics, Loki collects logs, Grafana visualizes the data, and Alertmanager sends notifications when predefined thresholds are exceeded.

---

# 3. Objectives

The main objectives are:

1. Containerize a web application using Docker.
2. Deploy the complete observability stack using Docker Compose.
3. Collect application metrics using Prometheus.
4. Monitor HTTP request latency.
5. Monitor application error rates.
6. Monitor CPU and memory utilization.
7. Centralize application logs using Loki.
8. Collect Docker container logs using Promtail.
9. Build Grafana dashboards.
10. Configure Prometheus alert rules.
11. Route alerts through Alertmanager.
12. Send alerts to Slack.
13. Simulate application failures and performance issues.
14. Demonstrate automated incident detection.
15. Document the complete architecture and implementation.

---

# 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Flask | Demo web application |
| Gunicorn | Production-style WSGI server |
| Docker | Application containerization |
| Docker Compose | Multi-container orchestration |
| Prometheus | Metrics collection and monitoring |
| Grafana | Metrics and log visualization |
| Loki | Log aggregation |
| Promtail | Log collection and forwarding |
| Alertmanager | Alert management and notification routing |
| Node Exporter | System-level metrics |
| Slack | Alert notifications |
| PromQL | Prometheus queries |
| LogQL | Loki queries |
| Git/GitHub | Version control and project hosting |

---

# 5. High-Level Architecture

```text
                           USERS
                             |
                             | HTTP
                             v
                  +----------------------+
                  |   Flask Application   |
                  |      Container       |
                  +----------+-----------+
                             |
             +---------------+----------------+
             |                                |
             | Metrics                        | Logs
             v                                v
     +---------------+                 +---------------+
     |  Prometheus   |                 |   Promtail   |
     |    Metrics    |                 | Log Collector|
     +-------+-------+                 +-------+-------+
             |                                 |
             |                                 v
             |                         +---------------+
             |                         |     Loki      |
             |                         | Log Storage   |
             |                         +-------+-------+
             |                                 |
             +----------------+----------------+
                              |
                              v
                     +----------------+
                     |     Grafana    |
                     |   Dashboards   |
                     +----------------+

                              ^
                              |
                     +----------------+
                     |  Alertmanager  |
                     | Alert Routing  |
                     +-------+--------+
                             |
                             v
                           Slack


                    System Metrics
                          |
                          v
                   +--------------+
                   | Node Exporter|
                   +------+-------+
                          |
                          v
                     Prometheus
```

---

# 6. Observability Concepts

The project primarily focuses on two major observability signals:

## 6.1 Metrics

Metrics are numerical measurements collected over time.

Examples:

- Number of requests
- Requests per second
- Error rate
- Request latency
- CPU usage
- Memory usage

Prometheus will collect and store these metrics.

---

## 6.2 Logs

Logs are textual records generated by applications and infrastructure.

Example:

```text
INFO Home endpoint accessed
INFO API data requested
WARNING Slow request detected
ERROR Simulated application error
```

Loki will store these logs.

Promtail will collect and forward them.

---

# 7. Application Design

The project will use a lightweight Flask application specifically designed for monitoring demonstrations.

## Application Endpoints

### `/`

Normal application endpoint.

Expected response:

```json
{
  "service": "observability-demo",
  "status": "running"
}
```

---

### `/health`

Health-check endpoint.

Expected response:

```json
{
  "status": "healthy"
}
```

---

### `/api/data`

Simulates a normal API request.

---

### `/error`

Intentionally generates an HTTP 500 error.

Purpose:

- Test error monitoring.
- Trigger error-rate alerts.
- Generate ERROR logs.

---

### `/slow`

Intentionally delays the response.

Purpose:

- Test latency monitoring.
- Generate WARNING logs.
- Trigger latency alerts.

---

# 8. Application Metrics

The Flask application will expose Prometheus-compatible metrics.

The main metrics include:

```text
flask_http_request_total
flask_http_request_duration_seconds
flask_http_request_duration_seconds_bucket
```

These metrics will allow the project to calculate:

- Total requests
- Requests per second
- Average latency
- P95 latency
- P99 latency
- HTTP status distribution
- Error rate

---

# 9. Logging Design

The Flask application will use Python's logging system.

Example:

```text
INFO    Home endpoint accessed
INFO    Health check successful
INFO    API data requested
WARNING Slow request detected
ERROR   Simulated application error
```

Logs will follow a structured and searchable format.

The flow will be:

```text
Flask Application
       |
       v
Docker Container Logs
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

# 10. Docker Architecture

All components will run as containers.

The main services are:

```text
app
prometheus
grafana
loki
promtail
alertmanager
node-exporter
```

Docker Compose will create a common monitoring network.

```text
monitoring network

+------------------------------------------------+
|                                                |
| app                                            |
| prometheus                                     |
| grafana                                        |
| loki                                           |
| promtail                                       |
| alertmanager                                   |
| node-exporter                                  |
|                                                |
+------------------------------------------------+
```

Services communicate using Docker service names.

Example:

```text
http://prometheus:9090
http://grafana:3000
http://loki:3100
http://alertmanager:9093
```

---

# 11. Repository Structure

The final repository should follow this structure:

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
└── README.md
```

---

# 12. Phase 1 — Build the Application

## Tasks

- Create Flask application.
- Create endpoints.
- Add logging.
- Add Prometheus instrumentation.
- Create requirements file.
- Create Dockerfile.

## Expected Result

The application should run inside Docker.

Test:

```text
http://localhost:5000
```

Expected:

```json
{
  "service": "observability-demo",
  "status": "running"
}
```

---

# 13. Phase 2 — Containerize Application

Create the application Dockerfile.

The Dockerfile should:

1. Use Python base image.
2. Set working directory.
3. Install dependencies.
4. Copy application source.
5. Expose port 5000.
6. Start the application using Gunicorn.

Build:

```bash
docker compose build
```

Run:

```bash
docker compose up -d
```

Check:

```bash
docker compose ps
```

---

# 14. Phase 3 — Deploy Prometheus

Prometheus will monitor the application.

Create:

```text
prometheus/prometheus.yml
```

Configure:

```text
scrape_interval: 5s
```

Prometheus target:

```text
app:5000
```

Prometheus will access:

```text
http://app:5000/metrics
```

Test Prometheus:

```text
http://localhost:9090
```

Run:

```promql
flask_http_request_total
```

Expected result:

Prometheus should return the application's HTTP request metrics.

---

# 15. Phase 4 — Configure Grafana

Grafana will provide the visualization layer.

Access:

```text
http://localhost:3000
```

Configure:

```text
Prometheus → http://prometheus:9090
Loki       → http://loki:3100
```

Grafana will be configured using provisioning files where possible.

---

# 16. Dashboard 1 — Request Latency

## Dashboard Name

**Application Request Latency**

## Purpose

Monitor application response performance.

## Panels

### Average Request Latency

```promql
rate(flask_http_request_duration_seconds_sum[5m])
/
rate(flask_http_request_duration_seconds_count[5m])
```

---

### P95 Latency

```promql
histogram_quantile(
  0.95,
  sum(
    rate(
      flask_http_request_duration_seconds_bucket[5m]
    )
  ) by (le)
)
```

---

### P99 Latency

```promql
histogram_quantile(
  0.99,
  sum(
    rate(
      flask_http_request_duration_seconds_bucket[5m]
    )
  ) by (le)
)
```

---

### Requests Per Second

```promql
rate(flask_http_request_total[5m])
```

---

## Dashboard Objective

The dashboard should make it easy to identify:

- Slow requests
- Latency spikes
- Changes in traffic
- Performance degradation

---

# 17. Dashboard 2 — Error Rate

## Dashboard Name

**Application Error Monitoring**

## Purpose

Monitor HTTP errors.

## Error Rate Query

```promql
100 *
(
  sum(rate(flask_http_request_total{status=~"5.."}[5m]))
  /
  sum(rate(flask_http_request_total[5m]))
)
```

---

## Status Code Distribution

```promql
sum by (status) (
  rate(flask_http_request_total[5m])
)
```

---

## Dashboard Panels

```text
Total Requests
Error Rate
5xx Requests
HTTP Status Distribution
Errors Over Time
```

---

# 18. Dashboard 3 — Infrastructure Monitoring

## Dashboard Name

**Infrastructure Monitoring**

## Purpose

Monitor host/system resource utilization.

Node Exporter will expose system metrics.

Important metrics:

```text
node_cpu_seconds_total
node_memory_MemTotal_bytes
node_memory_MemAvailable_bytes
```

---

## CPU Usage

Example PromQL:

```promql
100 -
(
  avg(
    rate(node_cpu_seconds_total{mode="idle"}[5m])
  ) * 100
)
```

---

## Memory Usage

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

## Dashboard Panels

```text
CPU Usage
Memory Usage
CPU Usage Over Time
Memory Usage Over Time
System Resource Trends
```

---

# 19. Dashboard 4 — Log Volume

## Dashboard Name

**Application Log Monitoring**

## Purpose

Visualize application logs using Loki.

Basic LogQL query:

```logql
{job="docker"}
```

---

## Log Volume

```logql
count_over_time(
  {job="docker"}[5m]
)
```

---

## Error Logs

```logql
{job="docker"} |= "ERROR"
```

---

## Warning Logs

```logql
{job="docker"} |= "WARNING"
```

---

## Dashboard Panels

```text
Total Log Volume
ERROR Logs
WARNING Logs
INFO Logs
Logs Over Time
Recent Application Logs
```

---

# 20. Phase 5 — Deploy Loki

Loki will provide centralized log storage.

Loki will run on:

```text
3100
```

Access:

```text
http://localhost:3100
```

The architecture will be:

```text
Application
     |
     v
Docker logs
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

# 21. Phase 6 — Deploy Promtail

Promtail will collect Docker container logs.

Promtail will:

1. Read Docker logs.
2. Add labels.
3. Send logs to Loki.
4. Track log positions.

Promtail target:

```text
http://loki:3100/loki/api/v1/push
```

---

# 22. Phase 7 — Deploy Node Exporter

Node Exporter will collect system-level metrics.

Metrics include:

- CPU
- Memory
- Disk
- Network
- System activity

Prometheus will scrape Node Exporter.

Target:

```text
node-exporter:9100
```

---

# 23. Phase 8 — Configure Alert Rules

Prometheus will evaluate alert rules.

## Alert 1 — High Error Rate

Condition:

```text
Error rate > 5%
```

For:

```text
30 seconds
```

Alert name:

```text
HighErrorRate
```

Severity:

```text
critical
```

---

# 24. Alert 2 — High Request Latency

Condition:

```text
P95 latency > 1 second
```

For:

```text
30 seconds
```

Alert name:

```text
HighRequestLatency
```

Severity:

```text
warning
```

---

# 25. Optional Additional Alerts

After the main system works, add:

## High CPU Usage

```text
CPU > 80%
```

## High Memory Usage

```text
Memory > 80%
```

## Application Down

Use Prometheus `up` metric:

```promql
up{job="application"} == 0
```

Alert:

```text
ApplicationDown
```

---

# 26. Phase 9 — Alertmanager

Alertmanager receives alerts from Prometheus.

Architecture:

```text
Prometheus
     |
     | Alert
     v
Alertmanager
     |
     | Routing
     v
Slack
```

Alertmanager responsibilities:

- Group alerts
- Route alerts
- Send notifications
- Handle resolved alerts
- Prevent notification spam

---

# 27. Phase 10 — Slack Integration

Create a Slack channel:

```text
#observability-alerts
```

Configure a Slack webhook.

The webhook must not be committed to GitHub.

Use environment variables.

Example:

```text
SLACK_WEBHOOK_URL=your_webhook_url
```

Create:

```text
.env
```

and:

```text
.env.example
```

`.env` must be included in `.gitignore`.

`.env.example` should contain only:

```text
SLACK_WEBHOOK_URL=
```

---

# 28. Security Requirements

Never commit:

```text
Slack webhook URLs
API keys
Passwords
Tokens
Credentials
Private configuration
```

`.gitignore` should include:

```text
.env
*.log
__pycache__/
*.pyc
.vscode/
.idea/
```

---

# 29. Phase 11 — Incident Simulation

The project must include controlled failure testing.

## Test 1 — Normal Traffic

Send requests to:

```text
/
```

Expected:

```text
Low error rate
Normal latency
Normal logs
```

---

## Test 2 — Error Spike

Send many requests to:

```text
/error
```

Example PowerShell:

```powershell
for ($i=1; $i -le 100; $i++) {
    try {
        Invoke-WebRequest http://localhost:5000/error
    }
    catch {}
}
```

Expected flow:

```text
HTTP 500 errors
       ↓
Prometheus
       ↓
Error rate > 5%
       ↓
HighErrorRate
       ↓
Alertmanager
       ↓
Slack
```

---

# 30. Test 3 — Latency Spike

Send repeated requests to:

```text
/slow
```

Expected:

```text
Response latency increases
       ↓
P95 latency increases
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

# 31. Test 4 — Application Down

Stop the application:

```bash
docker stop observability-app
```

Prometheus should detect:

```text
up{job="application"} = 0
```

This can trigger:

```text
ApplicationDown
```

Start it again:

```bash
docker start observability-app
```

---

# 32. Test 5 — Log Generation

Generate:

```text
INFO
WARNING
ERROR
```

logs.

Verify them in Grafana's Loki datasource.

Search:

```logql
{job="docker"}
```

Then:

```logql
{job="docker"} |= "ERROR"
```

---

# 33. Incident Detection Measurement

To support the project claim about rapid incident detection, measure the actual time.

Record:

```text
T1 = Time when incident is generated
T2 = Time when Slack notification is received
```

Calculate:

```text
Detection Time = T2 - T1
```

Example:

```text
Incident generated: 20:10:05
Slack alert:        20:10:37

Detection time: 32 seconds
```

The final README should report the **measured result**, not an assumed value.

---

# 34. Expected Results

The completed project should provide:

### Application

```text
Containerized Flask application
```

### Metrics

```text
Request count
Request rate
Latency
HTTP status codes
CPU
Memory
```

### Logs

```text
Centralized application logs
```

### Dashboards

```text
1. Request Latency
2. Error Rate
3. Infrastructure
4. Log Volume
```

### Alerts

```text
HighErrorRate
HighRequestLatency
ApplicationDown
HighCPUUsage
HighMemoryUsage
```

### Notification

```text
Slack
```

---

# 35. Final Grafana Dashboard Layout

The final system should contain:

```text
Grafana
│
├── Application Request Latency
│   ├── Average Latency
│   ├── P95 Latency
│   ├── P99 Latency
│   └── Requests/sec
│
├── Application Error Monitoring
│   ├── Error Rate
│   ├── 5xx Requests
│   ├── Status Codes
│   └── Errors Over Time
│
├── Infrastructure Monitoring
│   ├── CPU
│   ├── Memory
│   ├── CPU Trend
│   └── Memory Trend
│
└── Application Log Monitoring
    ├── Log Volume
    ├── Error Logs
    ├── Warning Logs
    └── Recent Logs
```

---

# 36. Health Checks

Docker Compose health checks should be considered for:

```text
Application
Prometheus
Grafana
Loki
Alertmanager
```

The goal is to make service availability visible and prevent dependent services from being started before their dependencies are ready.

---

# 37. Persistence

Important monitoring data should use Docker volumes where appropriate.

Example:

```text
grafana-data
```

This prevents Grafana configuration and dashboards from disappearing when containers restart.

For a local demonstration project, persistence can be limited to the components where it is useful.

---

# 38. Configuration Management

Configuration files should be separated from application source code.

```text
prometheus/
    prometheus.yml
    alerts.yml

loki/
    loki-config.yml

promtail/
    promtail-config.yml

alertmanager/
    alertmanager.yml
```

Benefits:

- Easier maintenance
- Easier debugging
- Easier deployment
- Better GitHub organization
- Clear separation of responsibilities

---

# 39. Docker Compose Commands

Start everything:

```bash
docker compose up -d
```

Build and start:

```bash
docker compose up -d --build
```

View containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

Application logs:

```bash
docker compose logs app
```

Prometheus logs:

```bash
docker compose logs prometheus
```

Grafana logs:

```bash
docker compose logs grafana
```

Loki logs:

```bash
docker compose logs loki
```

Alertmanager logs:

```bash
docker compose logs alertmanager
```

Stop:

```bash
docker compose down
```

Stop and remove volumes:

```bash
docker compose down -v
```

---

# 40. Testing Checklist

## Application

- [ ] Application starts successfully.
- [ ] `/` works.
- [ ] `/health` works.
- [ ] `/api/data` works.
- [ ] `/error` generates 500 errors.
- [ ] `/slow` generates delayed responses.
- [ ] Logs are generated.

## Prometheus

- [ ] Prometheus starts.
- [ ] Application target is UP.
- [ ] Metrics are visible.
- [ ] PromQL queries work.
- [ ] Alert rules load successfully.

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
- [ ] LogQL queries work.

## Alertmanager

- [ ] Alertmanager starts.
- [ ] Prometheus sends alerts.
- [ ] Alerts are routed correctly.
- [ ] Slack notification works.
- [ ] Resolved alerts work.

---

# 41. Failure Scenarios

The project should demonstrate at least these scenarios:

| Scenario | Expected Observation |
|---|---|
| Normal traffic | Normal metrics |
| High request volume | Increased request rate |
| `/error` requests | Increased error rate |
| `/slow` requests | Increased latency |
| Application stopped | Application-down alert |
| High CPU | CPU alert |
| High memory | Memory alert |
| Error logs | Loki displays ERROR logs |
| Warning logs | Loki displays WARNING logs |

---

# 42. Project Demonstration Flow

During the final presentation/demo, use this sequence.

## Step 1

Show the architecture.

Explain:

```text
Application
→ Prometheus
→ Grafana

Application
→ Promtail
→ Loki
→ Grafana

Prometheus
→ Alertmanager
→ Slack
```

---

## Step 2

Show Docker containers.

```bash
docker compose ps
```

Explain each container.

---

## Step 3

Open the application.

```text
http://localhost:5000
```

---

## Step 4

Show Prometheus.

```text
http://localhost:9090
```

Run:

```promql
flask_http_request_total
```

---

## Step 5

Open Grafana.

```text
http://localhost:3000
```

Show the four dashboards.

---

## Step 6

Generate errors.

Open:

```text
/error
```

multiple times.

Show the error-rate dashboard increasing.

---

## Step 7

Show Loki.

Search:

```logql
{job="docker"} |= "ERROR"
```

---

## Step 8

Generate slow requests.

Open:

```text
/slow
```

Show the latency dashboard.

---

## Step 9

Show Slack.

Demonstrate the alert notification.

---

## Step 10

Stop the application.

```bash
docker stop observability-app
```

Show the application-down alert.

---

# 43. Expected Project Outcome

At the end of the project, a developer or administrator should be able to answer:

```text
Is the application running?
        ↓
Prometheus

Is the application slow?
        ↓
Latency Dashboard

Is the application producing errors?
        ↓
Error Dashboard

What is happening inside the application?
        ↓
Loki Logs

Is the infrastructure under heavy load?
        ↓
Infrastructure Dashboard

Does something require immediate attention?
        ↓
Alertmanager → Slack
```

---

# 44. Future Enhancements

The following features can be added later.

## Distributed Tracing

Add:

```text
OpenTelemetry
Tempo
```

This would introduce the third major observability signal:

```text
Metrics
Logs
Traces
```

---

## Kubernetes Deployment

Move the stack from Docker Compose to:

```text
Kubernetes
```

Use:

```text
Helm
Kubernetes Service
ConfigMaps
Secrets
Persistent Volumes
```

---

## Cloud Deployment

Deploy the observability stack to:

```text
AWS
Azure
Google Cloud
```

---

## HTTPS

Add:

```text
Nginx
TLS/SSL
HTTPS
```

---

## Authentication

Protect Grafana and monitoring endpoints using proper authentication.

---

## Advanced Alerting

Add:

```text
CPU alerts
Memory alerts
Disk alerts
Container restart alerts
Application availability alerts
```

---

## Automated Incident Response

Future versions could trigger automated remediation actions.

Example:

```text
Application failure
       ↓
Alert
       ↓
Automation
       ↓
Restart container
       ↓
Health check
       ↓
Recovery notification
```

---

# 45. Security Improvements

For a production deployment:

- Use Docker secrets.
- Use HTTPS.
- Restrict exposed ports.
- Use authentication.
- Use least-privilege containers.
- Avoid running containers as root.
- Pin image versions instead of relying on `latest`.
- Restrict Grafana access.
- Secure Alertmanager.
- Secure Loki.
- Rotate Slack webhook credentials.
- Use network isolation.
- Regularly update container images.

---

# 46. Production Improvements

The college/demo version can use Docker Compose and local storage.

A production version should additionally consider:

```text
High availability
Persistent storage
Backup
Authentication
TLS
Access control
Centralized secrets
Kubernetes
Cloud monitoring
Distributed tracing
Log retention
Scalability
```

---

# 47. GitHub Strategy

Recommended repository name:

```text
observability-stack
```

Alternative:

```text
container-observability-platform
```

Recommended repository description:

```text
A Docker-based observability platform using Prometheus, Grafana, Loki, Promtail, Alertmanager, and Slack to monitor a containerized Flask application.
```

---

# 48. Git Commit Strategy

Use meaningful commits.

Example:

```text
Initial project structure
```

```text
Add Flask monitoring application
```

```text
Containerize application with Docker
```

```text
Add Prometheus monitoring
```

```text
Add Grafana provisioning
```

```text
Add Loki log aggregation
```

```text
Add Promtail log collection
```

```text
Add Node Exporter infrastructure metrics
```

```text
Add Prometheus alert rules
```

```text
Configure Alertmanager
```

```text
Add Slack notifications
```

```text
Add observability dashboards
```

```text
Add documentation
```

---

# 49. Resume Description

After completing and testing the project, the resume entry can be written as:

**Observability Stack for Containerized Service**

- Deployed Prometheus, Grafana, Loki, Promtail, Alertmanager, and Node Exporter using Docker Compose to monitor a containerized Flask application.
- Built Grafana dashboards for request latency, HTTP error rates, CPU/memory utilization, and application log volume using PromQL and LogQL.
- Configured threshold-based Prometheus alerts and Alertmanager routing with Slack notifications, enabling automated detection of application failures and performance issues.
- Simulated latency spikes, HTTP failures, and application outages to validate monitoring, logging, and alerting workflows.

If an actual measured detection time is obtained, add:

```text
Validated automated incident detection with measured alert delivery within <X> seconds.
```

Do not claim a specific time until it has been experimentally measured.

---

# 50. Viva Questions

## What is observability?

Observability is the ability to understand the internal state of a system by analyzing telemetry produced by that system.

---

## What are the three pillars of observability?

```text
Metrics
Logs
Traces
```

This project primarily implements:

```text
Metrics + Logs
```

Tracing can be added as a future enhancement.

---

## What is Prometheus?

Prometheus is a time-series monitoring and alerting system that collects numerical metrics from monitored targets.

---

## What is Grafana?

Grafana is a visualization and observability platform used to create dashboards from sources such as Prometheus and Loki.

---

## What is Loki?

Loki is a log aggregation system designed to store and query logs.

---

## What is Promtail?

Promtail is a log collector that forwards logs to Loki.

---

## What is Alertmanager?

Alertmanager handles alerts generated by Prometheus and routes them to notification systems such as Slack.

---

## What is PromQL?

PromQL is Prometheus Query Language.

Example:

```promql
rate(flask_http_request_total[5m])
```

---

## What is LogQL?

LogQL is the query language used by Loki.

Example:

```logql
{job="docker"} |= "ERROR"
```

---

## Why use Docker Compose?

Docker Compose allows multiple related services to be defined and managed together.

Instead of starting seven containers manually:

```text
docker run ...
docker run ...
docker run ...
```

we can use:

```bash
docker compose up -d
```

---

## Why do we need both Prometheus and Loki?

They serve different purposes.

```text
Prometheus → Metrics
Loki       → Logs
```

---

## Why do we need Grafana?

Prometheus and Loki can store/query data, but Grafana provides a unified visualization layer.

---

## Why do we need Alertmanager if Prometheus already has alerts?

Prometheus evaluates alert rules.

Alertmanager handles notification management and routing.

---

## What happens when error rate increases?

```text
Application
     ↓
Prometheus
     ↓
Alert rule
     ↓
HighErrorRate
     ↓
Alertmanager
     ↓
Slack
```

---

## What is P95 latency?

P95 latency is the response time below which approximately 95% of observed requests fall.

It is useful for understanding user-facing latency while reducing the influence of a small number of extreme outliers.

---

# 51. Learning Outcomes

After completing this project, the student should understand:

### Docker

- Containers
- Dockerfiles
- Docker Compose
- Volumes
- Networks
- Environment variables

### Monitoring

- Metrics
- Time-series data
- Prometheus
- PromQL
- Exporters

### Visualization

- Grafana
- Datasources
- Dashboard panels
- Variables
- Queries

### Logging

- Container logs
- Log aggregation
- Loki
- Promtail
- LogQL

### Alerting

- Alert rules
- Alert states
- Alertmanager
- Notification routing
- Slack integration

### DevOps

- Monitoring
- Incident detection
- Troubleshooting
- Container orchestration
- Configuration management

---

# 52. Final Definition of Done

The project is considered complete when all of the following are working:

```text
[✓] Flask application running
[✓] Application containerized
[✓] Docker Compose working
[✓] Prometheus collecting metrics
[✓] Grafana connected to Prometheus
[✓] Loki running
[✓] Promtail collecting logs
[✓] Grafana connected to Loki
[✓] Node Exporter collecting system metrics
[✓] Request latency dashboard
[✓] Error rate dashboard
[✓] CPU/memory dashboard
[✓] Log volume dashboard
[✓] Prometheus alert rules
[✓] Alertmanager
[✓] Slack notifications
[✓] Error simulation
[✓] Latency simulation
[✓] Application-down simulation
[✓] Alert recovery testing
[✓] GitHub repository
[✓] README documentation
[✓] Architecture diagram
[✓] Screenshots
[✓] Demo procedure
[✓] Viva preparation
```

---

# 53. Final Architecture

The completed project will provide an end-to-end monitoring pipeline:

```text
                         ┌─────────────┐
                         │    USER     │
                         └──────┬──────┘
                                │
                                ▼
                     ┌───────────────────┐
                     │ Flask Application │
                     │     Container     │
                     └─────────┬─────────┘
                               │
               ┌───────────────┴───────────────┐
               │                               │
               ▼                               ▼
       ┌──────────────┐                 ┌──────────────┐
       │  Prometheus  │                 │   Promtail   │
       │   Metrics    │                 │     Logs     │
       └──────┬───────┘                 └──────┬───────┘
              │                                │
              │                                ▼
              │                         ┌──────────────┐
              │                         │     Loki     │
              │                         │     Logs     │
              │                         └──────┬───────┘
              │                                │
              └────────────────┬───────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │    Grafana   │
                        │  Dashboards  │
                        └──────────────┘

                               ▲
                               │
                        ┌──────┴───────┐
                        │ Alertmanager │
                        └──────┬───────┘
                               │
                               ▼
                            Slack


                      ┌────────────────┐
                      │ Node Exporter  │
                      │ CPU / Memory   │
                      └───────┬────────┘
                              │
                              ▼
                         Prometheus
```

---

# 54. Project Success Criteria

The project successfully demonstrates an end-to-end observability workflow:

```text
APPLICATION
     ↓
GENERATES METRICS + LOGS
     ↓
┌───────────────────────────┐
│ Metrics → Prometheus      │
│ Logs    → Promtail → Loki │
└───────────────────────────┘
     ↓
GRAFANA
     ↓
VISUALIZATION
     ↓
PROMETHEUS ALERT RULE
     ↓
ALERTMANAGER
     ↓
SLACK
     ↓
INCIDENT NOTIFICATION
```

The final project should therefore demonstrate not only **monitoring**, but the complete cycle of:

**Detect → Analyze → Alert → Notify → Troubleshoot → Recover**

---

# 55. Recommended Implementation Order

Follow this exact order rather than building everything at once:

```text
PHASE 1
Flask Application
      ↓
PHASE 2
Docker Container
      ↓
PHASE 3
Prometheus
      ↓
PHASE 4
Grafana
      ↓
PHASE 5
Loki
      ↓
PHASE 6
Promtail
      ↓
PHASE 7
Node Exporter
      ↓
PHASE 8
Grafana Dashboards
      ↓
PHASE 9
Prometheus Alerts
      ↓
PHASE 10
Alertmanager
      ↓
PHASE 11
Slack
      ↓
PHASE 12
Failure Simulation
      ↓
PHASE 13
Testing
      ↓
PHASE 14
Documentation
      ↓
PHASE 15
GitHub + Final Demo
```

This order minimizes debugging complexity because each layer can be verified before the next layer is introduced.