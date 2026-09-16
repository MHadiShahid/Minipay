#!/usr/bin/env bash

set -u

NAMESPACE="${1:-minipay}"

echo "=== MiniPay Health Check ==="
echo "Namespace: $NAMESPACE"
echo

echo "=== Pods ==="
kubectl get pods -n "$NAMESPACE" -o wide
echo

echo "=== Services ==="
kubectl get svc -n "$NAMESPACE" -o wide
echo

echo "=== Endpoints ==="
kubectl get endpoints -n "$NAMESPACE" -o wide
echo

echo "=== Deployments ==="
kubectl get deployments -n "$NAMESPACE"
echo

echo "=== API Health ==="
API_POD="$(kubectl get pods -n "$NAMESPACE" -l app=api -o jsonpath='{.items[0].metadata.name}')"

if [ -n "$API_POD" ]; then
    kubectl exec -n "$NAMESPACE" "$API_POD" -- python -c \
        "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5).read().decode())"
else
    echo "API pod not found"
fi

echo
echo "=== Recent API Logs ==="
kubectl logs -n "$NAMESPACE" deployment/api --tail=20

echo
echo "=== Recent Pod Events ==="
kubectl get events -n "$NAMESPACE" --sort-by='.lastTimestamp' | tail -20