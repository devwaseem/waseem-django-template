# 1. Keep platform and product code separate

## Status

Accepted.

## Context

Cruft updates need a small, stable template-owned surface while products need
freedom to evolve.

## Decision

Keep generated infrastructure in the project namespace and product behavior in
`domains/`, with registry and scaffold commands as the explicit extension
points.

## Consequences

Product changes avoid template-owned files where possible, making upgrades
smaller and easier to review.
