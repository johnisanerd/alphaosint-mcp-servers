# Baidu Search MCP server

Registry name: `io.github.johnisanerd/baidu-search`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Run Baidu web searches with device, location and time filters and get organic results and related search features as structured rows, paginated.

## When to use it

Baidu is the main search engine in mainland China and ranks very differently from Google. Use it for China SEO, market research and monitoring Chinese-language coverage.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/Baidu-Search-Scraper`, which gives your agent a single tool, `johnvc--Baidu-Search-Scraper`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/Baidu-Search-Scraper` on your own Apify account and is billed there at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Search Start | $0.012 | One-time setup fee per Actor run |
| Page Processed | $0.02 | Fee per page of search results processed. This returns a single page of search results. |

Free-plan rates as of 2026-11-12; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00001). Current prices are on the Actor's page: https://apify.com/johnvc/Baidu-Search-Scraper

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/Baidu-Search-Scraper`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http baidu-search "https://mcp.apify.com/?tools=johnvc/Baidu-Search-Scraper"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "baidu-search": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/Baidu-Search-Scraper"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "baidu-search": {
      "url": "https://mcp.apify.com/?tools=johnvc/Baidu-Search-Scraper"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "baidu-search": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/Baidu-Search-Scraper"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--Baidu-Search-Scraper` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--Baidu-Search-Scraper`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | yes | `"python tutorial"` | The search term to search for on Baidu. |
| `device` | string: desktop, mobile, tablet |  | `"desktop"` | The device type to simulate for the search. |
| `localization` | integer |  | `1` | Language filter for results. 1 = All languages (default), 2 = Simplified Chinese only, 3 = Traditional Chinese only. |
| `page` | integer |  | `1` | The starting page number for search results (default: 1). |
| `num_results` | integer |  | `10` | Number of results to retrieve per page (max 50, default: 10). |
| `time_period` | string |  |  | Filter results by date range using Unix timestamps. Format: 'stf=START_UNIX,END_UNIX\|stftype=1'. Example for last 7 days: 'stf=1748994000,1749600000\|stftype=1'. Leave blank to get results from all dates. |
| `max_pagination` | integer |  | `3` | Maximum number of pages to fetch (0 = no limit, default: 3 to avoid too many requests). |
| `output_file` | string |  |  | Optional filename to save results. If not provided, will auto-generate based on query and parameters. |

### Example

Ask the agent in plain language, or call `johnvc--Baidu-Search-Scraper` with arguments such as:

```json
{
  "query": "python tutorial"
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `query` | string | The search term submitted to Baidu. |
| `device` | string | Device used for the search: desktop, mobile, or tablet. |
| `localization` | integer | Language filter. 1=All, 2=Simplified Chinese, 3=Traditional Chinese. |
| `page` | integer | First page of results fetched. |
| `num_results` | integer | Number of results requested per page. |
| `max_pagination` | integer | Maximum pages fetched (0 = unlimited). |
| `pages_processed` | integer | Number of result pages actually fetched. |
| `total_results_found` | integer | Total number of organic results returned across all pages. |
| `search_timestamp` | string | ISO 8601 timestamp of when the search was executed. |
| `search_metadata` | object | Run configuration and pagination summary. |
| `pagination_info` | object | Details about pages fetched: total pages, current page, limit reached. |
| `organic_results` | array | List of organic search results with title, URL, snippet, position, and rich data. |
| `answer_box` | array | Direct answer results shown above organic listings. |
| `related_videos` | array | Video results shown on the search page. |
| `people_also_search_for` | array | Related query suggestions shown by Baidu. |
| `related_searches` | array | Related search queries listed at the bottom of the page. |
| `top_searches` | array | Trending search terms surfaced by Baidu. |
| `time_period` | string | Unix timestamp range filter used for the search, if any. |

## Data source and terms

Baidu public search results, collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/Baidu-Search-Scraper
- Docs page: https://alphaosint.com/mcp/baidu-search/
- All AlphaOSINT MCP servers: [index](../../README.md)
