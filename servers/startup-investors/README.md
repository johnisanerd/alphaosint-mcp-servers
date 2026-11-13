# Startup Investors MCP server

Registry name: `io.github.johnisanerd/startup-investors`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Search investment firms by type, stage, sector and location and get firm profiles, with optional partner contacts.

## When to use it

Investor lists for fundraising, not company or people data. Use it to build fundraising target lists and research the venture market.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/startup-investors-data-scraper`, which gives your agent a single tool, `johnvc--startup-investors-data-scraper`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/startup-investors-data-scraper` on your own Apify account and is billed there at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Start the Actor | $0.01 | One-time setup fee per Actor run. Turn it on, tune it up, and go. |
| Firm Returned | $0.04 | Fee per firm processed. This is the cost to return a single firm. |
| Contacts Returned | $0.02 | Fee per contact returned. If contacts are requested for each firm, this is the cost to return a single contact with all the details we have in our database of the investor at the firm. |

Free-plan rates as of 2026-11-13; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00001). Current prices are on the Actor's page: https://apify.com/johnvc/startup-investors-data-scraper

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/startup-investors-data-scraper`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http startup-investors "https://mcp.apify.com/?tools=johnvc/startup-investors-data-scraper"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "startup-investors": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/startup-investors-data-scraper"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "startup-investors": {
      "url": "https://mcp.apify.com/?tools=johnvc/startup-investors-data-scraper"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "startup-investors": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/startup-investors-data-scraper"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--startup-investors-data-scraper` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--startup-investors-data-scraper`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `Firm_Types` | array |  | `["Venture Capital Investor"]` | Filter by one or more investor firm types. Combine multiple types to broaden the search (e.g. ['Venture Capital Investor', 'Angel Investor']). |
| `Focus_Areas` | array |  | `["Artificial Intelligence"]` | Filter by one or more industries the investor firm targets. Combine multiple focus areas to broaden the search (e.g. ['Artificial Intelligence', 'Biotechnology']). |
| `Investment_Stages` | array |  | `["Seed", "Series A"]` | Filter by one or more investment stages the firm participates in. Recommended values: Pre-Seed, Seed, Series A, Series B, Series C, Series D, Late Stage, Growth, Private Equity, Mezzanine, IPO, Debt. Other values pass t… |
| `Countries` | array |  | `["United States"]` | Filter by one or more countries where the firm is headquartered. Use full English country names. Common values: United States, United Kingdom, Canada, Germany, France, India, China, Israel, Singapore, Australia, Japan,… |
| `Keyword` | string |  | `"Sequoia"` | Search across firm names, descriptions, and other text fields. Use a partner name, firm name, or thesis keyword. Leave empty to search the full database. Example: 'Sequoia', 'climate', 'fintech'. |
| `Max_Results` | integer |  | `100` | Maximum number of investor firm records to return. Range: 1-10000. Default: 100. Each firm is billed at the per-firm rate; setting this high without other filters can run up cost - use Keyword or Firm_Types to narrow fi… |
| `Offset` | integer |  | `0` | Skip this many firms before returning results. Combine with Max_Results to paginate across multiple runs (e.g. Max_Results=1000 + Offset=0 for page 1; Offset=1000 for page 2). For gap-free pagination, sort on a unique f… |
| `Order_By` | string: created_at, firm_name, firm_country, firm_type_id |  | `"created_at"` | Order results by a single field. One of: created_at (newest firms first), firm_name (alphabetical), firm_country (grouped by country), firm_type_id (grouped by firm type). Unknown values fall back to created_at. |
| `Order_Direction` | string: asc, desc |  | `"desc"` | Sort direction for the Order_By field. 'desc' returns highest/newest first; 'asc' returns lowest/oldest first. |
| `Include_Contacts` | boolean |  | `false` | Enable to include the investor_contacts array on every firm returned. Each contact includes name, job title, email (when available), LinkedIn URL, and other social profiles. Charged separately at the per-contact rate. |

### Example

Ask the agent in plain language, or call `johnvc--startup-investors-data-scraper` with arguments such as:

```json
{
  "Firm_Types": [
    "Venture Capital Investor"
  ],
  "Focus_Areas": [
    "Artificial Intelligence"
  ],
  "Investment_Stages": [
    "Seed",
    "Series A"
  ],
  "Countries": [
    "United States"
  ],
  "Keyword": "Sequoia",
  "Offset": 0
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `firm_id` | integer | Unique numeric identifier for the investor firm in our database. |
| `firm_type_id` | string | Short code for the firm type (e.g., 'VC' for Venture Capital, 'A' for Angel, 'PE' for Private Equity). |
| `firm_type_name` | string | Full name of the firm type (e.g., 'Venture Capital Investor', 'Angel Investor'). |
| `firm_name` | string | Name of the investor firm. |
| `firm_description` | string | Detailed description of the firm and its investment focus. |
| `firm_address_1` | string | Primary address line of the firm's headquarters. |
| `firm_address_2` | string | Secondary address line (suite, floor, etc.). |
| `firm_city` | string | City where the firm is headquartered. |
| `firm_state` | string | State, province, or region of the firm's headquarters. |
| `firm_country` | string | Country where the firm is headquartered. |
| `firm_zip` | string | ZIP or postal code of the firm's headquarters. |
| `firm_phone` | string | Contact phone number for the firm. |
| `firm_website` | string | Official website URL of the firm. |
| `firm_linkedin_url` | string | LinkedIn company page URL of the firm. |
| `crunchbase_uuid` | string | Unique identifier in the Crunchbase database for cross-referencing. |
| `crunchbase_url` | string | Crunchbase profile URL of the firm. |
| `twitter_url` | string | Twitter (X) profile URL of the firm. |
| `facebook_url` | string | Facebook page URL of the firm. |
| `firm_stages` | array | Investment stages the firm participates in (e.g., ['Seed', 'Series A', 'Series B']). |
| `firm_aum` | number | Total assets under management (AUM) of the firm in USD. May be 0 if not disclosed. |
| `firm_focus` | array | Industries and focus areas the firm targets. |
| `industry_names` | array | Industry classifications associated with the firm (joined from the industries table). |
| `last_checked` | string | ISO timestamp when the firm record was last verified against source data. |
| `created_at` | string | ISO timestamp when this record was created in our database. |
| `updated_at` | string | ISO timestamp when this record was last updated. |
| `investor_contacts` | array | Verified investor contacts (partners, principals, associates) at this firm. Only present when Include_Contacts is enabled. Each contact uses 'job_title' for the role/position. |
| `search_metadata` | object | Diagnostic metadata about the search query that produced this row: filters used, timestamp, total results, and execution time. |

## Data source and terms

A curated database of about 10,500 investment firms compiled from public firm profiles. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/startup-investors-data-scraper
- Docs page: https://alphaosint.com/mcp/startup-investors/
- All AlphaOSINT MCP servers: [index](../../README.md)
