# AI Usage

AI tools were used as development and troubleshooting assistants during the assessment.

## Tool Used

- ChatGPT

## Areas Where AI Assistance Was Used

AI assistance was used for:

- understanding and organizing the assessment requirements;
- troubleshooting Docker and Kubernetes configuration;
- reviewing Kubernetes manifests;
- designing and reviewing SQL investigations;
- structuring the Python transaction diagnostic utility;
- designing API and UI automated tests;
- investigating Linux operational issues;
- documenting incident root-cause analysis;
- reviewing Git workflow and final submission requirements.

## Representative Interaction Summaries

### 1. Kubernetes troubleshooting

AI assistance was used to investigate Kubernetes startup and deployment problems, including API readiness, service selectors, container ports, probes, and database connectivity.

The suggested commands and configuration changes were executed against the local cluster. Kubernetes pod status, rollout status, service endpoints, logs, and health responses were used to validate the results.

### 2. Kubernetes incident investigation

AI assistance was used to analyze the deliberately broken starter Kubernetes manifest.

The identified defects were independently reproduced, including the invalid image, incorrect ports and probes, incorrect database host, selector mismatch, and incorrect configuration variable.

The corrected temporary deployment was then applied and validated through rollout status, pod readiness, service endpoints, and API health checks.

### 3. SQL performance investigation

AI assistance was used to structure a before/after SQL performance investigation for transaction-reference lookup.

The baseline query was executed with `EXPLAIN (ANALYZE, BUFFERS)`. An index was then added and the query was executed again.

The observed execution plan changed from a sequential scan to an index scan, with the measured execution time and buffer usage recorded in `sql/PERFORMANCE.md`.

### 4. Incident RCA

AI assistance was used to structure incident investigation documents around controlled defect reproduction.

For example, an API lookup defect was intentionally injected, the resulting HTTP 500 behavior was reproduced, and the original implementation was restored afterward.

The RCA documents contain the actual commands, observed behavior, root cause, remediation, and validation rather than treating AI suggestions as evidence.

### 5. Submission and documentation review

AI assistance was used to review the repository against the assessment requirements, including reproducibility, Git history, evidence, automated tests, AI usage documentation, and secret handling.

The repository contents and Git state were checked directly before making the final documentation changes.

## Validation of AI-Generated Output

AI-generated suggestions were not treated as evidence by themselves.

Commands, tests, SQL queries, Kubernetes operations, logs, API responses, and application behavior were executed in the local assessment environment before being documented.

The final test suite was executed with:

```text
pytest -v

```

and completed with:

20 passed

Kubernetes deployments were also validated using pod status, rollout status, service endpoints, health checks, and logs.

Example of Correcting AI Output

During Kubernetes configuration work, an initial configuration approach used the existing Secret manifest containing a test password.

The assessment instructions explicitly prohibit publishing passwords. This was identified during the final repository review.

The committed Secret manifest was removed and replaced with a non-secret example containing CHANGE_ME. The actual password remains supplied through the local Kubernetes environment rather than being committed to Git.

This demonstrates that AI-assisted implementation suggestions were reviewed against the actual assessment requirements and changed when necessary.