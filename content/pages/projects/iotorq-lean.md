Title: ioTORQ LEAN
Date: 2019-04-11 00:00
Authors: me
Summary: Real-time data platform for Lean Manufacturing
Template: project_detail
save_as: projects/iotorq-lean.html
Technologies:python,django,vuejs,azure,sass,javascript,redis,postgresql,kafka,mqtt,docker
Images:projects\LEAN\lean-dashboard.png,projects\LEAN\lean-notification.png,projects\LEAN\lean-report.png
website:<https://panevo.com/software/lean-manufacturing-oee-software/>

### Project Background

At [Panevo](https://www.panevo.com), I built from a scratch the first version of a novel real-time data platform for lean manufacturing, used in fast-moving production lines. Sensors on production lines send data every second to our cloud-based systems, and live metrics are shown in real-time to operators. When the line stops, a notification is shown to the operator so that they enter the cause of the downtime, allowing the company to collect very detailed information about the efficiency of their manufacturing environment.

![Working principle](/images/projects/LEAN/lean-working-principle.png)

Under the hood, data is processed through different backend services (MQTT broker, Kafka, Faust...) with real-time analysis, before being sent to storage (PostgreSQL) and for display in dashboards (Websockets). The platform runs on a cluster of virtual machines in Azure, orchestrated with Kubernetes and Docker Swarm (we are transitioning services from Swarm to AKS and this work is still ongoing).

### Key Features

- Real-time dashboards
- Notification system with automatic alerting and escalation
- Complex reports for data exploration
- Many background jobs and services for data preparation and automatic reports
- Flexible REST API
- Role and Permission management system
- Enterprise Compliance and Security (MFA, SOCII...)
