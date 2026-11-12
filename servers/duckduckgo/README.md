# DuckDuckGo Search MCP server

Registry name: `io.github.johnisanerd/duckduckgo`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Run DuckDuckGo searches with region, safe-search and date filters and get organic results, ads, knowledge graph, news, images, videos and related searches.

## How it differs

A low-cost general web search tool for agents that need search results without a Google dependency, plus DuckDuckGo rank tracking.

**From the other AlphaOSINT servers:** each server wraps exactly one Apify Actor and does one job; the [index](../../README.md) lists them side by side.

**From Apify's shared endpoint:** `https://mcp.apify.com` on its own exposes general tools (`search-actors`, `call-actor`) that let an agent look for and run any of thousands of Actors. This server's URL pins one Actor with `?tools=johnvc/DuckDuckGo-Scraper-for-serp-rankings`, so the agent gets a single tool, `johnvc--DuckDuckGo-Scraper-for-serp-rankings`, whose parameters are this Actor's typed input schema. There is no search or Actor-selection step, and the agent cannot start other Actors through it.

## Hosted on Apify, billed to your Apify account

This server is not self-hosted. It runs on Apify's hosted MCP endpoint (`mcp.apify.com`), which starts the Apify Actor `johnvc/DuckDuckGo-Scraper-for-serp-rankings` for each tool call. You need an Apify account, and **every call is billed to that account** at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Setup | $0.00006 | One-time setup fee per Actor run |
| Search result | $0.0004 | One DuckDuckGo search result delivered (organic, ad, news, knowledge-graph, image or video item). Only delivered results are billed; cached results bill the same. |

Free-plan rates as of 2026-11-12; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00001). Current prices are on the Actor's page: https://apify.com/johnvc/DuckDuckGo-Scraper-for-serp-rankings

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/DuckDuckGo-Scraper-for-serp-rankings`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http duckduckgo "https://mcp.apify.com/?tools=johnvc/DuckDuckGo-Scraper-for-serp-rankings"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "duckduckgo": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/DuckDuckGo-Scraper-for-serp-rankings"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "duckduckgo": {
      "url": "https://mcp.apify.com/?tools=johnvc/DuckDuckGo-Scraper-for-serp-rankings"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "duckduckgo": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/DuckDuckGo-Scraper-for-serp-rankings"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--DuckDuckGo-Scraper-for-serp-rankings` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--DuckDuckGo-Scraper-for-serp-rankings`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | yes | `"The Siliconimist Podcast"` | Search DuckDuckGo for this term (up to 500 characters). Identical searches are served from a 7-day cache. |
| `localization` | string: us-en, uk-en, ca-en, au-en, de-de, fr-fr … |  | `"us-en"` | Set the region and language for search results (e.g. `us-en`, `uk-en`, `fr-fr`, `de-de`, `jp-jp`). Defaults to `us-en` (United States English). |
| `safe` | string: strict, moderate, off |  | `"moderate"` | Set the safe-search filter level. Use `strict` to block adult content, `moderate` for default filtering, or `off` for no filtering. |
| `date_filter` | string |  |  | Filter results by date. Use `d` for the past day, `w` for the past week, `m` for the past month, `y` for the past year, or a custom range like `2026-01-01..2026-05-01`. |
| `max_pages` | integer |  | `1` | Set the maximum number of result pages to fetch. The first page holds 10 results and each later page 15. Use `0` for as many pages as exist (up to 200 pages, about 3,000 results). You pay only for results actually deliv… |
| `output_file` | string |  |  | Save results to this filename in the run's key-value store in addition to the dataset. Leave empty to skip the file output. |

### Example

Ask the agent in plain language, or call `johnvc--DuckDuckGo-Scraper-for-serp-rankings` with arguments such as:

```json
{
  "query": "The Siliconimist Podcast"
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `query` | string | Search Query |
| `localization` | string | Localization/Region |
| `safe_search` | integer | 1=Strict, -1=Moderate, -2=Off |
| `date_filter` | string | Date Filter |
| `max_pages` | integer | Maximum Pages |
| `search_timestamp` | string | Search Timestamp |
| `total_results_found` | integer | Total Results Found |
| `pages_processed` | integer | Pages Processed |
| `page_number` | integer | Current Page Number |
| `search_metadata` | object | Search Metadata |
| `pagination_info` | object | Pagination Information |
| `organic_results` | array | Organic Search Results |
| `ads` | array | Advertisement Results |
| `knowledge_graph` | array | Knowledge Graph Results |
| `news_results` | array | News Results |
| `inline_images` | array | Inline Image Results |
| `inline_videos` | array | Inline Video Results |
| `related_searches` | array | Related Searches |
| `results_count` | integer | Results Delivered on This Page (billed per result) |
| `cached` | boolean | Served From the 7-Day Cache |
| `fetchedAt` | string | When the Page Was Fetched (UTC) |
| `cacheAgeDays` | number | Cache Age in Days |

## Data source and terms

DuckDuckGo public search results, collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/DuckDuckGo-Scraper-for-serp-rankings
- Docs page: https://alphaosint.com/mcp/duckduckgo/
- All AlphaOSINT MCP servers: [index](../../README.md)
