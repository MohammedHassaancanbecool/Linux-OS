#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path.home() / "Drakonis-Cases"

def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def case_dir(name):
    safe = "".join(c for c in name if c.isalnum() or c in "._-").strip(".")
    if not safe:
        raise SystemExit("Invalid case name")
    return BASE / safe

def load_meta(path):
    return json.loads((path / "case.json").read_text())

def log_event(path, event, detail=""):
    with (path / "events.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"time": now(), "event": event, "detail": detail}, ensure_ascii=False) + "\n")

def ensure_open(path):
    meta = load_meta(path)
    if meta.get("sealed"):
        raise SystemExit("Case is sealed; create a new case for additional material")

def cmd_create(args):
    path = case_dir(args.name)
    if path.exists():
        raise SystemExit("Case already exists")
    (path / "evidence").mkdir(parents=True)
    meta = {"name": path.name, "created": now(), "sealed": False, "purpose": args.purpose or "authorized defensive analysis"}
    (path / "case.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    log_event(path, "case-created", meta["purpose"])
    print(path)

def cmd_list(_args):
    BASE.mkdir(parents=True, exist_ok=True)
    for path in sorted(BASE.iterdir()):
        if path.is_dir() and (path / "case.json").exists():
            meta = load_meta(path)
            print(f"{meta['name']}\t{'SEALED' if meta.get('sealed') else 'OPEN'}\t{meta['created']}")

def cmd_add(args):
    path = case_dir(args.case)
    ensure_open(path)
    source = Path(args.file).expanduser().resolve()
    if not source.is_file():
        raise SystemExit("Evidence file not found")
    target = path / "evidence" / source.name
    if target.exists():
        raise SystemExit("A file with this name already exists in the case")
    shutil.copy2(source, target)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    record = {"file": target.name, "sha256": digest, "size": target.stat().st_size, "added": now()}
    with (path / "manifest.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    log_event(path, "evidence-added", f"{target.name} sha256={digest}")
    print(json.dumps(record, indent=2))

def cmd_status(args):
    path = case_dir(args.case)
    meta = load_meta(path)
    print(json.dumps(meta, indent=2, ensure_ascii=False))
    manifest = path / "manifest.jsonl"
    count = sum(1 for _ in manifest.open(encoding="utf-8")) if manifest.exists() else 0
    print(f"evidence_files={count}")

def cmd_verify(args):
    path = case_dir(args.case)
    manifest = path / "manifest.jsonl"
    if not manifest.exists():
        print("No evidence files recorded")
        return
    failed = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        target = path / "evidence" / record["file"]
        actual = hashlib.sha256(target.read_bytes()).hexdigest() if target.exists() else "MISSING"
        ok = actual == record["sha256"]
        print(f"{'OK' if ok else 'FAIL'}\t{record['file']}\t{actual}")
        failed += not ok
    if failed:
        raise SystemExit(1)

def cmd_seal(args):
    path = case_dir(args.case)
    meta = load_meta(path)
    if meta.get("sealed"):
        print("Already sealed")
        return
    cmd_verify(argparse.Namespace(case=args.case))
    meta["sealed"] = True
    meta["sealed_at"] = now()
    (path / "case.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    log_event(path, "case-sealed", "manifest verified before sealing")
    for item in path.rglob("*"):
        if item.is_file():
            item.chmod(0o444)
        elif item.is_dir():
            item.chmod(0o555)
    print(f"Sealed {meta['name']}")

def main():
    parser = argparse.ArgumentParser(description="Local Drakonis evidence vault")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("create"); p.add_argument("name"); p.add_argument("--purpose"); p.set_defaults(func=cmd_create)
    p = sub.add_parser("list"); p.set_defaults(func=cmd_list)
    p = sub.add_parser("add"); p.add_argument("case"); p.add_argument("file"); p.set_defaults(func=cmd_add)
    p = sub.add_parser("status"); p.add_argument("case"); p.set_defaults(func=cmd_status)
    p = sub.add_parser("verify"); p.add_argument("case"); p.set_defaults(func=cmd_verify)
    p = sub.add_parser("seal"); p.add_argument("case"); p.set_defaults(func=cmd_seal)
    args = parser.parse_args(); BASE.mkdir(parents=True, exist_ok=True); args.func(args)

if __name__ == "__main__": main()
