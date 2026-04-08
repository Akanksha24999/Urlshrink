# AWS EKS Deployment Guide for Urlshrink

## Prerequisites
- AWS Account with ECR and EKS access
- `kubectl` installed and configured
- `aws-cli` installed and configured
- Docker installed locally

## Step 1: Push Docker Image to AWS ECR

### 1.1 Create ECR Repository
```bash
aws ecr create-repository \
  --repository-name urlshrink \
  --region ap-south-1
```

### 1.2 Get ECR Login Token
```bash
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com
```

### 1.3 Tag and Push Image
```bash
docker tag urlshrink:latest <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/urlshrink:latest
docker push <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/urlshrink:latest
```

## Step 2: Create/Configure EKS Cluster

### 2.1 Create EKS Cluster (if not already created)
Recommended: Use the configuration file for consistency.
```bash
eksctl create cluster -f k8s/cluster.yaml
```

### 2.2 Configure kubectl context
```bash
aws eks update-kubeconfig \
  --region ap-south-1 \
  --name urlshrink-new-cluster
```

### 2.3 Verify connection
```bash
kubectl get nodes
```

## Step 3: Create ECR Secret for EKS

```bash
kubectl create secret docker-registry ecr-secret \
  --docker-server=<ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region ap-south-1) \
  --namespace urlshrink
```

## Step 4: Update Kubernetes Manifests

1. **deployment.yaml**: Replace <`ACCOUNT_ID`> and `ap-south-a` with your actual values:
   ```yaml
   image: <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/urlshrink:latest
   ```

2. **service.yaml**: No additional changes are required for the service manifest.

## Step 5: Deploy to EKS

```bash

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Step 6: Verify Deployment

```bash
# Check deployment status
kubectl get deployments -n urlshrink

# Check pods
kubectl get pods -n urlshrink

# Check service and get Load Balancer URL
kubectl get service -n urlshrink

# View logs
kubectl logs -n urlshrink -l app=urlshrink --tail=50 -f
```

## Step 7: Access Your Application

Once the LoadBalancer service has an external IP/hostname:
```bash
kubectl get service urlshrink-service -n urlshrink
```

Visit the `EXTERNAL-IP` or hostname in your browser at `http://<EXTERNAL-IP>`

## Setting up Monitoring

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
kubectl create namespace monitoring
helm install kube-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false
```

## Useful Commands

```bash
# Delete deployment
kubectl delete -f k8s/

# Scale replicas
kubectl scale deployment urlshrink -n urlshrink --replicas=5

# Restart pods
kubectl rollout restart deployment/urlshrink -n urlshrink

# Port-forward for local testing
kubectl port-forward -n urlshrink svc/urlshrink-service 8000:80

# Get detailed pod information
kubectl describe pod <POD_NAME> -n urlshrink

# SSH into a pod
kubectl exec -it <POD_NAME> -n urlshrink -- /bin/bash
```

## Troubleshooting

- **ImagePullBackOff**: Check ECR secret and image path
- **CrashLoopBackOff**: Check pod logs with `kubectl logs`
- **Pending**: Check pod events for scheduling failures:
  ```bash
  kubectl describe pod <pod-name> -n urlshrink
  ```
  Common causes: Insufficient CPU/Memory, PVC binding issues, or node taints.
- **Connection refused**: Verify Security Groups allow port 8000

## Clean Up

```bash
# Delete EKS cluster
eksctl delete cluster --name urlshrink-new-cluster --region ap-south-1

# Delete ECR repository
aws ecr delete-repository --repository-name urlshrink --region ap-south-1 --force
```
