\# Linux Investigation Evidence



\## 1. Operating System and Kernel



Evidence collected from the MiniPay API container:



```text

PRETTY\_NAME="Debian GNU/Linux 13 (trixie)"

VERSION\_ID="13"

VERSION\_CODENAME=trixie



Kernel:



Linux api-76bbd74467-2xjpc 5.15.167.4-microsoft-standard-WSL2

x86\_64 GNU/Linux



The Kubernetes workloads run in a Debian 13 container on the Docker Desktop WSL2 environment.



2\. CPU and Memory



The container reports:



CPU: AMD Ryzen 5 3600, 6 cores / 12 threads

CPU architecture: x86\_64

Memory available to the Linux environment: approximately 7.7 GiB

Swap: 2 GiB



The API container has Kubernetes resource configuration:



CPU request: 100m

CPU limit: 500m

Memory request: 128Mi

Memory limit: 512Mi

3\. Disk Utilization



API container:



Filesystem      Size  Used Avail Use%

overlay         1007G 9.4G 947G  1%



Container filesystem directory usage:



195M    /

187M    /usr

6.5M    /var

1.3M    /etc

64K     /app

16K     /root



PostgreSQL container also reported approximately 1% filesystem usage.



The PostgreSQL workload additionally uses a Kubernetes PersistentVolumeClaim (postgres-pvc) for database storage.



4\. Kubernetes Workload and Network State



Current workloads:



api-76bbd74467-2xjpc        1/1 Running   0 restarts

postgres-cc49d4488-27kkt    1/1 Running   0 restarts



Services:



api        ClusterIP 10.96.14.43    8000/TCP

postgres   ClusterIP 10.96.232.171  5432/TCP



Endpoints:



api        10.244.0.8:8000

postgres   10.244.0.6:5432



The API container's DNS configuration uses the Kubernetes cluster DNS service:



nameserver 10.96.0.10

search minipay.svc.cluster.local svc.cluster.local cluster.local



The PostgreSQL service resolves successfully:



10.96.232.171 postgres.minipay.svc.cluster.local

5\. Application Health and Logs



The API readiness and liveness probes both use:



GET /health



on port 8000.



Recent application logs contained repeated successful health checks:



"GET /health HTTP/1.1" 200 OK



No application errors were present in the sampled API logs.



The container image does not include wget, so an in-container HTTP request using wget could not be performed. Kubernetes probe results and application logs were used instead.



6\. Processes



The API image is intentionally minimal and does not contain ps, ss, or netstat. Therefore process and listening-port information could not be collected directly from that container.



The PostgreSQL container does provide ps. Its process list showed the expected PostgreSQL processes:



postgres       1  ... postgres

postgres      67  ... postgres: checkpointer

postgres      68  ... postgres: background writer

postgres      70  ... postgres: walwriter

postgres      71  ... postgres: autovacuum launcher

postgres      72  ... postgres: logical replication launcher



No unexpected long-running application processes were observed.



7\. Resource Monitoring Limitation



kubectl top pods -n minipay returned:



error: Metrics API not available



Therefore live Kubernetes CPU/memory utilization could not be collected through the Metrics API in the current local cluster.



The deployment's configured resource requests and limits were verified using kubectl describe pod.



8\. High CPU Investigation Procedure



For a high-CPU incident:



Check pod CPU usage with kubectl top pods -n minipay.

If Metrics Server is unavailable, inspect processes inside the affected container where process tools are available.

Check application logs with kubectl logs.

Check pod events and restart counts with kubectl describe pod.

Compare the observed behavior with the application's workload and recent deployments.

If necessary, capture a process profile or reproduce the workload in a controlled environment.



The current cluster does not expose the Metrics API, so live CPU measurements were unavailable.



9\. Low Disk Investigation Procedure



For a low-disk incident:



Run df -h to identify the affected filesystem.

Run du -xhd1 / and drill into the largest directories.

Inspect application logs for excessive log growth.

Inspect temporary files and caches.

For PostgreSQL, inspect database/PVC utilization separately.

Remove only identified temporary or obsolete data according to the application's retention policy.

Recheck df -h after remediation.



The current containers reported approximately 1% filesystem utilization.



10\. Unreachable API Investigation Procedure



For an unreachable API:



Check pod status and restart count.

Check readiness/liveness probe configuration.

Check Service selector and endpoints.

Check application logs.

Verify DNS resolution of the Service.

Verify the application is listening on the configured container port.

Test the API from inside the cluster.

Inspect recent rollout/deployment events.



The current API has:



Ready=True

zero restarts

Service endpoint 10.244.0.8:8000

healthy /health probe responses

11\. Repeatedly Terminating Process Investigation Procedure



For a process that repeatedly terminates:



Check pod restart count.

Inspect kubectl describe pod events.

Inspect previous-container logs with kubectl logs --previous.

Check liveness probe failures.

Check resource limits for possible OOM termination.

Review recent deployment/configuration changes.

Reproduce the failure if possible.

Correct the underlying configuration or application defect and validate the rollout.



The current API pod has zero restarts and no pod events.



12\. Evidence Limitations



The investigation was performed against the minimal production-style containers already used by the MiniPay deployment. Missing utilities such as wget, ps, and ss were not installed merely for evidence collection.



The Kubernetes Metrics API was also unavailable. These limitations are recorded rather than replaced with inferred measurements.

