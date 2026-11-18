#!/usr/bin/env python3
"""Write servers/<name>/README.md for every AlphaOSINT server in the official MCP Registry.

Source of truth: _data/mcp_servers.yml in johnisanerd/website-alphaosint (pass its path), plus each
Actor's public build definition from the Apify API (input schema, dataset schema, live prices).
Each README covers what the server does, when to use it, pricing, the endpoint, client setup,
tools, parameters, an example call and output fields.

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

def server_actor(actor, build):
    """Operations of a multi-tenant Server Actor, or None for a plain Actor.

    For a multi-tenant Server Actor, Apify's hosted MCP endpoint turns the Actor's own tool into an
    HTTP tool (method, path, query, body) built from the Actor's web server schema, and a batch run
    needs the generic call-actor tool. Pages for these Actors describe both.
    """
    sb = actor.get("actorStandby") or {}
    ws = (build.get("actorDefinition") or {}).get("webServerSchema")
    if not (sb.get("isEnabled") and sb.get("tenancy") == "MULTI_TENANT" and isinstance(ws, dict)):
        return None
    ops = []
    for path, methods in (ws.get("paths") or {}).items():
        for method, op in (methods or {}).items():
            if method.lower() not in ("get", "post", "put", "patch", "delete") or not isinstance(op, dict):
                continue
            params = []
            for p in op.get("parameters") or []:
                if p.get("in") != "query":
                    continue
                s = p.get("schema") or {}
                ex = p.get("example", s.get("example"))
                if ex is None and p.get("required"):
                    ex = s.get("default")
                params.append((p["name"], s.get("type", ""), bool(p.get("required")), p.get("description") or "", ex))
            ops.append({"method": method.upper(), "path": path, "summary": op.get("summary") or "",
                        "params": params, "body": bool(op.get("requestBody"))})
    return ops or None


def server_tool_example(ops):
    op = next((o for o in ops if o["method"] == "GET"), ops[0])
    call = {"method": op["method"], "path": op["path"]}
    # Required parameters with an example; with none required, only the first documented one
    # (optional parameters can be mutually exclusive, such as a URL or a name).
    query = {n: ex for n, _t, r, _d, ex in op["params"] if r and ex is not None}
    if not query:
        first = next(((n, ex) for n, _t, _r, _d, ex in op["params"] if ex is not None), None)
        query = dict([first]) if first else {}
    if query:
        call["query"] = query
    return call


def server_operations_md(ops, cell_fn):
    out = ["| Method | Path | What it does |", "|---|---|---|"]
    for o in ops:
        what = o["summary"]
        if o["body"] and not o["params"] and "json" not in what.lower():
            what += " (JSON body with the same fields)"
        out.append("| `%s` | `%s` | %s |" % (o["method"], o["path"], cell_fn(what)))
    out.append("")
    for o in ops:
        if not o["params"]:
            continue
        out.append("Query parameters of `%s %s`:\n" % (o["method"], o["path"]))
        out.append("| Parameter | Type | Required | Description |\n|---|---|---|---|")
        for n, t, r, d, _ex in o["params"]:
            out.append("| `%s` | %s | %s | %s |" % (n, t, "yes" if r else "", cell_fn(d)))
        out.append("")
    return "\n".join(out)

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
    ops = server_actor(actor, build)
    batch_url = "https://mcp.apify.com/?tools=call-actor,%s" % slug
    o = []
    o.append("# %s MCP server\n" % e["title"])
    o.append("Registry name: `io.github.johnisanerd/%s`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).\n" % name)
    o.append("## What it does\n\n%s\n" % e["purpose"])
    o.append("## When to use it\n\n%s\n" % e["distinct"])
    if ops:
        o.append("## How it works\n\n"
                 "The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL "
                 "pins one Actor with `?tools=%s`. The Actor is a multi-tenant Server Actor, so the endpoint gives "
                 "your agent one tool, `%s`, that sends a single HTTP request to the Actor's server interface and "
                 "returns the JSON response, usually within seconds. Each request handles one item and starts no "
                 "run in your account. The agent can't start other Actors through this URL.\n\n"
                 "To also run the Actor in batch, with many items per run and the full input listed below, use "
                 "`%s`. It adds Apify's `call-actor` tool, which can start any Actor your Apify account allows. "
                 "For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` "
                 "parameter.\n" % (slug, tool, batch_url))
        o.append("## Pricing\n\n"
                 "Each request through `%s` is charged to your Apify account at the Actor's prices and starts no "
                 "run. A batch run through `call-actor` runs the Actor `%s` on your account at the same prices:\n" % (tool, slug))
    else:
        o.append("## How it works\n\n"
                 "The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL "
                 "pins one Actor with `?tools=%s`, which gives your agent a single tool, `%s`, whose parameters are "
                 "the Actor's typed input schema. The agent can call that tool directly without searching for an "
                 "Actor first, and it can't start other Actors through this server. For general access to the "
                 "whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.\n" % (slug, tool))
        o.append("## Pricing\n\n"
                 "Each tool call runs the Apify Actor `%s` on your own Apify account and is billed there at the "
                 "Actor's prices:\n" % slug)
    if main:
        o.append("| Charge | Price (USD) | What it covers |\n|---|---|---|")
        for t, p, d in main:
            o.append("| %s | %s | %s |" % (cell(t), usd(p), cell(d)))
        o.append("")
        o.append("Free-plan rates as of %s; paid Apify plans pay less per event.%s Current prices are on the Actor's page: https://apify.com/%s\n"
                 % (time.strftime("%Y-%m-%d"), ((" Batch runs also bill a token amount per run start and stored row (%s)." if ops else " Apify also bills a token amount per run start and stored row (%s).") % ", ".join(usd(p) for _, p, _ in minor)) if minor else "", slug))
    if ops:
        o.append("## Endpoint\n\n- Transport: Streamable HTTP\n- URL: `%s` (the server tool only)\n- URL with batch runs: `%s`\n- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)\n" % (url, batch_url))
    else:
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
    if ops:
        o.append("For batch runs, put the URL with batch runs in the same places.\n")
        o.append("## Tools\n\n| Tool | What it does |\n|---|---|\n"
                 "| `%s` | Sends one HTTP request to the Actor's server interface (operations below) and returns the JSON response. Charged per event; starts no run. |\n\n"
                 "With the URL with batch runs, Apify also adds:\n\n| Tool | What it does |\n|---|---|\n"
                 "| `call-actor` | Runs the Actor (or another Actor) with an input such as the batch input below. |\n"
                 "| `get-actor-run` | Status of a run started by `call-actor`. |\n"
                 "| `get-dataset-items` | Reads a run's result rows. |\n"
                 "| `get-key-value-store-record` | Reads a record a run stored. |\n"
                 "| `abort-actor-run` | Stops a run. |\n" % tool)
        o.append("### Parameters of `%s`\n\n"
                 "The tool takes `method`, `path`, and optionally `query` (query parameters by name) and `body` (a JSON body, POST only). The Actor documents these operations:\n\n%s\n" % (tool, server_operations_md(ops, cell)))
        o.append("### Batch input (for `call-actor`)\n")
        if props:
            o.append("| Parameter | Type | Required | Default | Description |\n|---|---|---|---|---|")
            for k, s in props.items():
                o.append("| `%s` | %s | %s | %s | %s |" % (k, cell(type_of(s), 80), "yes" if k in req else "", default_of(s), cell(s.get("description") or s.get("title"))))
            o.append("")
        ex = EXAMPLES.get(name) or example(actor, props, req)
        o.append("### Example\n\nAsk the agent in plain language, or call `%s` with arguments such as:\n\n```json\n%s\n```\n" % (tool, json.dumps(server_tool_example(ops), indent=2, ensure_ascii=False)))
        if ex:
            o.append("A batch run through `call-actor` takes the Actor and its input:\n\n```json\n%s\n```\n" % json.dumps({"actor": slug, "input": ex}, indent=2, ensure_ascii=False))
    else:
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
        lead = "The server tool's JSON response carries result rows with these fields (batch runs write the same rows):" if ops else "JSON rows with these fields:"
        o.append("### Output\n\n%s\n\n| Field | Type | Description |\n|---|---|---|" % lead)
        for f, t, d in rows[:60]:
            o.append("| `%s` | %s | %s |" % (f, cell(t, 60), cell(d)))
        if len(rows) > 60:
            o.append("\n%d more fields are in the Actor's dataset schema." % (len(rows) - 60))
        o.append("")
    o.append("## Data source and terms\n\n%s The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.\n" % e["data_source"])
    o.append("## Links\n\n- Actor on Apify: https://apify.com/%s\n- Docs page: https://alphaosint.com/mcp/%s/\n- All AlphaOSINT MCP servers: [index](../../README.md)\n" % (slug, name))
    text = "\n".join(o)
    assert not re.search(r"fp(r|_sid)=", text), name
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
