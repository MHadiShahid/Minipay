# Git Workflow

The assessment was developed incrementally on the `main` branch, with each logical area committed separately.

## Commit Strategy

Changes were grouped by functional area such as API implementation, Python diagnostics, UI/API tests, Kubernetes configuration, SQL investigation, incident RCA, and Linux evidence.

Each commit was kept focused so that individual changes could be reviewed and traced independently.

## Branch and Merge Strategy

The final assessment work was maintained on `main`. No long-lived feature branches were required because this was a single-developer assessment repository. In a team workflow, feature branches would be used for isolated changes and merged into `main` through review.

The final submission is identified by the `submission-v1.0` Git tag.
