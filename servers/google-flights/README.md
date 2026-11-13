# Google Flights MCP server

Registry name: `io.github.johnisanerd/google-flights`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Search one-way, round-trip and multi-city itineraries and get prices, airlines, stops, layovers, durations and optional booking options as JSON.

## When to use it

Fares and itineraries for any route and date, with filters for stops, airlines, cabin and passengers. Use it for trip-planning agents, fare monitoring and route analysis.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search`, which gives your agent a single tool, `johnvc--Google-Flights-Data-Scraper-Flight-and-Price-Search`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search` on your own Apify account and is billed there at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Page Processed | $0.02 | Fee per page of flight results processed. Returns best flights, other flights, price insights, airports, and booking options for that page. |
| Setup | $0.001 | One-time setup fee per Actor run |
| Booking Options Processed | $0.02 | Fee per booking option returned when fetch_booking_options is enabled. Default is off. |

Free-plan rates as of 2026-11-13; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00001, $0.00001). Current prices are on the Actor's page: https://apify.com/johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http google-flights "https://mcp.apify.com/?tools=johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "google-flights": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "google-flights": {
      "url": "https://mcp.apify.com/?tools=johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-flights": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--Google-Flights-Data-Scraper-Flight-and-Price-Search` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--Google-Flights-Data-Scraper-Flight-and-Price-Search`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `departure_id` | string |  | `"LAX"` | Departure airport code(s), comma-separated for multiple (e.g., 'LAX', 'JFK', 'CDG,ORY'). Required for one-way and round-trip searches. Not used for multi-city trips. |
| `arrival_id` | string |  | `"JFK"` | Arrival airport code(s), comma-separated for multiple (e.g., 'JFK', 'SFO', 'LAX,SEA'). Required for one-way and round-trip searches. Not used for multi-city trips. |
| `outbound_date` | string |  | `"2026-11-27"` | Departure date in YYYY-MM-DD format (e.g., '2025-11-25'). Required for one-way and round-trip searches. Not used for multi-city trips. |
| `return_date` | string |  | `"2026-12-02"` | Return date in YYYY-MM-DD format (e.g., '2025-11-30'). Optional, used for round-trip searches. |
| `multi_city_json` | string |  |  | JSON string for multi-city trips. Format: [{"departure_id":"...","arrival_id":"...","date":"..."},...]. When provided, departure_id, arrival_id, and outbound_date are not required. |
| `adults` | integer |  | `1` | Number of adult passengers (default: 1, minimum: 1) |
| `children` | integer |  | `0` | Number of child passengers (default: 0, minimum: 0) |
| `infants` | integer |  | `0` | Number of infant passengers (default: 0, minimum: 0) |
| `currency` | string |  | `"USD"` | Currency code for prices (e.g., 'USD', 'EUR', 'GBP'). Default: 'USD' |
| `hl` | string: en, es, fr, de, it, pt … |  | `"en"` | Language code for results (e.g., 'en', 'fr', 'de', 'es'). Default: 'en' |
| `gl` | string: us, uk, ca, au, de, fr … |  | `"us"` | Country code for results (e.g., 'us', 'uk', 'fr', 'de'). Default: 'us' |
| `max_price` | integer |  |  | Maximum price filter in the specified currency. Optional. |
| `max_stops` | integer |  |  | Maximum number of stops (0 = direct flights only, 1 = one stop max, null = no limit). Optional. |
| `airlines` | string |  |  | Comma-separated list of preferred airline codes (e.g., 'UA,AA,DL'). Optional. |
| `exclude_basic` | boolean |  | `false` | If true, filters out Economy flights that include carry-on bags and free seat selection. Optional. |
| `fetch_booking_options` | boolean |  | `false` | If true, performs extra requests to retrieve detailed booking options (booking links, baggage fees, etc.). This increases API usage and is billed per booking option returned. |
| `max_pages` | integer |  | `1` | Maximum number of pages to fetch (0 = no limit, default: 1). |
| `output_file` | string |  |  | Optional filename to save results. If not provided, will auto-generate based on route and parameters. |

### Example

Ask the agent in plain language, or call `johnvc--Google-Flights-Data-Scraper-Flight-and-Price-Search` with arguments such as:

```json
{
  "departure_id": "LAX",
  "arrival_id": "JFK",
  "outbound_date": "2026-11-27",
  "return_date": "2026-12-02"
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `search_parameters` | object | Search Parameters |
| `search_metadata` | object | Search Metadata |
| `search_timestamp` | string | Search Timestamp |
| `page_number` | integer | Current Page Number |
| `all_flights` | array | Flat, one-row-per-flight summary of every itinerary on this page (best flights and other flights combined). Powers the Flights view so each flight renders as a single table row. The full nested itineraries remain availa… |
| `best_flights` | array | Best Flights |
| `other_flights` | array | Other Flights |
| `price_insights` | object | Price Insights |
| `airports` | array | Airports Information |
| `booking_options` | array | Booking Options |

## Data source and terms

Google Flights public search results, collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search
- Docs page: https://alphaosint.com/mcp/google-flights/
- All AlphaOSINT MCP servers: [index](../../README.md)
