> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase4A external-tool bounded lab run
Generated: 2026-05-20T11:53:48Z
Target: http://<lab-ip>:3000
Limits: red-team Kali only; local lab; httpx metadata only; katana depth=1; low rate; no raw body; no callback; no nuclei/ffuf/exploit scripts

## Pre-health
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Feature-Policy: payment 'self'
X-Recruiting: /#/jobs
Accept-Ranges: bytes
Cache-Control: public, max-age=0
Last-Modified: Wed, 20 May 2026 11:21:10 GMT
ETag: W/"26af-19e451e3e27"
Content-Type: text/html; charset=UTF-8
Content-Length: 9903

## Counts
httpx_lines=1
katana_lines=17

## Post-health
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Feature-Policy: payment 'self'
X-Recruiting: /#/jobs
Accept-Ranges: bytes
Cache-Control: public, max-age=0
Last-Modified: Wed, 20 May 2026 11:21:10 GMT
ETag: W/"26af-19e451e3e27"
Content-Type: text/html; charset=UTF-8
Content-Length: 9903

## Files
httpx.jsonl
httpx.stderr
katana.jsonl
katana.stderr
katana.stdout
summary.md
targets.txt
