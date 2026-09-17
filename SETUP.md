# MiniPay Setup Guide

### Prerequisites

Ensure you have the following tools installed before getting started:

* **Docker Desktop** & **Docker Compose**
* **Python 3**
* **Git**
* **Node.js** & **npm**
* **kubectl**
* **A running Kubernetes cluster**

---

### Local API Environment

From the repository root:

```bash
docker compose up -d

```

Verify the API health:

```bash
curl http://127.0.0.1:8000/health

```

**Expected result:**

```json
{"status":"ok","database":"connected"}

```

---

### Python Support Tool

Install Python dependencies:

```bash
pip install -r python/requirements.txt

```

Run a transaction diagnostic:

```bash
python python/support_tool.py --transaction TXN00000001

```

Get output in JSON format:

```bash
python python/support_tool.py --transaction TXN00000001 --json

```

Run tests:

```bash
pytest -v

```

---

### Kubernetes Deployment

1. **Build the API image:**
```bash
docker build -t minipay-api:1.0 api .

```


2. **Create the namespace:**
```bash
kubectl apply -f kubernetes/namespace.yaml

```


3. **Create the PostgreSQL Secret locally:**
```bash
kubectl create secret generic postgres-secret -n minipay --from-literal=POSTGRES_PASSWORD=<your_password>

```


> **Note:** Do not commit real passwords to the repository.


4. **Apply PostgreSQL resources:**
```bash
kubectl apply -f kubernetes/postgres-config.yaml
kubectl apply -f kubernetes/postgres-pvc.yaml
kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/postgres-service.yaml

```


5. **Apply API resources:**
```bash
kubectl apply -f kubernetes/api-config.yaml
kubectl apply -f kubernetes/api-deployment.yaml
kubectl apply -f kubernetes/api-service.yaml

```


6. **Verify the deployment:**
```bash
kubectl get pods -n minipay
kubectl get services -n minipay
kubectl get pvc -n minipay

```



---

### Testing

**API Tests:**

```bash
pytest tests/api/test_api.py -v

```

**UI Tests:**

```bash
npm install
npx playwright test

```

*The Playwright report will be generated under `playwright-report/`.*

---

### Documentation & Evidence

* **SQL & Performance:** SQL investigation scripts are under `sql/`. The performance investigation is documented in `sql/PERFORMANCE.md`.
* **Linux Evidence:** Investigation procedures and collected evidence are in `evidence/linux.md`. The repeatable health-check script is `scripts/health-check.sh`.
* **Kubernetes Incidents:** Documented under `investigation/` (includes reproduction steps, symptoms, root cause, remediation, and validation).

---

### Rancher Context

Rancher was investigated as part of the assessment. The local Kubernetes environment runs Kubernetes **v1.37.0**, whereas the targeted Rancher environment supports up to Kubernetes **v1.35**.

A dedicated cluster for Rancher compatibility was not spun up to avoid unnecessary environment sprawl outside the core MiniPay scope. Limitations and intended Rancher operational procedures are documented in the `evidence/` directory.

---

### Reproducibility

All committed manifests, scripts, SQL queries, tests, and documentation allow for full end-to-end reproduction. Real passwords, tokens, private keys, and secrets must be supplied locally and **must not** be committed.