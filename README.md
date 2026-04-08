# Urlshrink - DevOps & Cloud Infrastructure

This project implements a cloud-native deployment of a Django-based URL shortener, focusing on high availability, scalability, and automated infrastructure management.

## Technology Stack

*   **Application**: Django (Python)
*   **Containerization**: Docker
*   **Orchestration**: Amazon EKS (Kubernetes)
*   **Container Registry**: Amazon ECR
*   **Monitoring**: Prometheus & Grafana (via Helm)
*   **Infrastructure Management**: `eksctl`, `kubectl`, `helm`

## DevOps Implementation Details

### 1. Orchestration & Scalability
The application is deployed on **Amazon EKS**, utilizing Kubernetes for automated scaling and self-healing. The deployment uses a replica-based strategy to ensure high availability across the cluster.

### 2. Configuration & Secret Management
Security is prioritized by decoupling configuration from code:
*   **Kubernetes Secrets**: Used to manage the Django `SECRET_KEY` and ECR pull credentials.
*   **Environment Variables**: Dynamic configuration for `DEBUG` mode and `ALLOWED_HOSTS`.

### 3. Networking & Load Balancing
*   **Service Type**: `LoadBalancer` exposes the application to the internet via an AWS Classic/Network Load Balancer.
*   **Port Mapping**: External traffic on port 80 is routed to the Django container on port 8000.

### 4. Observability & Monitoring
Integrated monitoring using the **Kube-Prometheus-Stack**:
*   **Prometheus**: Collects metrics from the cluster and application pods.
*   **Grafana**: Provides visualization dashboards for resource utilization and system health.
*   **ServiceMonitors**: Configured to automatically discover and scrape application metrics.

### 5. Infrastructure as Code (IaC)
Infrastructure provisioning is streamlined using `eksctl` with configuration files, ensuring that the EKS cluster setup is repeatable and consistent across environments.

[!Infrastructure Status](https://aws.amazon.com/eks/)
[!Containerized](https://www.docker.com/)
