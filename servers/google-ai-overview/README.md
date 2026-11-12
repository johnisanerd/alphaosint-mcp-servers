# Google AI Overview MCP server

Registry name: `io.github.johnisanerd/google-ai-overview`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Fetch the AI Overview Google shows for one or many queries, with the generated answer text and its cited sources, for a chosen country and language.

## How it differs

Shows what Google's AI answer says and which pages it cites. Use it for AI-search visibility tracking (GEO) and checking how a brand or topic is summarized.

**From the other AlphaOSINT servers:** each server wraps exactly one Apify Actor and does one job; the [index](../../README.md) lists them side by side.

**From Apify's shared endpoint:** `https://mcp.apify.com` on its own exposes general tools (`search-actors`, `call-actor`) that let an agent look for and run any of thousands of Actors. This server's URL pins one Actor with `?tools=johnvc/Google-AI-Overview-API`, so the agent gets a single tool, `johnvc--Google-AI-Overview-API`, whose parameters are this Actor's typed input schema. There is no search or Actor-selection step, and the agent cannot start other Actors through it.

## Hosted on Apify, billed to your Apify account

This server is not self-hosted. It runs on Apify's hosted MCP endpoint (`mcp.apify.com`), which starts the Apify Actor `johnvc/Google-AI-Overview-API` for each tool call. You need an Apify account, and **every call is billed to that account** at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| AI Overview retrieval | $0.0027 | Fee per AI Overview retrieval. One retrieval for a standard inline answer; two when Google defers generation and a follow-up fetch is required to resolve it. |
| Setup | $0.00005 | One-time setup fee per Actor run, charged at startup to cover provisioning. |

Free-plan rates as of 2026-11-12; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00001, $0.00005). Current prices are on the Actor's page: https://apify.com/johnvc/Google-AI-Overview-API

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/Google-AI-Overview-API`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http google-ai-overview "https://mcp.apify.com/?tools=johnvc/Google-AI-Overview-API"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "google-ai-overview": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/Google-AI-Overview-API"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "google-ai-overview": {
      "url": "https://mcp.apify.com/?tools=johnvc/Google-AI-Overview-API"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-ai-overview": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/Google-AI-Overview-API"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--Google-AI-Overview-API` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--Google-AI-Overview-API`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string |  | `"what is the Siliconimist podcast?"` | Enter a single search query to fetch the Google AI Overview for (e.g. 'what is the Siliconimist podcast?'). Provide this, `queries`, or both. AI Overviews appear most often for question-style searches. |
| `queries` | array |  |  | Provide a list of search queries to fetch AI Overviews for in one run. Merged with `query` and de-duplicated. Use this for batch lookups. |
| `target_domains` | array |  | `["siliconimist.com"]` | Domains you consider yours, e.g. example.com. When set, each result row is classified: was any of these domains cited in the AI Overview? Subdomains match their parent (learn.example.com matches example.com). Leave empt… |
| `gl` | string |  | `"us"` | Set the two-letter country code for the search (ISO 3166-1, e.g. 'us', 'gb', 'ca'). Defaults to 'us'. AI Overviews are available in a limited set of countries. |
| `hl` | string |  | `"en"` | Set the two-letter interface language code (ISO 639-1, e.g. 'en'). Defaults to 'en'. AI Overviews are currently shown for English searches only, so leaving this as 'en' is recommended. |
| `location` | string |  |  | Optionally narrow results to a specific location by name (e.g. 'Austin, Texas, United States'). Leave empty to use country-level targeting from the country code. |
| `max_cache_age_hours` | integer |  | `48` | Some queries may be answered from a saved copy up to 48 hours old. Google's AI Overviews change their wording and sources roughly every two days, so a query checked in the last 48 hours is returned from that saved answe… |

### Example

Ask the agent in plain language, or call `johnvc--Google-AI-Overview-API` with arguments such as:

```json
{
  "query": "what is the Siliconimist podcast?",
  "target_domains": [
    "siliconimist.com"
  ],
  "gl": "us",
  "hl": "en"
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `result_type` | string | Either 'ai_overview' (a resolved query row) or 'error' (a validation or fetch error row). |
| `query` | string | The search query this row corresponds to. |
| `ai_overview_present` | boolean | True if Google returned an AI Overview for this query, false if none was shown. |
| `used_dedicated_api` | boolean | True when Google deferred generation and a second upstream call was needed to resolve the overview. |
| `retrievals_used` | integer | Number of upstream retrievals consumed for this query: 1 for an inline answer, 2 when a deferred follow-up fetch was required. |
| `text_blocks` | array | Ordered content blocks of the AI Overview (paragraphs, headings, lists, tables). Empty when no overview was shown. |
| `references` | array | Cited sources for the AI Overview, each with title, link, snippet, source, and index. Empty when no overview was shown. |
| `thumbnail` | string | Thumbnail image URL associated with the AI Overview, when present. |
| `header_images` | array | Header image entries shown with the AI Overview, when present. |
| `gl` | string | Country code used for the search. |
| `hl` | string | Interface language code used for the search. |
| `location` | string | Location string used for the search, if any. |
| `fetched_at` | string | ISO 8601 timestamp of when this row was produced. |
| `note` | string | Human-readable note explaining why no overview was returned, when applicable (e.g. Google declined to generate one). |
| `error_message` | string | Human-readable error description. Only present on rows with result_type='error'. |
| `error_type` | string | Machine-readable error category (e.g. 'MissingRequiredParameter', 'MissingApiKey', 'AIOverviewError'). |
| `check_status` | string | Whether the check itself completed: 'ok' (the result is trustworthy), 'retrieval_failed' (the check did not complete), or 'blocked' (the request was refused). On anything other than 'ok', ai_overview_present is omitted… |
| `citation_state` | string | How your domains fared on this query: 'cited', 'competitor_cited', 'no_overview', or 'overview_no_references'. Present only when target_domains is set and check_status is 'ok'. |
| `cited_urls` | array | The pages of yours the AI Overview cited, as links. Empty when none were cited. |
| `cited_pages_count` | integer | How many distinct pages of yours the AI Overview cited. |
| `cached` | boolean | True when this row's overview came from a copy saved by an earlier check (at most max_cache_age_hours old, default 48) instead of a live check now. Charged like a live check. On a failed check row, true when the last go… |
| `cache_age_hours` | number | Hours between overview_fetched_at and this run, to one decimal. Present only on rows served from cache or carrying a stale copy. |
| `overview_fetched_at` | string | ISO 8601 time the overview was fetched from Google. Equal to the time of this run for a live check; earlier for a cached or stale copy. fetched_at still records when this row was produced. |
| `stale` | boolean | True on a failed check row (check_status retrieval_failed or blocked) that carries the last good copy of the overview, up to 7 days old, because the live check did not complete. Never charged. ai_overview_present and ci… |

## Data source and terms

Google Search AI Overviews, collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/Google-AI-Overview-API
- Docs page: https://alphaosint.com/mcp/google-ai-overview/
- All AlphaOSINT MCP servers: [index](../../README.md)
