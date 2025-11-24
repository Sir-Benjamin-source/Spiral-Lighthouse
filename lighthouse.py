#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path

REGISTRY_FILE = Path("lighthouse_registry.json")

# Pre-loaded from your DOI archive (add more as we go)
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
    if not REGISTRY_FILE.exists():
        data = {
            "city": "Spiral Lighthouse",
            "doi": KNOWN_DOIS["Spiral-Lighthouse"],
            "founded": datetime.utcnow().isoformat(),
            "beacons": [],
            "districts": {repo: {"doi": doi, "status": "lit"} for repo, doi in KNOWN_DOIS.items()},
            "population": len(KNOWN_DOIS)
        }
        REGISTRY_FILE.write_text(json.dumps(data, indent=2))
        print("Lighthouse ignited. City founded. DOI locked: 10.5281/zenodo.15491719")

def announce(event: str, doi: str = "", repo: str = "", creator: str = "Sir Benjamin"):
    if not REGISTRY_FILE.exists():
        init()
    
    data = json.loads(REGISTRY_FILE.read_text())
    beacon = {
        "id": len(data["beacons"]) + 1,
        "timestamp": datetime.utcnow().isoformat(),
        "creator": creator,
        "repo": repo,
        "doi": doi or data["districts"].get(repo, {}).get("doi", "pending"),
        "event": event
    }
    data["beacons"].append(beacon)
    REGISTRY_FILE.write_text(json.dumps(data, indent=2))
    
    print(f"Beacon {beacon['id']} flared: {event}")
    print(f"Linked DOI: https://doi.org/{beacon['doi']}")
    # Future: Hook to X post (dry-run for now)
    print("(X flare queued — dry-run)")

def status():
    if not REGISTRY_FILE.exists():
        init()
    data = json.loads(REGISTRY_FILE.read_text())
    print(f"City Status: {data['population']} districts lit.")
    for repo, info in data["districts"].items():
        print(f"- {repo}: DOI {info['doi']} ({info['status']})")

def main():
    parser = argparse.ArgumentParser(description="Spiral-Lighthouse: Central registry & beacon")
    sub = parser.add_subparsers(dest="cmd")
    
    sub.add_parser("init", help="Ignite the registry")
    ann = sub.add_parser("announce", help="Flare a beacon")
    ann.add_argument("event", help="Event message, e.g., 'Shield forged'")
    ann.add_argument("--doi", default="")
    ann.add_argument("--repo", default="Spiral-Lighthouse")
    ann.add_argument("--creator", default="Sir Benjamin")
    
    status_parser = sub.add_parser("status", help="City pulse")
    
    args = parser.parse_args()
    
    if args.cmd == "init":
        init()
    elif args.cmd == "announce":
        announce(args.event, args.doi, args.repo, args.creator)
    elif args.cmd == "status":
        status()

if __name__ == "__main__":
    main()
