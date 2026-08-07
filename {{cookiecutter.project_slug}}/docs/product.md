# Product context

**Status:** Complete this document before implementing substantial product
behavior. Keep it concise, specific, and current. It is the product companion
to `AGENTS.md`; do not store secrets, personal data, temporary tickets, or
implementation diaries here.

## Purpose and boundaries

- **Product outcome:** <!-- What durable outcome does this product create? -->
- **Primary users:** <!-- Who uses it, and what are their roles? -->
- **Primary user journeys:** <!-- Name the important end-to-end workflows. -->
- **Explicit non-goals:** <!-- What must this product not attempt to solve? -->
- **Success measures:** <!-- Observable outcomes, not implementation activity. -->

## Domain language

Use one precise term for each important concept. Add terms before introducing
models, API fields, routes, or UI copy that depend on them.

| Term | Meaning | Avoid |
| --- | --- | --- |
| <!-- Canonical term --> | <!-- Precise meaning --> | <!-- Ambiguous aliases --> |

## Data, security, and retention

- **Data classification:** <!-- Public, internal, confidential, regulated, etc. -->
- **Sensitive data:** <!-- What requires special handling? -->
- **Retention and deletion:** <!-- Ownership, duration, deletion trigger, exceptions. -->
- **Audit requirements:** <!-- What events must be attributable or retained? -->
- **Threats and abuse cases:** <!-- Link the threat model when one exists. -->

## Authorization and external contracts

- **Roles and permissions:** <!-- Who may do what? Include tenant boundaries. -->
- **External systems:** <!-- System, owner, source of truth, direction, and contract. -->
- **Compatibility commitments:** <!-- Public APIs, imports/exports, events, or reports. -->
- **Failure handling:** <!-- User-visible behavior and reconciliation path. -->

## Decisions and references

- **Product ADRs:** <!-- Link relevant files under docs/adr/. -->
- **Specifications:** <!-- Link stable product specifications and wireframes. -->
- **Operational runbooks:** <!-- Link support, recovery, and escalation guidance. -->

When this document changes a lasting technical decision, add or update the
corresponding ADR. Add a nested `AGENTS.md` inside a domain or integration only
when it has local invariants that would make the root guide noisy.
