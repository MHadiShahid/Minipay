# MiniPay Architecture

## Overview

MiniPay is implemented as a small application stack consisting of:

```text
Browser UI
    |
    v
FastAPI Application
    |
    v
PostgreSQL

The same API is also deployed as a containerized workload in Kubernetes.

Application Components
Frontend

The frontend provides the browser-based MiniPay support interface.

Location:

frontend/

It is used by the UI automation suite under:

tests/ui/
API

The API is implemented with FastAPI.

Location:

api/

The API provides:

health checking
customer creation and lookup
payment creation
payment lookup
customer payment history

The application obtains its database connection configuration from environment variables rather than hardcoding credentials.

Database

PostgreSQL is used as the relational database.

The schema is located at:

database/schema.sql

The assessment data contains customers, transactions, and callbacks.

SQL investigations are located under:

sql/
Kubernetes Architecture

The Kubernetes deployment uses the minipay namespace.

                    minipay namespace

              +-----------------------+
              |      API Service      |
              |       :8000           |
              +-----------+-----------+
                          |
                          v
              +-----------------------+
              |    API Deployment     |
              |       FastAPI         |
              +-----------+-----------+
                          |
                          v
              +-----------------------+
              | PostgreSQL Service    |
              |       :5432           |
              +-----------+-----------+
                          |
                          v
              +-----------------------+
              | PostgreSQL Deployment |
              +-----------+-----------+
                          |
                          v
              +-----------------------+
              |    PostgreSQL PVC     |
              +-----------------------+

Kubernetes resources include:

Namespace
API Deployment
API Service
PostgreSQL Deployment
PostgreSQL Service
ConfigMaps
Secret
PersistentVolumeClaim

The API deployment defines:

CPU and memory requests
CPU and memory limits
readiness probe
liveness probe

The PostgreSQL data uses persistent storage through a PVC.

Configuration and Secrets

Non-sensitive configuration is stored in ConfigMaps.

The PostgreSQL password is supplied through a Kubernetes Secret.

The repository contains a Secret example only. The real password is created in the evaluator's environment and is not committed to Git.

Support and Operations

The Python support utility provides transaction diagnostics independently of the browser UI.

Location:

python/

Incident investigation documentation is under:

investigation/

Linux operational evidence is under:

evidence/
Testing

The solution contains:

API tests using pytest
Python diagnostic unit tests
Playwright UI automation
SQL investigation queries
Kubernetes health and rollout validation

The complete Python/API test suite can be run with:

pytest -v
Deployment Flow
Source Code
    |
    v
Docker Image
    |
    v
Kubernetes API Deployment
    |
    v
API Service
    |
    v
PostgreSQL Service
    |
    v
PostgreSQL + Persistent Storage