# MiniPay Setup Guide

## Prerequisites

Install:

- Docker Desktop
- Docker Compose
- Python 3
- Git
- Node.js/npm
- kubectl
- A Kubernetes cluster

## Local API Environment

From the repository root:

docker compose up -d

Verify the API:

curl http://127.0.0.1:8000/health

Expected result:

{"status":"ok","database":"connected"}
Python Support Tool

Install Python dependencies:

pip install -r python/requirements.txt

Run a transaction diagnostic:

python python/support_tool.py --transaction TXN00000001

JSON output:

python python/support_tool.py --transaction TXN00000001 --json

Run tests:

pytest -v
Kubernetes

Build the API image:

docker build -t minipay-api:1.0 .

Create the namespace:

kubectl apply -f kubernetes/namespace.yaml

Create the PostgreSQL Secret locally:

kubectl create secret generic postgres-secret -n minipay --from-literal=POSTGRES_PASSWORD=<password>

Do not commit the real password.

Apply the PostgreSQL resources:

kubectl apply -f kubernetes/postgres-config.yaml
kubectl apply -f kubernetes/postgres-pvc.yaml
kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/postgres-service.yaml

Apply the API resources:

kubectl apply -f kubernetes/api-config.yaml
kubectl apply -f kubernetes/api-deployment.yaml
kubectl apply -f kubernetes/api-service.yaml

Verify:

kubectl get pods -n minipay
kubectl get services -n minipay
kubectl get pvc -n minipay
API Tests

Run:

pytest tests/api/test_api.py -v
UI Tests

Install dependencies:

npm install

Run:

npx playwright test

The Playwright report is generated under playwright-report/.

SQL

The SQL investigation scripts are under:

sql/

The performance investigation is documented in:

sql/PERFORMANCE.md
Linux Evidence

Linux investigation procedures and collected evidence are documented in:

evidence/linux.md

The repeatable health-check script is:

scripts/health-check.sh
Kubernetes Incidents

Incident investigations are documented under:

investigation/

They contain reproduction steps, observed symptoms, root cause, remediation, and validation.

Rancher

Rancher was investigated as part of the assessment. The local Kubernetes environment used for the implementation runs Kubernetes 1.37.0, while the Rancher environment considered for the assessment had a certified Kubernetes support range ending at 1.35.

A second cluster could be created specifically for Rancher compatibility, but this was not pursued because it would introduce a separate environment that was not required for the core MiniPay implementation.

The limitation and intended Rancher operational procedure are documented separately in the evidence directory.

Reproducibility

The committed manifests, scripts, SQL queries, tests, and documentation are intended to allow the evaluator to reproduce the implementation and investigations.

Real passwords, tokens, private keys, and other secrets must be supplied locally and must not be committed.