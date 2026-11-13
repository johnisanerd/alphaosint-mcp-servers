# Google Shopping MCP server

Registry name: `io.github.johnisanerd/google-shopping`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Search products and get listings with price, seller, rating, delivery information and discount tags, with filters for location, price range, sort order, free shipping and sale items.

## When to use it

Cross-retailer product prices for a query rather than a single store's catalog. Use it for price comparison, deal finding and competitor price monitoring.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/google-shopping-api-google-shopping-products-prices-deals`, which gives your agent a single tool, `johnvc--google-shopping-api-google-shopping-products-prices-deals`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/google-shopping-api-google-shopping-products-prices-deals` on your own Apify account and is billed there at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Setup | $0.02 | One-time setup fee per Actor run. Covers initialization and API provisioning costs. |
| Page Processed | $0.02 | Fee per page of shopping results processed. Each page returns approximately 40 product listings. |

Free-plan rates as of 2026-11-13; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00001, $0.00001). Current prices are on the Actor's page: https://apify.com/johnvc/google-shopping-api-google-shopping-products-prices-deals

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/google-shopping-api-google-shopping-products-prices-deals`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http google-shopping "https://mcp.apify.com/?tools=johnvc/google-shopping-api-google-shopping-products-prices-deals"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "google-shopping": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/google-shopping-api-google-shopping-products-prices-deals"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "google-shopping": {
      "url": "https://mcp.apify.com/?tools=johnvc/google-shopping-api-google-shopping-products-prices-deals"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-shopping": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/google-shopping-api-google-shopping-products-prices-deals"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--google-shopping-api-google-shopping-products-prices-deals` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--google-shopping-api-google-shopping-products-prices-deals`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `q` | string | yes | `"wireless headphones"` | The product or keyword to search for on Google Shopping. Example: 'wireless headphones', 'iPhone 15 case'. |
| `location` | string |  |  | Geographic location to localize the search results. Example: 'Austin, Texas, United States', 'London, England, United Kingdom'. |
| `gl` | string |  |  | Two-letter country code for Google to use. Examples: 'us', 'uk', 'de', 'fr', 'ca', 'au'. |
| `hl` | string |  |  | Two-letter language code for results. Examples: 'en', 'es', 'de', 'fr', 'ja'. |
| `google_domain` | string |  |  | Google domain to use for the search. Defaults to 'google.com'. Examples: 'google.co.uk', 'google.de', 'google.fr'. |
| `device` | string: desktop, tablet, mobile |  | `"desktop"` | Device type to simulate. Different devices may return slightly different results and prices. |
| `min_price` | number |  |  | Filter results to only show products above this price (in the local currency). |
| `max_price` | number |  |  | Filter results to only show products below this price (in the local currency). |
| `sort_by` | integer |  |  | Sort results by price. 1 = price low to high, 2 = price high to low. Leave blank for default relevance sorting. |
| `free_shipping` | boolean |  | `false` | When enabled, only return products that offer free shipping. |
| `on_sale` | boolean |  | `false` | When enabled, only return products that are currently on sale or have a discount. |
| `max_pages` | integer |  | `1` | Maximum number of result pages to fetch. Each page contains approximately 40 products. Set to 0 for no limit (fetches all available pages). Default is 1. |
| `output_file` | string |  |  | Optional filename for saving results as a JSON file locally. If not provided, a timestamped filename is generated automatically. |

### Example

Ask the agent in plain language, or call `johnvc--google-shopping-api-google-shopping-products-prices-deals` with arguments such as:

```json
{
  "q": "wireless headphones"
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `search_parameters` | object | The input parameters used for this search, echoed back in each result page for traceability. |
| `search_metadata` | object | Aggregate statistics about the search run: total results, pages processed, and pagination status. |
| `search_timestamp` | string | ISO 8601 timestamp of when this search page was executed. |
| `page_number` | integer | 1-indexed page number this dataset item represents. Each page of results is pushed as a separate item. |
| `shopping_results` | array | Array of product listings returned on this page. Each item includes title, price, source, rating, reviews, delivery, and more. |
| `filters` | array | Filter options available for narrowing results. Only present on the first page of results. |
| `error` | boolean | True when this dataset item represents an error record rather than search results. |
| `error_message` | string | Human-readable description of the error that occurred, if error is true. |
| `error_type` | string | Machine-readable error category (e.g., 'InsufficientFunds', 'ValidationError', 'APIError'). |
| `timestamp` | string | ISO 8601 timestamp of when the error occurred. Only present on error records. |

## Data source and terms

Google Shopping public search results, collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/google-shopping-api-google-shopping-products-prices-deals
- Docs page: https://alphaosint.com/mcp/google-shopping/
- All AlphaOSINT MCP servers: [index](../../README.md)
