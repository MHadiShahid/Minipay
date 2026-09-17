# Kubernetes Findings

## Supplied Starter Manifest

The assessment supplied `starter/kubernetes/broken-api.yaml` as a deliberately broken Kubernetes manifest.

The manifest was reviewed before applying the corrected MiniPay deployment.

## Identified Defects

### 1. Invalid Container Image

The starter Deployment references an image that is not available in the local environment.

**Impact:** The API pod cannot start successfully if the image cannot be pulled.

**Correction:** Use the locally built `minipay-api:1.0` image and load it into the Kind cluster.

### 2. Incorrect Readiness Probe Port

The starter readiness probe checks `/health` on port `8081`.

The MiniPay API listens on port `8000`.

**Impact:** The container may be running but will not become Ready because the readiness probe cannot reach the application.

**Correction:** Configure the readiness probe to use `/health` on port `8000`.

### 3. Incorrect Liveness Probe Configuration

The starter manifest uses a different port configuration from the actual API listener.

**Impact:** Kubernetes may incorrectly consider a healthy API container unhealthy and restart it.

**Correction:** Configure the liveness probe to use `/health` on port `8000`.

### 4. Service Selector Mismatch

The Deployment uses the application label:

```text
app: minipay-api
```

while the Service selector uses:

```text
app: minipay-backend
```

**Impact:** The Service does not select the API pods and therefore has no usable backend endpoints.

**Correction:** Make the Service selector match the API Deployment labels.

### 5. Incorrect Service Target Port

The starter Service targets port `8081`, while the API listens on port `8000`.

**Impact:** Even if the Service selects the correct pods, traffic is sent to the wrong port.

**Correction:** Set the Service `targetPort` to `8000`.

### 6. Incorrect Database Configuration

The starter configuration does not match the database service name used by the Kubernetes deployment.

**Impact:** The API cannot establish its PostgreSQL connection.

**Correction:** Use the Kubernetes PostgreSQL Service name:

```text
postgres
```

and the database:

```text
minipay
```

### 7. Missing/Incorrect Environment Configuration

The starter configuration does not provide the API with the required database connection configuration in the form expected by the application.

**Impact:** The API cannot connect to PostgreSQL even when both workloads are running.

**Correction:** Configure `DATABASE_URL` using Kubernetes environment configuration and supply the password through a Kubernetes Secret.

## Validation

After correcting the configuration, the Kubernetes deployment was validated using:

```text
kubectl get pods -n minipay
kubectl rollout status deployment/api -n minipay
kubectl get services -n minipay
kubectl get endpoints -n minipay
kubectl logs -n minipay <api-pod>
```

The API reached the Ready state and the Service obtained API pod endpoints.

The application health endpoint returned:

```json
{"status":"ok","database":"connected"}
```

This confirmed both API availability and API-to-PostgreSQL connectivity.

## Operational Lesson

The incident demonstrates why Kubernetes troubleshooting should validate the complete path:

```text
Deployment
    ↓
Pod
    ↓
Container port
    ↓
Readiness/Liveness probes
    ↓
Service selector
    ↓
Service targetPort
    ↓
Application
    ↓
Database Service
    ↓
PostgreSQL
```

A pod being `Running` does not by itself prove that the application is reachable or healthy.
