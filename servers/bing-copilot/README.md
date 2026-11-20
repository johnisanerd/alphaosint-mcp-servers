# Bing Copilot MCP server

Registry name: `io.github.johnisanerd/bing-copilot`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Get the Copilot AI answer Bing shows for a query, with the answer text in structured blocks, the sources it cites and the brands it mentions.

## When to use it

The Microsoft side of AI answer tracking, alongside Google AI Overview. Use it for answer-engine optimization, brand monitoring and checking which sources Copilot cites.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/bing-copilot-api`. The Actor is a multi-tenant Server Actor, so the endpoint gives your agent one tool, `johnvc--bing-copilot-api`, that sends a single HTTP request to the Actor's server interface and returns the JSON response, usually within seconds. Each request handles one item and starts no run in your account. The agent can't start other Actors through this URL.

To also run the Actor in batch, with many items per run and the full input listed below, use `https://mcp.apify.com/?tools=call-actor,johnvc/bing-copilot-api`. It adds Apify's `call-actor` tool, which can start any Actor your Apify account allows. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each request through `johnvc--bing-copilot-api` is charged to your Apify account at the Actor's prices and starts no run. A batch run through `call-actor` runs the Actor `johnvc/bing-copilot-api` on your account at the same prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Copilot query resolved | $0.015 | One AI answer resolution: the answer, its structured text blocks, and its cited references when present. |

Free-plan rates as of 2026-11-19; paid Apify plans pay less per event. Current prices are on the Actor's page: https://apify.com/johnvc/bing-copilot-api

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/bing-copilot-api` (the server tool only)
- URL with batch runs: `https://mcp.apify.com/?tools=call-actor,johnvc/bing-copilot-api`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http bing-copilot "https://mcp.apify.com/?tools=johnvc/bing-copilot-api"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "bing-copilot": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/bing-copilot-api"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "bing-copilot": {
      "url": "https://mcp.apify.com/?tools=johnvc/bing-copilot-api"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "bing-copilot": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/bing-copilot-api"
      ]
    }
  }
}
```

For batch runs, put the URL with batch runs in the same places.

## Tools

| Tool | What it does |
|---|---|
| `johnvc--bing-copilot-api` | Sends one HTTP request to the Actor's server interface (operations below) and returns the JSON response. Charged per event; starts no run. |

With the URL with batch runs, Apify also adds:

| Tool | What it does |
|---|---|
| `call-actor` | Runs the Actor (or another Actor) with an input such as the batch input below. |
| `get-actor-run` | Status of a run started by `call-actor`. |
| `get-dataset-items` | Reads a run's result rows. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

### Parameters of `johnvc--bing-copilot-api`

The tool takes `method`, `path`, and optionally `query` (query parameters by name) and `body` (a JSON body, POST only). The Actor documents these operations:

| Method | Path | What it does |
|---|---|---|
| `GET` | `/answer` | Bing Copilot AI answer for one query |
| `POST` | `/answer` | Bing Copilot AI answer for one query, JSON body |

Query parameters of `GET /answer`:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | The question or search phrase to resolve. One query per request. |
| `brandToTrack` | string |  | Optional brand or product name. The row then carries a brandMentioned boolean. |
| `max_cache_age_hours` | integer |  | Oldest saved answer, in hours, to serve instead of a live check. 48 is the minimum (lower values are treated as 48); raise it up to 168 to accept older saved answers. |


### Batch input (for `call-actor`)

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string |  | `"best crm for startups"` | REQUIRED (or use `queries`). A question or search phrase to resolve, e.g. 'best crm for startups'. Anything you would type into the answer engine works. |
| `queries` | array |  |  | Provide a list of queries to resolve in one run, e.g. ['best crm for startups', 'best help desk software']. Each query returns one AI answer row. |
| `brandToTrack` | string |  |  | Optional brand or product name, e.g. 'Salesforce'. Each answer row then includes a `brandMentioned` boolean showing whether the brand appears in the AI answer text or its cited sources. |
| `max_cache_age_hours` | integer |  | `48` | Optional. A query answered within this many hours may be served from a saved copy instead of a fresh lookup, charged the same. Values below 48 are treated as 48; the maximum is 168. Default 48. |

### Example

Ask the agent in plain language, or call `johnvc--bing-copilot-api` with arguments such as:

```json
{
  "method": "GET",
  "path": "/answer",
  "query": {
    "query": "best crm for startups"
  }
}
```

A batch run through `call-actor` takes the Actor and its input:

```json
{
  "actor": "johnvc/bing-copilot-api",
  "input": {
    "query": "best crm for startups"
  }
}
```

### Output

The server tool's JSON response carries result rows with these fields (batch runs write the same rows):

| Field | Type | Description |
|---|---|---|
| `result_type` | string: copilot_answer, error | Discriminator for the row kind. Use it to filter the dataset. |
| `query` | string | The query this AI answer was resolved for. |
| `answerPresent` | boolean | True when the engine returned an AI answer for this query. |
| `answerHeader` | string | The one-paragraph headline answer, when the engine provides one. |
| `markdown` | string | The full AI answer rendered as one markdown document: headings, paragraphs, nested lists, tables, and code blocks. |
| `textBlocks` | array | The structured answer blocks exactly as returned: paragraph, heading, list (possibly nested), code_block, and table entries. |
| `references` | array | The sources the AI answer cites: index, title, link, snippet, and source name. |
| `headerVideo` | object | The featured video shown above the answer, when present: title, link, duration, channel, views. |
| `imagesLink` | string | Link to the image results for the query, when the engine returns one. |
| `videosLink` | string | Link to the video results for the query, when the engine returns one. |
| `brandToTrack` | string | The brand checked for mentions, echoed from the input when provided. |
| `brandMentioned` | boolean | True when the tracked brand appears in the AI answer text or its cited sources. Only present when brandToTrack is set. |
| `summary` | string | One-line human-readable summary of the answer, built for AI agents. |
| `note` | string | Extra context: why no answer was returned, or that a stale copy was returned uncharged. |
| `fetched_at` | string | ISO-8601 timestamp of when this row was fetched. |
| `cached` | boolean | True when this answer was served from a saved copy fetched within max_cache_age_hours instead of a fresh lookup. Present only when caching is active. |
| `cache_age_hours` | number | How old the saved copy was, in hours, when it was served. |
| `answer_fetched_at` | string | ISO-8601 timestamp of when this answer was originally retrieved. Equals the fetch time for a fresh lookup. |
| `stale` | boolean | True on an error row that carries the last good copy (up to 7 days old) because the live check did not complete. Stale copies are never charged. |
| `error_message` | string | Human-readable error description on error rows. |
| `error_type` | string | Machine-readable error class on error rows, e.g. MissingRequiredParameter or CopilotError. |

## Data source and terms

Microsoft's public Copilot answers in Bing search, collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/bing-copilot-api
- Docs page: https://alphaosint.com/mcp/bing-copilot/
- All AlphaOSINT MCP servers: [index](../../README.md)
