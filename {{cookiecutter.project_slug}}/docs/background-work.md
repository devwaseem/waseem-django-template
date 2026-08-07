# Background work

{% if cookiecutter.enable_celery == "yes" %}
Celery is configured for late acknowledgements, worker-loss rejection, one task
prefetched at a time, bounded exponential retries, bounded time limits, and
request-ID propagation. These settings favor recovery over silent loss, but
they deliberately do **not** claim exactly-once delivery.

## Delivery contract

- A task can execute more than once. Treat transport delivery as
  **at-least-once**.
- Build an **effectively-once business outcome** with a durable idempotency key,
  database uniqueness/conditional writes, and a transactional outbox or inbox
  whenever a database write crosses a broker or another service boundary.
- Pass the same idempotency key to an external provider when it supports one.
  Persist the provider reference before treating the operation as complete.
- Use **at-most-once** only for explicitly disposable work such as best-effort
  metrics, and document that loss is acceptable. Do not add automatic retries
  to it.
- Do not call a task "exactly once", "always once", or "almost once". Those
  are outcome goals with trade-offs, not guarantees Celery can provide.

## Task rules

- A task only validates stable IDs, establishes correlation, invokes an
  idempotent domain operation, and reports success or failure. It does not own
  business policy.
- Set explicit connect/read/write timeouts for every network call. Make retries
  bounded and restricted to proven transient errors; never retry validation,
  authorization, or permanent provider failures blindly.
- Make task execution safe if it stops after an external side effect but before
  acknowledgement. Prefer an outbox record committed with the domain change,
  then publish it separately.
- Keep transactions short. Never hold a database transaction open while making
  a network request. Claim work with an explicit state transition or row lock,
  then commit its terminal state atomically.
- Send only small, versioned primitive payloads. Do not serialize requests,
  model instances, secrets, or unbounded data sets.
- Give long-running or resource-heavy work a deliberate queue, concurrency,
  and deployment policy once the product needs it; the template's default queue
  is intentionally conservative, not a universal topology.
{% else %}
Celery is intentionally not installed for this project. Adding background work
requires an ADR that defines delivery semantics, idempotency, retry policy,
timeouts, operational ownership, and failure handling.
{% endif %}
