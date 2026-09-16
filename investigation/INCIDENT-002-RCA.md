\# INCIDENT-002 RCA — Kubernetes Application Inaccessible After Deployment



\## Incident Summary



\*\*Incident:\*\* INCIDENT-002

\*\*Severity:\*\* P1

\*\*Area:\*\* Kubernetes deployment / application accessibility

\*\*Status:\*\* Resolved



A deliberately reproduced failure was created using the starter Kubernetes manifest provided with the assessment. The deployment created pods that could not start, and the API Service had no endpoints. The starter manifest contained multiple configuration defects involving the container image, ports, database configuration, and Service selector.



The configuration was corrected and redeployed. The corrected deployment reached 2/2 available replicas, the Service received two endpoints, and the application health endpoint confirmed both application and database connectivity.



\## Observations and Reproduction



The starter manifest was:



`starter/kubernetes/broken-api.yaml`



It was applied with:



```text

kubectl apply -f starter\\kubernetes\\broken-api.yaml

```



The deployment and Service were created successfully, but the resulting pods entered `InvalidImageName` because the container image was:



```yaml

image: YOUR\_IMAGE\_HERE

```



The initial deployment configuration also contained the following mismatches:



| Configuration      | Starter value         | Actual/required value |

| ------------------ | --------------------- | --------------------- |

| Container image    | `YOUR\_IMAGE\_HERE`     | `minipay-api:1.0`     |

| Container port     | `8080`                | `8000`                |

| Readiness probe    | `/health` on `8081`   | `/health` on `8000`   |

| Liveness probe     | `/health` on `8080`   | `/health` on `8000`   |

| Database host      | `minipay-db`          | `postgres`            |

| Service selector   | `app=minipay-backend` | `app=minipay-api`     |

| Service targetPort | `8081`                | `8000`                |



The initial Service had no endpoints because its selector did not match the pod label.



The deployment description showed:



\* 2 desired replicas

\* 0 available replicas

\* `YOUR\_IMAGE\_HERE` as the container image

\* `InvalidImageName` pod failures

\* readiness and liveness probes configured on incorrect ports



\## Evidence



Initial pod state:



```text

minipay-api-66cd6cb98d-pxb65   InvalidImageName

minipay-api-66cd6cb98d-x2qjb   InvalidImageName

```



Initial Service state:



```text

service/minipay-api

selector: app=minipay-backend

endpoints: <none>

```



The deployment therefore could not provide a functioning API workload.



\## Root Cause



The primary root cause was an invalid container image specified by the starter Kubernetes deployment:



```yaml

image: YOUR\_IMAGE\_HERE

```



This prevented Kubernetes from starting the API containers.



Additional configuration defects would also have prevented correct application operation after the image problem was resolved:



1\. The application listens on port `8000`, while the starter manifest declared container/probe ports involving `8080` and `8081`.

2\. The Service selected `app=minipay-backend`, while the Deployment pods were labelled `app=minipay-api`.

3\. The Service targeted port `8081` instead of the application's port `8000`.

4\. The starter database host was `minipay-db`, while the deployed PostgreSQL Service is named `postgres`.

5\. The application requires `DATABASE\_URL` for its database connection, rather than only the starter `DB\_HOST` setting.



These configuration inconsistencies formed a second layer of deployment defects beyond the invalid image.



\## Corrective Action



A corrected deployment was applied using:



```text

kubectl apply -f incident-002-fixed.yaml

```



The corrected configuration:



\* uses image `minipay-api:1.0`

\* exposes container port `8000`

\* uses `DATABASE\_URL`

\* obtains the PostgreSQL password from the existing `postgres-secret`

\* uses `postgres` as the PostgreSQL Service hostname

\* configures readiness and liveness probes against `/health` on port `8000`

\* uses the matching Service selector `app=minipay-api`

\* targets Service traffic to port `8000`



\## Validation



The corrected rollout completed successfully:



```text

deployment "minipay-api" successfully rolled out

```



Final deployment state:



```text

2 desired | 2 updated | 2 total | 2 available | 0 unavailable

```



Both API pods were running with zero restarts:



```text

minipay-api-8559c7c9fc-c46sq   1/1   Running   0

minipay-api-8559c7c9fc-smmb5   1/1   Running   0

```



The Service had two healthy endpoints:



```text

10.244.0.11:8000

10.244.0.12:8000

```



Application health was then checked from inside an API pod:



```text

{"status":"ok","database":"connected"}

```



This confirms that the application started successfully and could connect to PostgreSQL.



\## Preventive Actions



1\. Validate Kubernetes manifests before deployment.

2\. Verify container image names against locally available or registry-published images.

3\. Ensure Deployment labels and Service selectors match.

4\. Verify Service `targetPort` against the actual application listening port.

5\. Verify readiness and liveness probes against an accessible application health endpoint.

6\. Keep application configuration such as database connection settings consistent with the application's actual environment variables.

7\. Use `kubectl describe`, pod status, Service endpoints, rollout status, and application health checks as part of deployment validation.

8\. Add manifest validation and deployment smoke tests to the release workflow where practical.



\## Final Status



\*\*Resolved and validated.\*\*



The corrected Kubernetes deployment reached the required healthy state with 2/2 replicas available, two Service endpoints, and a successful application/database health check.



