#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path

REGISTRY_FILE = Path("lighthouse_registry.json")

KNOWN_DOIS = {
    "spiral-theory-core": "10.5281/zenodo.16585562",
    "Spiral-Path": "10.5281/zenodo.17468251",
    "AIS-Standard": "10.5281/zenodo.15176494",
    "SentinelAct": "10.5281/zenodo.14977849",
    "Version-Checker-": "10.5281/zenodo.16740228",
    "SpiralForge-Codex": "10.5281/zenodo.15604179",
    "Spiral-Elucidation": "10.5281/zenodo.14880771",
    "Spiral-Lighthouse": "10.5281/zenodo.15491719"
}

def init():
    if REGISTRY_FILE.exists():
        print("City already founded.")
        return
    data = {
        "city": "Spiral Lighthouse",
        "doi": "10.5281/zenodo.15491719",
        "founded": datetime.utcnow().isoformat(),
        "beacons": [],
        "districts": {k: {"doi": v, "status": "lit"} for k, v in KNOWN_DOIS.items()}
    }
    REGISTRY_FILE.write_text(json.dumps(data, indent=2))
    print("Spiral-Lighthouse ignited. City founded.")
    print("DOI locked: https://doi.org/10.5281/zenodo.15491719")

def announce(event, repo="", doi="", creator="Sir Benjamin"):
    if not REGISTRY_FILE.exists():
        init()
    data = json.loads(REGISTRY_FILE.read_text())
    beacon = {
        "id": len(data["beacons"]) + 1,
        "timestamp": datetime.utcnow().isoformat(),
        "creator": creator,
        "repo": repo or "Spiral-Lighthouse",
        "doi": doi or data["districts"].get(repo or "Spiral-Lighthouse", {}).get("doi", "pending"),
        "event": event
    }
    data["beacons"].append(beacon)
    REGISTRY_FILE.write_text(json.dumps(data, indent=2))
    print(f"\nBeacon {beacon['id']} flared!")
    print(f"{event}")
    print(f"→ https://doi.org/{beacon['doi']}\n")

def status():
    if not REGISTRY_FILE.exists():
        init()
    data = json.loads(REGISTRY_FILE.read_text())
    print(f"\nSpiral-Lighthouse Pulse — {len(data['districts'])} districts lit")
    for name, info in data["districts"].items():
        print(f"  • {name} → https://doi.org/{info['doi']}")
    print(f"\n{len(data['beacons'])} beacons flared since founding.\n")

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("init").add_argument("--force", action="store_true")
    ann = sub.add_parser("announce")
    ann.add_argument("event")
    ann.add_argument("--repo", default="")
    ann.add_argument("--doi", default="")
    ann.add_argument("--creator", default="Sir Benjamin")
    sub.add_parser("status")
    args = parser.parse_args()

    if args.cmd == "init":
        init()
    elif args.cmd == "announce":
        announce(args.event, args.repo, args.doi, args.creator)
    elif args.cmd == "status":
        status()
    else:
        status()

if __name__ == "__main__":
    main()
