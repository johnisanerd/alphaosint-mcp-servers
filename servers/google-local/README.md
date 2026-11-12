# Google Local MCP server

Registry name: `io.github.johnisanerd/google-local`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Search local businesses for a query and place and get name, rating, review count, phone, hours, address, place ID and coordinates.

## When to use it

Returns the ranked local results Google shows for a search, with country, language and device targeting. Use it for local SEO rank checks and building business lists for an area.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/google-local-api`, which gives your agent a single tool, `johnvc--google-local-api`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/google-local-api` on your own Apify account and is billed there at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Setup | $0.002 | One-time setup fee per Actor run. Covers instance provisioning, memory allocation, and search session initialization. |
| Pages Processed | $0.02 | Fee per page of Google Local search results processed. Returns the local pack businesses with rating, reviews, address, phone, hours, GPS, place_id, and links for that page. |

Free-plan rates as of 2026-11-12; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00001, $0.00005). Current prices are on the Actor's page: https://apify.com/johnvc/google-local-api

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/google-local-api`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http google-local "https://mcp.apify.com/?tools=johnvc/google-local-api"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "google-local": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/google-local-api"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "google-local": {
      "url": "https://mcp.apify.com/?tools=johnvc/google-local-api"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-local": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/google-local-api"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--google-local-api` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--google-local-api`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `q` | string | yes | `"coffee"` | The Google Local search query. Examples: 'coffee', 'dentists near me', 'plumbers in Brooklyn', 'best pizza'. Combine with the 'location' field for city-level targeting. Any term valid in Google Local search is accepted. |
| `location` | string |  | `"Austin, Texas, United States"` | City-level location (e.g., 'Austin, Texas, United States', 'London', 'Brooklyn, New York'). Optional but recommended. Cannot be combined with 'uule'. If both are omitted, results use the API's default origin. |
| `uule` | string |  |  | Advanced: Google-encoded location string for precise geographic targeting. Use instead of 'location' for fine-grained control. Cannot be combined with 'location'. |
| `google_domain` | string |  | `"google.com"` | Which Google domain to query (e.g., 'google.com', 'google.co.uk', 'google.fr', 'google.de'). Defaults to 'google.com'. Use the regional domain for localized result formatting. |
| `gl` | string |  | `"us"` | Two-letter country code (ISO 3166-1 alpha-2, e.g., 'us', 'uk', 'fr', 'de', 'jp'). Localizes search results to that country. Defaults to 'us'. |
| `hl` | string |  | `"en"` | Two-letter language code (ISO 639-1, e.g., 'en', 'es', 'fr', 'de', 'ja'). Sets the language for the interface and result content. Defaults to 'en'. |
| `ludocid` | string |  |  | Advanced: Google customer identifier (CID) for a specific place. When provided, narrows results around that single business. |
| `tbs` | string |  |  | Advanced: Google search filter string for criteria not exposed elsewhere. See Google's filter documentation for valid syntax. |
| `device` | string: desktop, tablet, mobile |  | `"desktop"` | Which device to emulate. Affects results-per-page count (desktop returns about 20 per page, mobile about 10) and result formatting. Defaults to 'desktop'. |
| `max_pages` | integer |  | `1` | Maximum number of result pages to fetch (1-indexed). Set 0 for unlimited, bounded by a safety cap of 20 pages. Default: 1. Each fetched page is billed separately under pay-per-event. |

### Example

Ask the agent in plain language, or call `johnvc--google-local-api` with arguments such as:

```json
{
  "q": "coffee",
  "location": "Austin, Texas, United States",
  "google_domain": "google.com",
  "gl": "us",
  "hl": "en"
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `search_parameters` | object | The complete set of input parameters used for this search, echoed back in each result page for traceability. |
| `search_metadata` | object | Aggregate statistics about the search run - total results estimate, pages processed, and pagination status. |
| `search_timestamp` | string | ISO 8601 timestamp of when this search page was executed (e.g., '2026-05-12T10:30:00.123456'). |
| `page_number` | integer | 1-indexed page number this dataset item represents. Each page of results is pushed as a separate dataset item. |
| `local_results` | array | Local pack businesses on this page. Each item: title, rating, reviews, address, phone, hours, type, price, place_id, gps_coordinates, links, service_options. |
| `ads_results` | array | Paid local placements (Google Local Ads) on this page. Same business fields as local_results plus ad_title. |
| `local_map` | object | Embedded local map preview returned by Google. Contains the map image URL when present. |
| `discover_more_places` | array | Related local search suggestions Google surfaces under the main results (e.g., 'Best coffee', 'Coffee shops nearby'). |
| `pagination` | object | Pagination state for this page. Contains the current page index. Use the Actor's max_pages input to fetch additional pages rather than walking links. |
| `error` | boolean | True when this dataset item represents an error record rather than search results. |
| `error_message` | string | Human-readable description of the error that occurred, if error is true. |
| `error_type` | string | Machine-readable error category (e.g., 'ValidationError', 'InsufficientFunds', 'SearchError', 'ChargeFailed'). |
| `timestamp` | string | ISO 8601 timestamp of when the error occurred. Only present on error records. |

## Data source and terms

Google Search local results (the local pack), collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/google-local-api
- Docs page: https://alphaosint.com/mcp/google-local/
- All AlphaOSINT MCP servers: [index](../../README.md)
