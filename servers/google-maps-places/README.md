# Google Maps Places MCP server

Registry name: `io.github.johnisanerd/google-maps-places`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Search Google Maps for places by keyword and location and get business name, address, phone, website, rating, review count, categories, coordinates and opening hours.

## When to use it

Bulk place lists from Google Maps, where Google Local returns the local results for a single search. Use it for lead lists, market mapping and store-location research.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/google-maps-places-api`, which gives your agent a single tool, `johnvc--google-maps-places-api`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/google-maps-places-api` on your own Apify account and is billed there at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| place Place (standard) | $0.002 | Per unique place returned in standard mode: name, address, phone, website, coordinates, and (when available) rating, review count, price level, category. |
| Place (rich details) | $0.004 | Per unique place when Rich Details is enabled: adds opening hours, rating, review count, category types, description, photo thumbnail, booking links, and Place ID. |

Free-plan rates as of 2026-11-13; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00005, $0.00001). Current prices are on the Actor's page: https://apify.com/johnvc/google-maps-places-api

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/google-maps-places-api`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http google-maps-places "https://mcp.apify.com/?tools=johnvc/google-maps-places-api"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "google-maps-places": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/google-maps-places-api"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "google-maps-places": {
      "url": "https://mcp.apify.com/?tools=johnvc/google-maps-places-api"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-maps-places": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/google-maps-places-api"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--google-maps-places-api` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--google-maps-places-api`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `searchTerms` | array | yes | `["coffee shops in Austin, TX"]` | One or more searches, for example 'coffee shops in Austin, TX' or 'dentists in 90210'. Each term is searched independently. Include a location here, or set the Location field below to apply one to every term. |
| `location` | string |  |  | Optional place to focus all search terms on, for example 'Austin, TX, United States'. Leave blank if your terms already include a location. |
| `maxResultsPerSearch` | integer |  | `20` | How many places to return per search term. Results come in pages of about 20; the Actor pulls just enough pages to reach this count, then stops early when a term runs out of places. Minimum 20. |
| `language` | string |  |  | Optional two-letter language code for results, for example 'en', 'es', 'fr'. |

### Example

Ask the agent in plain language, or call `johnvc--google-maps-places-api` with arguments such as:

```json
{
  "searchTerms": [
    "coffee shops in Austin, TX"
  ]
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `searchTerm` | string | The search term this place was returned for. |
| `position` | integer | Rank of the place within its result page. |
| `title` | string | Business or place name. |
| `address` | string | Full street address. |
| `latitude` | number | Latitude coordinate. |
| `longitude` | number | Longitude coordinate. |
| `rating` | number | Average star rating, when available. |
| `ratingCount` | integer | Number of ratings, when available. |
| `priceLevel` | string | Relative price indicator such as '$$' or '$1-10', when available. |
| `type` | string | Primary place category. |
| `types` | array | All place categories. |
| `phoneNumber` | string | Contact phone number, when available. |
| `website` | string | Website URL, when available. |
| `description` | string | Short place description, when available. |
| `openingHours` | object | Map of weekday to opening hours, when available. |
| `bookingLinks` | array | Booking or reservation links, when available. |
| `thumbnailUrl` | string | Place photo thumbnail. |
| `cid` | string | Google customer/place identifier. |
| `fid` | string | Google feature identifier. |
| `placeId` | string | Google Place ID. |
| `error_message` | string | Present only on error rows; explains why a request could not be completed. |
| `cached` | boolean | True when the place came from an identical search made in the last 24 hours; false when it was fetched in this run. |
| `fetchedAt` | string | When the results page holding this place was fetched (ISO 8601, UTC). |
| `cacheAgeDays` | number | Present only on reused rows: how old the reused results page was, in days (0.25 = 6 hours). |

## Data source and terms

Google Maps' public place listings, collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/google-maps-places-api
- Docs page: https://alphaosint.com/mcp/google-maps-places/
- All AlphaOSINT MCP servers: [index](../../README.md)
