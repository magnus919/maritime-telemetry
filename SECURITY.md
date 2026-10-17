# Security policy

## Supported versions

Security fixes target the current `main` branch. Older snapshots and example
builds do not receive separate backports. If a report affects an older revision,
include that revision and whether you can reproduce it on current `main`.

## Report a vulnerability privately

Email [magnus919@pm.me](mailto:magnus919@pm.me) or use
[GitHub's private vulnerability reporting form](https://github.com/magnus919/maritime-telemetry/security/advisories/new),
or open the repository's **Security → Advisories → Report a vulnerability** page.
Do not put exploit details, credentials or private captures in a public issue or PR.
For help using the form, see [GitHub's reporting instructions](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately).

Include what you can:

- Affected repository commit, file/example and dependency versions.
- The vulnerability, potential impact and prerequisites.
- A minimal reproduction using synthetic data or a system you own and control.
- Suggested mitigations and your preference for credit or anonymity.

Only provide the information needed to investigate. Remove real vessel locations,
MMSIs, serial numbers and secrets from attachments. Do not test against someone
else's boat, radio, server or account. An isolated software reproduction is useful;
a live-vessel demonstration is not required.

If the private form becomes unavailable, email [magnus919@pm.me](mailto:magnus919@pm.me)
instead. Keep vulnerability details out of public issues.

## What belongs here

Report vulnerabilities in the scripts, examples, dependency integration or guidance
maintained here, including credential exposure, unauthorized command paths and
instructions that create an exploitable configuration. Ordinary factual corrections
and non-security bugs can use the public issue forms. If you are unsure whether a
problem is security-sensitive, start privately.

For an upstream library or commercial device vulnerability, report to its maintainer
or vendor as well. Tell us privately when an example here is affected so its guidance
or dependency pin can be corrected; this project cannot promise an upstream fix.

## Handling and disclosure

Maintainers will assess reports, request enough information to reproduce the issue,
and coordinate a fix or documented mitigation where feasible. Please coordinate
public disclosure until maintainers have had a reasonable opportunity to investigate.
Response and remediation times depend on maintainer availability; this project has
no guaranteed response schedule or paid bug-bounty program. Credit is discussed
with the reporter before publication.
