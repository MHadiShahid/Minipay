# MiniPay - Implementation & L2 Support Engineer Assessment

MiniPay is a small payment-processing application used to demonstrate API development, SQL investigation, Kubernetes deployment, Python support tooling, automated testing, Linux troubleshooting, and incident investigation.

## Repository Structure

- `api/` - FastAPI application
- `database/` - database schema
- `frontend/` - browser UI
- `kubernetes/` - Kubernetes manifests
- `python/` - support diagnostic utility
- `sql/` - SQL investigations and performance analysis
- `tests/api/` - API automation
- `tests/ui/` - Playwright UI automation
- `investigation/` - incident RCA documents
- `evidence/` - Linux and Git evidence
- `scripts/` - repeatable support scripts
- `requirements/` - assessment requirements

## Prerequisites

- Docker Desktop
- Docker Compose
- Python 3
- Git
- kubectl
- A Kubernetes cluster capable of running the manifests
- Node.js/npm for UI tests

## Local Application

Install Python dependencies:

    pip install -r python/requirements.txt

Start the application dependencies:

    docker compose up -d

The API is available at:

    http://127.0.0.1:8000

Health check:

    curl http://127.0.0.1:8000/health

## Python Support Tool

Example:

    python python/support_tool.py --transaction TXN00000001

JSON output:

    python python/support_tool.py --transaction TXN00000001 --json

Run Python tests:

    pytest python/tests -v

## API Tests

Install test dependencies as required by the project environment and run:

    pytest tests/api/test_api.py -v

Run the complete Python/API test suite:

    pytest -v

## UI Tests

Install Node dependencies:

    npm install

Run Playwright tests:

    npx playwright test

The Playwright report is generated under `playwright-report/`.

## Kubernetes

Create the namespace:

    kubectl apply -f kubernetes/namespace.yaml

Create the PostgreSQL Secret locally. Do not commit the real password:

    kubectl create secret generic postgres-secret -n minipay --from-literal=POSTGRES_PASSWORD=<password>

Apply the remaining manifests:

    kubectl apply -f kubernetes/postgres-config.yaml
    kubectl apply -f kubernetes/postgres-pvc.yaml
    kubectl apply -f kubernetes/postgres-deployment.yaml
    kubectl apply -f kubernetes/postgres-service.yaml
    kubectl apply -f kubernetes/api-config.yaml
    kubectl apply -f kubernetes/api-deployment.yaml
    kubectl apply -f kubernetes/api-service.yaml

Check deployment status:

    kubectl get pods -n minipay
    kubectl get deployments -n minipay
    kubectl get services -n minipay

The repository contains `kubernetes/postgres-secret.example.yaml` as a configuration example. Real passwords should be supplied through the cluster and must not be committed.

## SQL Investigation

SQL investigation scripts are located under `sql/`.

The performance investigation and before/after query-plan evidence are documented in:

    sql/PERFORMANCE.md

## Linux Evidence

Linux investigation procedures and collected evidence are documented in:

    evidence/linux.md

The repeatable health-check script is:

    scripts/health-check.sh

## Incident Investigation

Incident RCA documents are located under:

    investigation/

They document controlled reproduction, observed symptoms, root cause, remediation, and validation.

## Git

The assessment was developed through incremental commits organized by logical work areas.

The final submission is identified by the Git tag:

    submission-v1.0

## AI Usage

AI assistance and the validation process are documented in:

    AI_USAGE.md

AI-generated suggestions were validated by executing the relevant commands, tests, queries, deployments, and troubleshooting procedures in the assessment environment.