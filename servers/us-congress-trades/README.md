# US Congress Stock Trades MCP server

Registry name: `io.github.johnisanerd/us-congress-trades`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Search reported stock transactions by member, ticker, report date or date range and get the transaction, asset, amount range and filing details.

## When to use it

Government disclosure records, not market data. Use it for journalism, transparency research and tracking trades in a ticker.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/us-congress-financial-disclosures-and-stock-trading-data`, which gives your agent a single tool, `johnvc--us-congress-financial-disclosures-and-stock-trading-data`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/us-congress-financial-disclosures-and-stock-trading-data` on your own Apify account and is billed there at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Initiate | $0.001 | Start the server and answer a request. |
| Transaction Retreived | $0.0019 | Each transaction retrieved. |

Free-plan rates as of 2026-11-13; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00001). Current prices are on the Actor's page: https://apify.com/johnvc/us-congress-financial-disclosures-and-stock-trading-data

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/us-congress-financial-disclosures-and-stock-trading-data`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http us-congress-trades "https://mcp.apify.com/?tools=johnvc/us-congress-financial-disclosures-and-stock-trading-data"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "us-congress-trades": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/us-congress-financial-disclosures-and-stock-trading-data"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "us-congress-trades": {
      "url": "https://mcp.apify.com/?tools=johnvc/us-congress-financial-disclosures-and-stock-trading-data"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "us-congress-trades": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/us-congress-financial-disclosures-and-stock-trading-data"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--us-congress-financial-disclosures-and-stock-trading-data` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--us-congress-financial-disclosures-and-stock-trading-data`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `First_Name` | string |  | `""` | Filter by the first name of the congressional member. Case-insensitive partial match. Leave blank to search all members. |
| `Last_Name` | string |  | `""` | Filter by the last name of the congressional member. Case-insensitive partial match. Leave blank to search all members. |
| `Date_Reported` | string |  | `""` | Filter to disclosures with this exact transaction date in YYYY-MM-DD format. Leave blank to ignore. Use Start_Date and End_Date instead for a range. |
| `Start_Date` | string |  | `"2024-01-01"` | Earliest transaction date to include (inclusive), in YYYY-MM-DD format. Pair with End_Date for a range. Leave blank for no lower bound. |
| `End_Date` | string |  | `"2024-12-31"` | Latest transaction date to include (inclusive), in YYYY-MM-DD format. Pair with Start_Date for a range. Leave blank for no upper bound. |
| `Stock_Symbol` | string |  | `""` | Filter to transactions involving this ticker (e.g. AAPL, MSFT, NVDA). Case-insensitive partial match. Leave blank to include all tickers. |
| `Max_Results` | integer |  | `100` | Maximum number of disclosure records to return per run. Range 1-1000. Default 100. |

### Example

Ask the agent in plain language, or call `johnvc--us-congress-financial-disclosures-and-stock-trading-data` with arguments such as:

```json
{
  "First_Name": "",
  "Last_Name": "",
  "Date_Reported": "",
  "Start_Date": "2024-01-01",
  "End_Date": "2024-12-31",
  "Stock_Symbol": ""
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `Owner` | string | Code indicating who owns the asset. SP = spouse, DC = dependent child, JT = joint, blank = the member themselves. |
| `Asset` | string | Name of the financial asset or investment, including parenthetical ticker when present. |
| `Ticker` | string | Stock ticker symbol for publicly traded assets. Blank when the asset is not publicly listed. |
| `Asset_Type_Code` | string | Code indicating the type of asset. Common values: ST = stock, OP = options, MF = mutual fund, BD = bond, ET = ETF, CT = cryptocurrency. |
| `Transaction_Type` | string | Single-letter transaction code. P = purchase, S = sale, S (partial) = partial sale, E = exchange. |
| `Date` | string | Date the transaction occurred (YYYY-MM-DD). |
| `Notification_Date` | string | Date the transaction was reported to Congress (YYYY-MM-DD). |
| `Amount_Range` | string | Reported transaction amount as a bracket, e.g. '$1,001 - $15,000'. Members are required to report ranges, not exact values. |
| `Capital_Gains_Over_200` | string | Indicates whether capital gains from the transaction exceeded $200. |
| `Details` | string | Free-text details about the transaction, e.g. option strike prices and expiration dates. |
| `First_Name` | string | First name of the congressional member who filed the disclosure. |
| `Last_Name` | string | Last name of the congressional member who filed the disclosure. |
| `State_District` | string | State (and district for House members) of the congressional member, e.g. 'CA11'. |
| `House` | string | Congressional chamber: 'House' or 'Senate'. |
| `Filing_ID` | string | Unique identifier for the financial disclosure filing. |
| `DocID` | string | Unique identifier for the source disclosure document. |
| `Year` | string | Year the financial disclosure was filed. |
| `PDF_Quality` | string | Source extraction path: 'text' or 'text-miner' (machine-readable House PDF), 'html' (Senate web filing), 'image' (scanned filing parsed with vision). |
| `created_at` | string | ISO timestamp when this record was added to the dataset. |
| `search_metadata` | object | Echo of the search parameters and timing for this run. |

## Data source and terms

Public financial disclosure filings that House and Senate members file under the STOCK Act. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/us-congress-financial-disclosures-and-stock-trading-data
- Docs page: https://alphaosint.com/mcp/us-congress-trades/
- All AlphaOSINT MCP servers: [index](../../README.md)
