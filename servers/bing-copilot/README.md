# Bing Copilot MCP server

Registry name: `io.github.johnisanerd/bing-copilot`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Get the Copilot AI answer Bing shows for a query, with the answer text in structured blocks, the sources it cites and the brands it mentions.

## When to use it

The Microsoft side of AI answer tracking, alongside Google AI Overview. Use it for answer-engine optimization, brand monitoring and checking which sources Copilot cites.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/bing-copilot-api`, which gives your agent a single tool, `johnvc--bing-copilot-api`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/bing-copilot-api` on your own Apify account and is billed there at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Copilot query resolved | $0.015 | One AI answer resolution: the answer, its structured text blocks, and its cited references when present. |

Free-plan rates as of 2026-11-13; paid Apify plans pay less per event. Current prices are on the Actor's page: https://apify.com/johnvc/bing-copilot-api

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/bing-copilot-api`
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

## Tools

| Tool | What it does |
|---|---|
| `johnvc--bing-copilot-api` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--bing-copilot-api`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string |  | `"best crm for startups"` | REQUIRED (or use `queries`). A question or search phrase to resolve, e.g. 'best crm for startups'. Anything you would type into the answer engine works. |
| `queries` | array |  |  | Provide a list of queries to resolve in one run, e.g. ['best crm for startups', 'best help desk software']. Each query returns one AI answer row. |
| `brandToTrack` | string |  |  | Optional brand or product name, e.g. 'Salesforce'. Each answer row then includes a `brandMentioned` boolean showing whether the brand appears in the AI answer text or its cited sources. |

### Example

Ask the agent in plain language, or call `johnvc--bing-copilot-api` with arguments such as:

```json
{
  "query": "best crm for startups"
}
```

### Output

JSON rows with these fields:

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
| `note` | string | Extra context when no answer was returned for the query. |
| `fetched_at` | string | ISO-8601 timestamp of when this row was fetched. |
| `error_message` | string | Human-readable error description on error rows. |
| `error_type` | string | Machine-readable error class on error rows, e.g. MissingRequiredParameter or CopilotError. |

## Data source and terms

Microsoft's public Copilot answers in Bing search, collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/bing-copilot-api
- Docs page: https://alphaosint.com/mcp/bing-copilot/
- All AlphaOSINT MCP servers: [index](../../README.md)
