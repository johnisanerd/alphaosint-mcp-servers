# Workday Careers MCP server

Registry name: `io.github.johnisanerd/workday-careers`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

List every job on a company's Workday careers site with title, location, posted date, full description, pay range when published, employment type, remote status and apply link.

## When to use it

Jobs straight from the employer's own careers site, including roles that never reach job boards. Use it for hiring-signal research, job monitoring at target companies and job search agents.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/workday-careers-api`, which gives your agent a single tool, `johnvc--workday-careers-api`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/workday-careers-api` on your own Apify account and is billed there at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Job result | $0.0001 | Charged once per job posting returned to the dataset. Error rows are never charged. |
| Actor start | $0.001 | Charged once when a run starts. |

Free-plan rates as of 2026-11-12; paid Apify plans pay less per event. Current prices are on the Actor's page: https://apify.com/johnvc/workday-careers-api

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/workday-careers-api`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http workday-careers "https://mcp.apify.com/?tools=johnvc/workday-careers-api"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "workday-careers": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/workday-careers-api"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "workday-careers": {
      "url": "https://mcp.apify.com/?tools=johnvc/workday-careers-api"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "workday-careers": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/workday-careers-api"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--workday-careers-api` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--workday-careers-api`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `startUrls` | array | yes | `[{"url": "https://workday.wd5.myworkdayjobs.com/Workday"}]` | REQUIRED. One or more Workday careers site URLs. Every public form works: https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite, locale variants like https://intel.wd1.myworkdayjobs.com/en-US/External, and the m… |
| `searchText` | string |  | `""` | Optional keyword query passed to the site's own job search (matches titles and descriptions the same way the search box on the careers page does). Leave empty to return every job. |
| `maxJobsPerSite` | integer |  | `0` | Soft cap on jobs returned per start URL. 0 means all jobs on the site. Useful to keep test runs small and cheap. |
| `includeDetails` | boolean |  | `true` | When true (default), the actor opens each job's detail record to add the full description, exact ISO posted and end dates, employment type, all locations, country, and apply URL. When false, only the fast list fields ar… |
| `descriptionFormat` | string: both, html, text |  | `"both"` | Format of the job description fields when details are fetched: 'html' keeps the original rich text, 'text' returns clean plain text, 'both' (default) returns both fields. |
| `postedAfter` | string |  |  | Optional ISO date filter (YYYY-MM-DD). Only jobs posted on or after this date are returned. Requires 'Fetch full job details', because the list endpoint carries only relative dates ('Posted Today', 'Posted 30+ Days Ago'… |
| `detailConcurrency` | integer |  | `5` | How many job-detail requests run in parallel (1 to 10, default 5). The actor always paces list pages and backs off politely on rate limits; raise this only for very large sites. |

### Example

Ask the agent in plain language, or call `johnvc--workday-careers-api` with arguments such as:

```json
{
  "startUrls": [
    {
      "url": "https://workday.wd5.myworkdayjobs.com/Workday"
    }
  ],
  "searchText": "",
  "maxJobsPerSite": 50
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `resultType` | string: job, error | Row kind discriminator: 'job' for a job posting, 'error' for a start URL that could not be scraped. Filter on it to separate data from diagnostics. |
| `title` | string | The job posting's title. |
| `company` | string | Hiring organization name from the job record, falling back to the Workday tenant name. |
| `tenant` | string | The Workday tenant identifier parsed from the careers URL. Use it to join rows back to a tenant-discovery dataset. |
| `siteId` | string | The Workday career-site slug within the tenant (one tenant can host several sites). |
| `sourceUrl` | string | The start URL this row came from, exactly as provided in the input. |
| `url` | string | Public job posting page URL. |
| `applyUrl` | string | Direct application URL (the job URL plus /apply). |
| `jobReqId` | string | The employer's job requisition ID (for example JR1990000). Stable identifier for deduplication across runs. |
| `jobPostingId` | string | Workday's posting slug identifier (detail mode only). |
| `workdayInternalId` | string | Workday's internal GUID for the posting (detail mode only). |
| `externalPath` | string | The posting's path fragment on the careers site, as returned by the list endpoint. |
| `locationsText` | string | Location summary as shown on the job card (a single location or e.g. '11 Locations'). |
| `primaryLocation` | string | The posting's primary location (detail mode only). |
| `additionalLocations` | array | Every additional location on multi-location postings (detail mode only). |
| `country` | string | Country of the primary location (detail mode only). |
| `countryCode` | string | ISO alpha-2 country code of the primary location (detail mode only). |
| `postedOn` | string | Relative posted date exactly as the careers site shows it. |
| `postedDate` | string | Exact ISO posting date (detail mode only). |
| `endDate` | string | ISO date the posting stops accepting applications, when the employer sets one (detail mode only). |
| `timeLeftToApply` | string | Human-readable time remaining to apply, when the employer sets an end date (detail mode only). |
| `timeType` | string | Employment time type such as Full Time or Part Time (detail mode only). |
| `remoteType` | string | Work arrangement label when the site exposes one (for example Remote, Flex, Onsite). |
| `canApply` | boolean | Whether the posting currently accepts applications (detail mode only). |
| `descriptionHtml` | string | Full job description as rich HTML (detail mode, when descriptionFormat is html or both). |
| `descriptionText` | string | Full job description as clean plain text (detail mode, when descriptionFormat is text or both). |
| `salaryText` | string | Best-effort pay range snippet extracted from the description when the employer publishes one. Null when no range is stated. |
| `salaryMin` | number | Lower bound of the extracted pay range. Null when no range is stated. |
| `salaryMax` | number | Upper bound of the extracted pay range. Null when no range is stated. |
| `salaryCurrency` | string | Currency of the extracted pay range (ISO code where the symbol maps cleanly). Null when no range is stated. |
| `scrapedAt` | string | UTC timestamp of this run. |
| `totalJobsOnSite` | integer | Total number of jobs the careers site reported at scrape time (before any max cap or filters). |
| `errorMessage` | string | Human-readable reason a start URL failed (rows with resultType 'error' only). |

## Data source and terms

Employers' public Workday careers sites (myworkdayjobs.com and myworkdaysite.com). The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/workday-careers-api
- Docs page: https://alphaosint.com/mcp/workday-careers/
- All AlphaOSINT MCP servers: [index](../../README.md)
