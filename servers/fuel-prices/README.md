# Fuel Prices MCP server

Registry name: `io.github.johnisanerd/fuel-prices`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Look up current gas and diesel prices at US stations by ZIP code, city or GPS coordinates and get station name, address, distance, cash and credit prices across six grades, and posted times.

## When to use it

Station-level US retail fuel prices for a location. Use it for trip-cost estimates, fleet tools and local price comparisons.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/fuelprices`, which gives your agent a single tool, `johnvc--fuelprices`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/fuelprices` on your own Apify account and is billed there at the Actor's prices:

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/fuelprices`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http fuel-prices "https://mcp.apify.com/?tools=johnvc/fuelprices"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "fuel-prices": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/fuelprices"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "fuel-prices": {
      "url": "https://mcp.apify.com/?tools=johnvc/fuelprices"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fuel-prices": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/fuelprices"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--fuelprices` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--fuelprices`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `search` | string | yes | `"11507"` | ZIP code, city name, or latitude/longitude coordinates (e.g., '11507', 'New York', '36.0816642, -115.0534345'). Coverage is primarily the United States, with some Canadian locations. |
| `fuel` | integer |  | `1` | Fuel type to search for. 1=Regular (default), 2=Midgrade, 3=Premium, 4=Diesel, 5=E85, 12=Unleaded88. |
| `lang` | string: en |  | `"en"` | Language code for the search results. Currently only English is supported. |
| `maxAge` | integer |  | `0` | Maximum age of gas station data in days. Use 0 for no age restriction (all stations returned regardless of when prices were last reported). Higher values limit results to stations with prices reported within that many d… |
| `output_file` | string |  |  | Optional: Custom name for the output CSV file. If not provided, a timestamped filename will be automatically generated (e.g., gas_stations_11507_2025-08-19_11-01-12_1.csv). |

### Example

Ask the agent in plain language, or call `johnvc--fuelprices` with arguments such as:

```json
{
  "search": "11507",
  "fuel": 1,
  "lang": "en"
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `name` | string | Name of the gas station or brand (e.g., 'Shell', 'BP', 'USA'). |
| `distance` | number | Distance from the searched location in miles. |
| `priceUnit` | string | Currency and unit for fuel prices (e.g., 'USD/GAL'). |
| `ratingsCount` | integer | Total number of user ratings for this station. |
| `starRating` | number | Average star rating for this station (0-5). |
| `address_line1` | string | Primary street address of the station. |
| `address_line2` | string | Secondary address line (suite, unit, etc.), if any. |
| `address_locality` | string | City or locality where the station is located. |
| `address_region` | string | State or region abbreviation (e.g., 'NY', 'CA'). |
| `address_postalCode` | string | ZIP or postal code of the station. |
| `price_credit` | number | Fuel price per gallon when paying by credit card (USD). |
| `price_credit_postedTime` | string | ISO 8601 timestamp of when the credit price was last reported. |
| `price_cash` | number | Fuel price per gallon when paying by cash (USD). |
| `price_cash_postedTime` | string | ISO 8601 timestamp of when the cash price was last reported. |

## Data source and terms

Crowd-reported station prices from public US fuel-price listings, collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/fuelprices
- Docs page: https://alphaosint.com/mcp/fuel-prices/
- All AlphaOSINT MCP servers: [index](../../README.md)
