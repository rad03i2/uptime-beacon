# Security Policy

## Supported version
The latest release is supported.

## Reporting
Please report suspected vulnerabilities privately through GitHub's security reporting features when available. Do not publish credentials, private URLs, tokens, or sensitive infrastructure details in public issues.

## Design notes
Uptime Beacon only accepts HTTP(S) URLs and rejects URLs with embedded credentials. It does not persist response bodies, cookies, credentials, or telemetry. Operators are responsible for choosing targets they are authorized to monitor. Because HTTP requests can reach internal services, do not expose an untrusted wrapper around this CLI without SSRF controls.
