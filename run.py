#!/usr/bin/env python3
"""Enterprise Cryptographic Discovery & Analysis Tool (SIH26164). Name: see brand.json.

Usage:
    python run.py                      # start the app at http://127.0.0.1:8765
    python run.py scan <path|git-url>  # command-line scan
        [--cbom out.json] [--sarif out.sarif] [--fail-on critical|high|medium]
"""
import os
import sys
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
sys.path.insert(0, HERE)

REQUIRED = {"flask": "flask", "cryptography": "cryptography"}
OPTIONAL = {"jsonschema": "jsonschema (CBOM schema validation)"}


def check_deps():
    missing = []
    for mod, pkg in REQUIRED.items():
        try:
            __import__(mod)
        except ImportError:
            missing.append(pkg)
    if missing:
        print("Missing packages. Install with:\n    pip install " + " ".join(missing))
        sys.exit(1)
    for mod, what in OPTIONAL.items():
        try:
            __import__(mod)
        except ImportError:
            print(f"note: optional package missing - {what}. pip install {mod}")


def cli_scan(argv):
    import json
    from core.engine import Scan
    from core.export.cbom import build_cbom, validate
    from core.export.sarif import build_sarif
    target = argv[0]
    args = dict(zip(argv[1::2], argv[2::2]))
    s = Scan(target).run()
    if s.status != "done":
        print("scan failed:", s.error)
        sys.exit(2)
    sm = s.summary()
    from core.brand import NAME
    print(f"{NAME}  {sm['files']} files  {sm['total']} crypto assets  {sm['duration']}s")
    for k in ("broken", "vulnerable", "weakened", "safe", "inventory"):
        print(f"  {k:<11}{sm['classes'].get(k, 0)}")
    print("\nTop priorities:")
    for f in s.findings[:10]:
        dl = ", ".join(d["label"] for d in f.data_links)
        print(f"  [{f.risk['priority']:>3}] {f.risk['class']:<10} {f.display_name:<22} {f.location}:{f.line}  {dl}")
    if "--cbom" in args:
        bom = build_cbom(s)
        ok, errs = validate(bom)
        json.dump(bom, open(args["--cbom"], "w"), indent=2)
        print(f"\nCBOM written to {args['--cbom']} (CycloneDX 1.6, schema valid: {ok})")
    if "--sarif" in args:
        json.dump(build_sarif(s), open(args["--sarif"], "w"), indent=2)
        print(f"SARIF written to {args['--sarif']}")
    fail = args.get("--fail-on")
    if fail:
        order = ["low", "medium", "high", "critical"]
        worst = max((order.index(f.risk["severity"]) for f in s.findings if f.risk["severity"] in order), default=-1)
        if worst >= order.index(fail):
            sys.exit(3)


if __name__ == "__main__":
    check_deps()
    if len(sys.argv) > 2 and sys.argv[1] == "scan":
        cli_scan(sys.argv[2:])
    else:
        from core.api import serve
        from core.brand import NAME
        port = int(os.environ.get("APP_PORT", "8765"))
        url = f"http://127.0.0.1:{port}"
        print(f"{NAME} running at {url}  (Ctrl+C to stop)")
        if not os.environ.get("NO_BROWSER"):
            try:
                webbrowser.open(url)
            except Exception:
                pass
        serve(port=port)
