Title: ioTORQ LEAN
Date: 2019-04-11 00:00
Authors: me
Summary: Real-time data platform for Lean Manufacturing
Template: project_detail
save_as: projects/iotorq-lean.html
Technologies:python,django,vuejs,azure,sass,javascript,redis,postgresql,kafka,mqtt,docker
Images:projects\LEAN\lean-dashboard.png,projects\LEAN\lean-notification.png,projects\LEAN\lean-report.png
website: https://panevo.com/software/lean-manufacturing-oee-software/

### Real-time lean manufacturing and production performance platform

ioTORQ LEAN is a real-time data platform designed to help industrial operators and manufacturing teams understand, monitor, and improve production performance on the factory floor.

The platform continuously collects high-frequency signals from production lines and assets, transforms them into live metrics, and presents them through dashboards used directly by operators, supervisors, and managers. As a product moves through a line, the corresponding metrics update in real time, allowing teams to immediately see the impact of stoppages, speed changes, or production events.

ioTORQ LEAN focuses on core lean manufacturing use cases such as real-time production tracking, downtime detection, and performance monitoring. It enables teams to identify losses as they happen, rather than relying on delayed reports or manual data collection, and supports continuous improvement efforts across single lines or multiple sites.

### Real-time constraints and platform complexity

Unlike traditional reporting or batch analytics systems, ioTORQ LEAN operates under strict real-time constraints.

The platform is designed for 24/7 industrial environments where operators expect sub-second latency between what happens on the production line and what they see on screen. When a product enters, stops, or exits a process, the live dashboard must reflect that change immediately. This imposes strong requirements on data ingestion, processing, and delivery, as well as on system reliability.

The platform handles continuous data streams, real-time metric calculations, and live dashboards while maintaining high availability and predictable performance.

### Project and technical ownership

I started building ioTORQ LEAN from scratch, initially working hands-on as the primary architect and developer alongside one other engineer. The first versions of the platform were designed, implemented, and deployed under tight timelines and limited resources, serving real industrial users in production environments within 8 months.

As adoption grew, I led the evolution of the platform architecture to support increased data volumes, additional use cases, and multi-site deployments. This included designing scalable real-time data pipelines and ensuring the system could operate reliably in 24/7 industrial settings.

I later hired and scaled the engineering team responsible for the platform, transitioning from direct implementation to technical leadership, architecture oversight, and product direction. 

### Key Features

- Real-time dashboards
- Notification system with automatic alerting and escalation
- Complex reports for data exploration
- Many background jobs and services for data preparation and automatic reports
- Flexible REST API
- Role and Permission management system
- Enterprise Compliance and Security (MFA, SOCII...)
