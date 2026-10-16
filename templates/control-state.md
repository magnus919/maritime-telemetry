# Command and independent-feedback contract

Filled scope example: simulated cabin relay, no hardware binding. Request `lab-1`
asks for `true` at monotonic t=0, expires t=5; feedback timeout 2 s. Both authorization
and interlock must be true. At t=1 a matching observed `true` sampled at t=1 achieves
the request. A pre-command sample, HTTP acceptance or an old retained value does not.

- Actual actuator, path/source and physical feedback channel:
- Permitted range/rate, authorization and interlocks:
- Command identifier ownership, conflict/replay ledger and retention:
- Expiry, timeout, unknown-result and retry policy:
- Manual override/local authority and physical stop route:
- Restart/restore behavior; no automatic replay of uncertain commands:
- Feedback identity/time/quality and independence from command acknowledgment:
- Tests: denied, expired, duplicate, conflicting-ID, lost response, stuck feedback,
  source change, reconnect, override and watchdog:
- Observed states and physical evidence:
- Rollback, authorized scope and unresolved constraints:
