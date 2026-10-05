# Aegis

![Aegis overview: pipeline, worked Aadhaar example, results and tech stack](docs/overview/aegis-overview.png)

**SIH 2026 · SIH26164 · Enterprise Cryptographic Discovery & Analysis Tool (NTRO)**

Aegis finds every cryptographic asset in code, binaries, container images, certificates, keystores and configuration,
traces **which data each one protects**, and dates its quantum risk from **published expert data**. It recommends the
right post-quantum replacement for how each key is used, can patch and verify supported cases, and exports a
schema-valid **CycloneDX 1.6 CBOM**. It runs entirely on one machine with no internet access.

## Run it

Needs Python 3.10+. Easiest: double-click **Start Aegis (Windows).bat** or **Start Aegis (Mac).command**. The first run installs
three packages (needs internet once); after that it starts offline and opens http://127.0.0.1:8765.

Or from a terminal:

```bash
pip install -r requirements.txt      # flask, cryptography, jsonschema
python run.py                        # opens http://127.0.0.1:8765
```

Command line / CI:

```bash
python run.py scan ./service --cbom cbom.json --sarif aegis.sarif --fail-on critical
```

Tests: `python -m unittest discover -s tests` (engine, 33 tests) · `python tests/ui_robot.py` (clicks every control in the UI) ·
`python bench/score.py` (accuracy against hand-labelled open-source code) ·
`unshare -rn bash tools/offline_proof/offline.sh` (everything again with no network at all).

## What it does, by stage

| Stage | Screens | What happens |
|---|---|---|
| Discover | New scan, Inventory | 7 detector families: Python AST + taint, Java / JS / C / Go lexers, ELF binaries, certificates and keys (PEM, DER, OpenSSH, PKCS#12, JKS), configuration (nginx, Apache, HAProxy, OpenSSL, SSH, Kubernetes, Terraform / KMS), dependency manifests (8 ecosystems), plus an opt-in live TLS endpoint check |
| Link and assess | Overview, Data at risk, Quantum timeline, Systems | Data-flow linking to Aadhaar / PAN / health / eSign / financial data; Mosca's X + Y vs Z per asset; probability of exposure from the GRI 2025 survey curve; per-algorithm arrival via the qubit ladder; business criticality rules; crypto-agility |
| Migrate and prove | Replacements, Fix and verify, Migration plan, Reports | Usage-aware FIPS 203/204/205 recommendations with key sizes, TLS handshake cost and client support; automatic patch + tests + re-scan (prototype); DST-aligned phased plan; CBOM, SARIF, CSV / Markdown, board report |
| Shared | Compare scans, Data sources, Policy | Scan history and diffs, file-hash cache, every bundled source with its snapshot date, editable assumptions |

## Public data bundled for offline use (rebuild with `tools/`)

| Data | Source | Used for |
|---|---|---|
| 458 crypto-library advisories | GitHub Advisory Database (CC-BY-4.0) | vulnerable library versions and upgrade targets |
| Quantum arrival survey | Global Risk Institute, *Quantum Threat Timeline Report 2025* (Mosca & Piani, 26 experts) | the arrival curve: 10% by 2030, 25% by 2033, 50% by 2037 |
| Logical-qubit formulas | Häner et al. 2017 (RSA, 2n+2); Roetteler et al. 2017 (ECC, 9n+2⌈log₂n⌉+10) | which algorithms fall first |
| 374 cipher suites, 57 groups | IANA registry via testssl.sh | naming suites, spotting static-RSA key exchange |
| Server-side TLS guidelines 6.0 | Mozilla | profile check of every TLS config |
| 177 real client handshakes | Qualys SSL Labs list via testssl.sh | real ClientHello sizes; which clients already send X25519MLKEM768 |
| Cryptography registry | CycloneDX | registry family names in the CBOM |

## Honest limits

- Deep data-flow tracing is Python (one inter-procedural hop); other languages get API-level detection.
- Data types are inferred from names and value formats (Aadhaar Verhoeff, PAN, IFSC, UPI) with a confidence score.
- Auto-patching covers Python RSA encryption and MD5 / SHA-1 hashing; the hybrid envelope uses a pure-Python
  reference ML-KEM (prototype; production uses liboqs / OpenSSL 3.5+).
- Binaries: ELF only. Quantum arrival is a fitted distribution of expert opinion, not a prediction.

## Renaming

Edit `brand.json`; the UI, reports, CBOM tool name and command line all read it.

Third-party code and data: kyber-py and dilithium-py (MIT), pyelftools (public domain),
CycloneDX schema and registry (Apache-2.0), IBM Plex Sans and IBM Plex Mono fonts (SIL OFL 1.1, `web/fonts/`),
testssl.sh data (GPLv2), Mozilla guidelines (MPL-2.0), GitHub Advisory Database (CC-BY-4.0).
