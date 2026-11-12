# Crunchbase Company MCP server

Registry name: `io.github.johnisanerd/crunchbase-company`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Look up companies by Crunchbase organization URL and get funding rounds and totals, investors, industries, headquarters, employee count, rank and operating status.

## When to use it

Funding and investor data for named companies, rather than a search across the whole database. Use it for account research, investor diligence and enriching a company list.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/crunchbase-company-api`, which gives your agent a single tool, `johnvc--crunchbase-company-api`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/crunchbase-company-api` on your own Apify account and is billed there at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Company scraped | $0.006 | Fee per company returned. Charged once for each company pushed to the dataset. |
| Name or domain lookup | $0.002 | Fee per company name or website domain looked up (companyNames), charged whether or not a match is found. Organization URLs (companyUrls) never pay it. |

Free-plan rates as of 2026-11-12; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00001, $0.00001). Current prices are on the Actor's page: https://apify.com/johnvc/crunchbase-company-api

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/crunchbase-company-api`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http crunchbase-company "https://mcp.apify.com/?tools=johnvc/crunchbase-company-api"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "crunchbase-company": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/crunchbase-company-api"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "crunchbase-company": {
      "url": "https://mcp.apify.com/?tools=johnvc/crunchbase-company-api"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "crunchbase-company": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/crunchbase-company-api"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--crunchbase-company-api` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--crunchbase-company-api`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `companyUrls` | array |  | `["https://www.crunchbase.com/organization/openai"]` | One or more Crunchbase organization URLs, e.g. https://www.crunchbase.com/organization/openai. URLs that are not Crunchbase /organization/ URLs are skipped. Up to 100 per run. Need larger batches? Contact us and we can… |
| `companyNames` | array |  |  | Look companies up by name or website domain, e.g. "OpenAI" or "basecamp.com". Each entry resolves to the single top-matching Crunchbase organization and returns the same full company row as a URL, at the same per-compan… |

### Example

Ask the agent in plain language, or call `johnvc--crunchbase-company-api` with arguments such as:

```json
{
  "companyUrls": [
    "https://www.crunchbase.com/organization/openai"
  ]
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `result_type` | string | Either 'company' (a collected company) or 'error' (a validation or collection error row). |
| `searchTerm` | string | The company name or website domain from companyNames that produced this row. Only present on rows resolved by name lookup; use it to join results back to your input list. |
| `name` | string | The company name. |
| `legalName` | string | The registered legal name, when available. |
| `cbRank` | integer | The company's Crunchbase rank (lower is more prominent). |
| `description` | string | The company overview / about text. |
| `website` | string | The company website URL. |
| `logoUrl` | string | Company logo image URL. |
| `hqLocation` | string | Headquarters location (city, region, country). |
| `region` | string | Headquarters region or state. |
| `country` | string | Headquarters country. |
| `hqRegions` | array | Broader regions for the headquarters location. |
| `continent` | string | Headquarters continent. |
| `employeeCount` | string | Employee-count band as reported by Crunchbase. |
| `operatingStatus` | string | Operating status (e.g. active, closed). |
| `companyType` | string | Company type (e.g. for_profit, non_profit). |
| `ipoStatus` | string | IPO status (e.g. private, public). |
| `stockSymbol` | string | Public stock ticker, when the company is public. |
| `industries` | array | Industry tags. |
| `totalFunding` | string | Total funding raised in USD, only when the source exposes a company-level total (currently often unavailable). Never estimated or derived; omitted rather than guessed. |
| `numFundingRounds` | integer | Number of funding rounds. |
| `numInvestors` | integer | Number of investors. |
| `numLeadInvestors` | integer | Number of lead investors. |
| `numAcquisitions` | integer | Number of acquisitions the company has made. |
| `investors` | array | Distinct investor names. |
| `founders` | array | Founder names. |
| `fundingRounds` | array | Per-round detail: round label, stage, investors, and lead investors. The source exposes structure publicly but gates dollar amounts and dates behind login, so those are never included. The source caps this list; numFund… |
| `keyPeople` | array | Current executives and key people with titles. |
| `advisors` | array | Board members and advisors. |
| `contacts` | array | Named contacts with job title, departments, and LinkedIn handle, as listed publicly by the source. |
| `numContacts` | integer | Total number of contacts the source lists for the company. |
| `products` | array | Named products and services with short descriptions. |
| `similarCompanies` | array | Similar or competing companies with profile URLs. |
| `recentNews` | array | Up to 5 recent news mentions with date, publisher, and URL. |
| `acquisitions` | array | Names of companies this company has acquired. |
| `subOrganizations` | array | Subsidiaries and joint ventures. |
| `contactEmail` | string | Public contact email, when listed. |
| `contactPhone` | string | Public contact phone number. |
| `monthlyVisits` | integer | Estimated monthly website visits. |
| `monthlyVisitsGrowth` | number | Month-over-month change in website visits as a fraction (0.15 means +15%). |
| `growthScore` | integer | Crunchbase growth score. |
| `growthTrend` | integer | Growth score change over the past quarter. |
| `heatScore` | integer | Crunchbase heat score. |
| `heatTrend` | integer | Heat score change over the past quarter. |
| `techStackCount` | integer | Number of technologies detected on the company website. |
| `techStack` | array | Detected website technologies (sampled by the source). |
| `patentsGranted` | integer | Number of granted patents. |
| `trademarksRegistered` | integer | Number of registered trademarks. |
| `itSpendEstimateUsd` | integer | Estimated annual IT spend in USD. |
| `monthlyAppDownloads` | integer | Estimated monthly mobile app downloads. |
| `socialMediaLinks` | array | Social media profile URLs. |
| `companyUrl` | string | The Crunchbase organization URL. |
| `summary` | string | Plain-language one-line interpretation of the company. |
| `cached` | boolean | True when this row was served from a company record collected earlier (within the last 30 days) instead of collected live. Charged like a live row. Also true on a stale row. Present only when caching is enabled. |
| `cacheAgeDays` | integer | Whole days between fetched_at and this run. Only on cached or stale rows. |
| `stale` | boolean | True when the live collection of this company did not complete and the row is the last good copy, older than 30 days but at most 45 days old. Never charged. See note. |
| `note` | string | Explains an unusual row, for example why a stale copy was returned. |
| `fetched_at` | string | ISO 8601 time the company data was collected from the source. On a cached or stale row this is the time of the original collection, not of this run. |
| `error_message` | string | Human-readable error description. Only present on rows with result_type='error'. |
| `error_type` | string | Machine-readable error category (e.g. 'MissingRequiredParameter', 'MissingApiKey', 'CollectionError'). |

## Data source and terms

Crunchbase's public organization pages, collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/crunchbase-company-api
- Docs page: https://alphaosint.com/mcp/crunchbase-company/
- All AlphaOSINT MCP servers: [index](../../README.md)
