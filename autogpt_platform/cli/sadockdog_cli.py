#!/usr/bin/env python3
"""
SADOCKDOG CLI

Lightweight CLI to select one of your agents and execute it with a prompt.

Auth:
  - Create an API key in the web UI (Profile → API Keys) with EXECUTE_GRAPH.
  - Export it as AUTOGPT_API_KEY.

Config:
  - AGPT_BASE_URL (default http://localhost:8006)

Usage:
  $ setx AUTOGPT_API_KEY "<your_api_key>"   # PowerShell: $Env:AUTOGPT_API_KEY = "..."
  $ python autogpt_platform/cli/sadockdog_cli.py
"""

import json
import os
import sys
import urllib.request
import urllib.error


BASE = os.environ.get("AGPT_BASE_URL", "http://localhost:8006").rstrip("/")
API_KEY = os.environ.get("AUTOGPT_API_KEY")

if not API_KEY:
    print("ERROR: AUTOGPT_API_KEY is not set. Create one in the web UI (Profile → API Keys).", file=sys.stderr)
    sys.exit(1)


def _req(path: str, method: str = "GET", data: dict | None = None):
    url = f"{BASE}{path}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        try:
            err = e.read().decode("utf-8")
        except Exception:
            err = str(e)
        print(f"HTTP {e.code} for {method} {url}: {err}", file=sys.stderr)
        sys.exit(2)
    except urllib.error.URLError as e:
        print(f"Connection error for {method} {url}: {e}", file=sys.stderr)
        sys.exit(3)


def list_my_agents():
    status, data = _req("/api/store/myagents")
    if status != 200:
        print(f"Unexpected status: {status}", file=sys.stderr)
        sys.exit(4)
    return data.get("agents", [])


def execute_agent(graph_id: str, graph_version: int | None, prompt: str):
    payload = {
        "inputs": {"prompt": prompt},
        "credentials_inputs": {},
    }
    path = f"/api/graphs/{graph_id}/execute/{graph_version if graph_version is not None else 'null'}"
    status, data = _req(path, method="POST", data=payload)
    if status != 200:
        print(f"Unexpected execute status: {status}", file=sys.stderr)
        sys.exit(5)
    return data


def main():
    print("SADOCKDOG CLI — select an agent and send a prompt\n")
    agents = list_my_agents()
    if not agents:
        print("No agents found. Create one in the web UI first.")
        return

    for i, a in enumerate(agents, start=1):
        name = a.get("agent_name")
        aid = a.get("agent_id")
        ver = a.get("agent_version")
        print(f"{i}. {name}  (id={aid}, v={ver})")

    while True:
        sel = input("\nChoose an agent (number): ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(agents):
            idx = int(sel) - 1
            chosen = agents[idx]
            break
        print("Invalid choice. Try again.")

    prompt = input("Enter your instruction/prompt: ").strip()
    if not prompt:
        print("Empty prompt. Aborting.")
        return

    graph_id = chosen.get("agent_id")
    graph_version = chosen.get("agent_version")
    print("\nExecuting agent…")
    res = execute_agent(graph_id, graph_version, prompt)
    exec_id = res.get("id")
    print("\nExecution started!")
    print(f"Execution ID: {exec_id}")
    print(
        "View in web UI: http://localhost:3000/platform/library/agents/"
        f"{graph_id}?flowExecutionID={exec_id}"
    )


if __name__ == "__main__":
    main()
