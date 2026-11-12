#!/usr/bin/env python3
"""Write servers/<name>/README.md for every AlphaOSINT server in the official MCP Registry.

Source of truth: _data/mcp_servers.yml in johnisanerd/website-alphaosint (pass its path), plus each
Actor's public build definition from the Apify API (input schema, dataset schema, live prices).
Every README is written for GitHub's MCP Registry review: tool names, parameters, a short example,
setup for Claude Code, VS Code, Cursor and Claude Desktop, a plain note that calls run on Apify's
hosted endpoint and bill the user's Apify account, how the server differs from the others and from
Apify's shared endpoint, and no referral parameters anywhere.

    uv run --with pyyaml python scripts/build_readmes.py ../website-alphaosint/_data/mcp_servers.yml
"""
import json, pathlib, re, sys, time, urllib.request
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://api.apify.com/v2"
# Hand-picked examples where the Actor has no prefill to build one from.
EXAMPLES = {"linkedin-people-search": {"jobTitle": "CTO", "company": "Stripe", "maxResults": 10}}
MINOR = {"apify-default-dataset-item", "apify-actor-start"}

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "alphaosint-mcp-readmes"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["data"]

def cell(t, n=220):
    t = " ".join(str(t or "").split()).replace("|", "\\|")
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"

def type_of(s):
    t = s.get("type", "")
    if isinstance(t, list):
        t = " or ".join(x for x in t if x != "null") or "null"
    if s.get("enum"):
        v = [str(x) for x in s["enum"]]
        t += ": " + ", ".join(v[:6]) + (" …" if len(v) > 6 else "")
    return t

def default_of(s):
    for k in ("default", "prefill"):
        if k in s:
            return "`" + cell(json.dumps(s[k], ensure_ascii=False), 60).replace("`", "'") + "`"
    return ""

def example(actor, props, required):
    body = (actor.get("exampleRunInput") or {}).get("body")
    try:
        ex = json.loads(body) if body else None
    except ValueError:
        ex = None
    if isinstance(ex, dict) and ex and "helloWorld" not in ex:
        return ex
    ex = {}
    for k, s in props.items():
        if "prefill" in s:
            ex[k] = s["prefill"]
        elif k in required and "default" in s:
            ex[k] = s["default"]
        elif k in required and s.get("example") is not None:
            ex[k] = s["example"]
    return ex

def outputs(ds):
    f = (ds or {}).get("fields") or {}
    if f.get("type") == "object" and isinstance(f.get("properties"), dict):
        f = f["properties"]
    rows = []
    for n, s in f.items():
        if isinstance(s, dict):
            rows.append((n, type_of(s), s.get("description") or s.get("title") or ""))
    return rows

def prices(actor):
    info = (actor.get("pricingInfos") or [{}])[-1]
    ev = ((info.get("pricingPerEvent") or {}).get("actorChargeEvents")) or {}
    main, minor = [], []
    for k, e in ev.items():
        tiers = e.get("eventTieredPricingUsd") or {}
        p = (tiers.get("FREE") or {}).get("tieredEventPriceUsd", e.get("eventPriceUsd"))
        if p is None:
            continue
        (minor if k in MINOR else main).append((e.get("eventTitle") or k, p, e.get("eventDescription") or ""))
    return main, minor

def usd(x):
    return "$" + ("%.5f" % x).rstrip("0").rstrip(".")

def readme(e, actor, build):
    name, slug = e["name"], e["actor"]
    tool = slug.replace("/", "--")
    url = "https://mcp.apify.com/?tools=%s" % slug
    ad = build.get("actorDefinition") or {}
    inp = ad.get("input") or {}
    req = set(inp.get("required") or [])
    props = {k: v for k, v in (inp.get("properties") or {}).items() if v.get("type") or not v.get("sectionCaption")}
    ds = (ad.get("storages") or {}).get("dataset")
    main, minor = prices(actor)
    o = []
    o.append("# %s MCP server\n" % e["title"])
    o.append("Registry name: `io.github.johnisanerd/%s`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).\n" % name)
    o.append("## What it does\n\n%s\n" % e["purpose"])
    o.append("## How it differs\n\n%s\n\n"
             "**From the other AlphaOSINT servers:** each server wraps exactly one Apify Actor and does one job; "
             "the [index](../../README.md) lists them side by side.\n\n"
             "**From Apify's shared endpoint:** `https://mcp.apify.com` on its own exposes general tools "
             "(`search-actors`, `call-actor`) that let an agent look for and run any of thousands of Actors. "
             "This server's URL pins one Actor with `?tools=%s`, so the agent gets a single tool, `%s`, whose "
             "parameters are this Actor's typed input schema. There is no search or Actor-selection step, and "
             "the agent cannot start other Actors through it.\n" % (e["distinct"], slug, tool))
    o.append("## Hosted on Apify, billed to your Apify account\n\n"
             "This server is not self-hosted. It runs on Apify's hosted MCP endpoint (`mcp.apify.com`), which "
             "starts the Apify Actor `%s` for each tool call. You need an Apify account, and **every call is "
             "billed to that account** at the Actor's prices:\n" % slug)
    if main:
        o.append("| Charge | Price (USD) | What it covers |\n|---|---|---|")
        for t, p, d in main:
            o.append("| %s | %s | %s |" % (cell(t), usd(p), cell(d)))
        o.append("")
        o.append("Free-plan rates as of %s; paid Apify plans pay less per event.%s Current prices are on the Actor's page: https://apify.com/%s\n"
                 % (time.strftime("%Y-%m-%d"), (" Apify also bills a token amount per run start and stored row (%s)." % ", ".join(usd(p) for _, p, _ in minor)) if minor else "", slug))
    o.append("## Endpoint\n\n- Transport: Streamable HTTP\n- URL: `%s`\n- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)\n" % url)
    vscode = {"servers": {name: {"type": "http", "url": url}}}
    cursor = {"mcpServers": {name: {"url": url}}}
    desktop = {"mcpServers": {name: {"command": "npx", "args": ["-y", "mcp-remote", url]}}}
    o.append("## Setup\n\n**Claude Code**\n\n```bash\nclaude mcp add --transport http %s \"%s\"\n```\n\n"
             "**VS Code** (`.vscode/mcp.json`)\n\n```json\n%s\n```\n\n"
             "**Cursor** (`~/.cursor/mcp.json`)\n\n```json\n%s\n```\n\n"
             "**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions "
             "without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:\n\n```json\n%s\n```\n"
             % (name, url, json.dumps(vscode, indent=2), json.dumps(cursor, indent=2), json.dumps(desktop, indent=2)))
    o.append("## Tools\n\n| Tool | What it does |\n|---|---|\n"
             "| `%s` | Runs the Actor with the parameters below and returns the result rows. |\n"
             "| `get-actor-run` | Status of a run the tool started (for long runs). |\n"
             "| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |\n"
             "| `get-key-value-store-record` | Reads a record a run stored. |\n"
             "| `abort-actor-run` | Stops a run. |\n\n"
             "Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.\n" % tool)
    o.append("### Parameters of `%s`\n" % tool)
    if props:
        o.append("| Parameter | Type | Required | Default | Description |\n|---|---|---|---|---|")
        for k, s in props.items():
            o.append("| `%s` | %s | %s | %s | %s |" % (k, cell(type_of(s), 80), "yes" if k in req else "", default_of(s), cell(s.get("description") or s.get("title"))))
        o.append("")
    ex = EXAMPLES.get(name) or example(actor, props, req)
    if ex:
        o.append("### Example\n\nAsk the agent in plain language, or call `%s` with arguments such as:\n\n```json\n%s\n```\n" % (tool, json.dumps(ex, indent=2, ensure_ascii=False)))
    rows = outputs(ds)
    if rows:
        o.append("### Output\n\nJSON rows with these fields:\n\n| Field | Type | Description |\n|---|---|---|")
        for f, t, d in rows[:60]:
            o.append("| `%s` | %s | %s |" % (f, cell(t, 60), cell(d)))
        if len(rows) > 60:
            o.append("\n%d more fields are in the Actor's dataset schema." % (len(rows) - 60))
        o.append("")
    o.append("## Data source and terms\n\n%s The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.\n" % e["data_source"])
    o.append("## Links\n\n- Actor on Apify: https://apify.com/%s\n- Docs page: https://alphaosint.com/mcp/%s/\n- All AlphaOSINT MCP servers: [index](../../README.md)\n" % (slug, name))
    text = "\n".join(o)
    assert "fpr=" not in text and "fp_sid" not in text, name
    return text

def main():
    entries = yaml.safe_load(pathlib.Path(sys.argv[1]).read_text())
    only = set(sys.argv[2:])
    rows = []
    for e in entries:
        if only and e["name"] not in only:
            continue
        actor = get("%s/acts/%s" % (API, e["actor"].replace("/", "~")))
        build = get("%s/actor-builds/%s" % (API, actor["taggedBuilds"]["latest"]["buildId"]))
        d = ROOT / "servers" / e["name"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "README.md").write_text(readme(e, actor, build), encoding="utf-8")
        rows.append(e)
        print("wrote servers/%s/README.md" % e["name"])
        time.sleep(0.3)
    if not only:
        idx = ["| Server | Registry name | What it does |", "|---|---|---|"]
        for e in rows:
            idx.append("| [%s](servers/%s/) | `io.github.johnisanerd/%s` | %s |" % (e["title"], e["name"], e["name"], cell(e["purpose"], 200)))
        readme_path = ROOT / "README.md"
        text = readme_path.read_text(encoding="utf-8")
        start, end = "<!-- servers:start -->", "<!-- servers:end -->"
        text = text[: text.index(start) + len(start)] + "\n" + "\n".join(idx) + "\n" + text[text.index(end):]
        readme_path.write_text(text, encoding="utf-8")

if __name__ == "__main__":
    main()
