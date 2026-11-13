# Google Jobs MCP server

Registry name: `io.github.johnisanerd/google-jobs`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Search job postings by keyword and location across Google's 184 country domains and get structured rows with title, company, location, posting age, application links and the full description.

## When to use it

Google Jobs aggregates postings from LinkedIn, Indeed, company career sites and many smaller boards, so one query covers the whole market. Use it for job search agents, hiring-signal research and labor-market analysis.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/Google-Jobs-Scraper`, which gives your agent a single tool, `johnvc--Google-Jobs-Scraper`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/Google-Jobs-Scraper` on your own Apify account and is billed there at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Page Processed (up to 10 jobs) | $0.09 | Fee per page of search results returned (typically 10 job results) |

Free-plan rates as of 2026-11-13; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00001, $0.00005). Current prices are on the Actor's page: https://apify.com/johnvc/Google-Jobs-Scraper

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/Google-Jobs-Scraper`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http google-jobs "https://mcp.apify.com/?tools=johnvc/Google-Jobs-Scraper"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "google-jobs": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/Google-Jobs-Scraper"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "google-jobs": {
      "url": "https://mcp.apify.com/?tools=johnvc/Google-Jobs-Scraper"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-jobs": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/Google-Jobs-Scraper"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--Google-Jobs-Scraper` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--Google-Jobs-Scraper`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | yes | `"Software Engineer"` | The job search query (e.g., 'Software Engineer', 'Data Scientist', 'Marketing Manager') |
| `location` | string |  | `"San Francisco, CA"` | Job location (city, state, or country). We recommend specifying a location at the city level for best results. If left empty and a Country Code is selected, the country name is used as the location automatically. If Goo… |
| `country` | string: None, dz, as, ai, ag, ar … |  | `"None"` | Country the search targets - this is what drives regional results (Google's gl parameter), and when Job Location is empty the country's name is used as the location automatically. If unset, it is derived from the Google… |
| `language` | string: None, en, es, fr, de, it … |  | `"None"` | Interface language for the search (Google's hl parameter). Optional and usually best left unset: Google then uses the language that matches the country, which is required in many non-English markets - explicitly setting… |
| `google_domain` | string: google.com, google.co.uk, google.ca, google.de, google.fr, google.com.a… |  | `"google.com"` | Google domain to use for search. Also determines the default country when the Country Code input is unset (e.g. google.de -> de). Domains of countries where Google Jobs is unavailable stop the run with a clear message a… |
| `posted_within` | string: any, 24h, 3d, 7d, 30d |  | `"any"` | Only return jobs posted within this window. Great for daily scheduled runs: set 'Last 24 hours' to avoid re-collecting listings you already scraped. Default 'Any time' applies no date filter (existing runs and tasks are… |
| `num_results` | integer |  | `100` | Maximum number of job results to return |
| `max_pagination` | integer |  | `0` | Maximum number of pages to fetch (each page has ~10 results). Set to 0 for unlimited pagination (fetch all available pages). |
| `include_lrad` | boolean |  | `false` | Whether to include location radius filtering |
| `lrad_value` | string |  | `"5"` | Location radius value in km (e.g., '2', '5', '10'). Only used when include_lrad is true. |
| `max_delay` | integer |  | `1` | Delay between API requests in seconds (to avoid rate limiting) |
| `output_file` | string |  | `"google_jobs_results.json"` | Custom filename for saving results. Leave empty for auto-generated filename. |

### Example

Ask the agent in plain language, or call `johnvc--Google-Jobs-Scraper` with arguments such as:

```json
{
  "query": "Software Engineer",
  "location": "San Francisco, CA",
  "lrad_value": "5",
  "output_file": "google_jobs_results.json"
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `company_name` | string | Name of the company posting the job. |
| `location` | string | Location of this posting as published by the source (city, state, remote, etc.). Null when the listing carries none. This is the posting's own location, not the location you searched for - see search_location. |
| `search_location` | string | The location this run searched, echoed from the input. Null when the run sent no location. |
| `via` | string | The platform or site where the job was listed (e.g., 'via LinkedIn', 'via Indeed'). |
| `job_highlights` | array | Structured highlights including Qualifications, Responsibilities, and Benefits sections. |
| `related_links` | array | Links related to the job or company. |
| `thumbnail` | string | URL of the company logo thumbnail. |
| `job_id` | string | Unique Google Jobs identifier for this listing. |
| `detected_extensions` | object | Structured job metadata extracted by Google: posted_at, schedule_type, health_insurance, dental_coverage, paid_time_off, etc. |
| `extensions` | array | Raw job metadata tags (e.g., 'Full-time', '3 days ago', 'Health insurance'). |
| `share_link` | string | Google-generated shareable link for this job listing. |
| `apply_options` | array | List of platforms where you can apply, each with a title and direct link. |
| `query` | string | The search query used to find this job. |
| `country` | string | Country code used for the search (e.g., 'us', 'gb'). |
| `language` | string | Language code used for the search (e.g., 'en'). |
| `google_domain` | string | Google domain used for the search (e.g., 'google.com'). |
| `search_timestamp` | string | ISO 8601 timestamp of when the search was performed. |
| `total_jobs_found` | integer | Total number of job listings found across all pages for this search. |
| `pages_processed` | integer | Number of result pages fetched during this run. |

## Data source and terms

Google's public job search results (the Google Jobs panel), collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/Google-Jobs-Scraper
- Docs page: https://alphaosint.com/mcp/google-jobs/
- All AlphaOSINT MCP servers: [index](../../README.md)
