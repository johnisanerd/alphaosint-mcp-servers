# LinkedIn People Search MCP server

Registry name: `io.github.johnisanerd/linkedin-people-search`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Find people by name, job title, employer, school or location and get profile URL, headline, current employer, location, and optionally about text, work history and education.

## When to use it

Finds people you don't have profile links for yet, where profile tools need the URL first. Use it for prospect lists, recruiting searches and finding the right contact at a company.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/linkedin-people-search-api`, which gives your agent a single tool, `johnvc--linkedin-people-search-api`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/linkedin-people-search-api` on your own Apify account and is billed there at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Person found | $0.0006 | Fee per person delivered to the dataset, with their public LinkedIn profile URL, name, headline and current employer. Charged once per person, never per search page, and never twice for the same person in one run. |
| Person enriched | $0.0025 | Fee per person whose public profile page was opened and parsed, adding the about text, work history, education, follower count, photo and languages. Charged only when the enrichment actually returned data. |

Free-plan rates as of 2026-11-13; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00001, $0.00001). Current prices are on the Actor's page: https://apify.com/johnvc/linkedin-people-search-api

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/linkedin-people-search-api`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http linkedin-people-search "https://mcp.apify.com/?tools=johnvc/linkedin-people-search-api"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "linkedin-people-search": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/linkedin-people-search-api"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "linkedin-people-search": {
      "url": "https://mcp.apify.com/?tools=johnvc/linkedin-people-search-api"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "linkedin-people-search": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/linkedin-people-search-api"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--linkedin-people-search-api` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--linkedin-people-search-api`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `firstName` | string |  |  | First name of the person to find, for example Jane. Combined with lastName into an exact-phrase search, so the two together find people by full name. Leave both name fields empty only if you are searching with the keywo… |
| `lastName` | string |  |  | Last name of the person to find, for example Doe. Combined with firstName into an exact-phrase search. |
| `keywords` | string |  |  | Extra search terms to add to the query, for example a skill, an employer or an industry word. Use this on its own to search without a specific name, or alongside a name to narrow the matches. |
| `jobTitle` | string |  |  | Job title to require, for example Software Engineer. Only people whose public profile or search snippet mentions this title are returned. |
| `company` | string |  |  | Employer name to require, for example Microsoft. Matches people whose public profile mentions this company, current or past. |
| `school` | string |  |  | School or university name to require, for example Stanford University. |
| `location` | string |  |  | Place to require, for example San Francisco or United Kingdom. Matched as text against the public profile, so a city, region or country all work. |
| `maxResults` | integer |  | `25` | Stop after delivering this many people. You are charged only for the people actually returned. Each search fetches a full page of ten results at once, so a run returns at least ten people when the query has that many ma… |
| `enrichProfiles` | boolean |  | `true` | When enabled, each person's public LinkedIn profile page is opened to add their about text, work history with job titles, education, connection and follower counts, photo and languages. Turn this off for a faster, cheap… |

### Example

Ask the agent in plain language, or call `johnvc--linkedin-people-search-api` with arguments such as:

```json
{
  "jobTitle": "CTO",
  "company": "Stripe",
  "maxResults": 10
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `resultType` | string: person, error | Row kind. 'person' is a matched person. 'error' reports a page that could not be read and is never charged. |
| `profileUrl` | string | Canonical public LinkedIn profile URL, with all tracking parameters removed. |
| `publicIdentifier` | string | The profile slug, which is the last path segment of the profile URL. Stable per person and useful as a deduplication key. |
| `fullName` | string | The person's name as shown on their public profile. |
| `headline` | string | The professional headline shown under the person's name, usually their role and employer. |
| `currentCompany` | string | Employer the person currently lists first on their profile. |
| `currentCompanyUrl` | string | LinkedIn company page for the current employer, when the profile links one. |
| `about` | string | The person's public About/summary text. Present only when the profile was opened for enrichment. |
| `locationLocality` | string | City or metropolitan area from the public profile. |
| `locationCountry` | string | Two-letter country code from the public profile. |
| `profilePhotoUrl` | string | Public profile photo. Absent when the person has no public photo. |
| `followerCount` | integer | Number of followers shown on the public profile. |
| `experience` | array | Positions listed on the public profile, most recent first. Each entry has organizationName, organizationUrl, organizationLocation, role, startDate and endDate where the profile shows them. |
| `education` | array | Schools listed on the public profile. Each entry has organizationName, organizationUrl, startDate and endDate where shown. |
| `languages` | array | Languages listed on the public profile. |
| `awards` | array | Honours and awards listed on the public profile. |
| `isEnriched` | boolean | True when the person's public profile page was opened and parsed. False when the row carries search-level data only, which happens when enrichment is off or the profile would not open. |
| `searchRank` | integer | Position of this person in the search results, starting at 1. |
| `searchQuery` | string | The exact public search query this run used, so every row can be traced back to what was asked. |
| `searchHeadline` | string | The headline text the search result showed, kept when the opened profile page has its own headline (which then fills headline). Absent on rows that were not enriched, where headline is the search text. |
| `currentTitle` | string | Job title at the current employer, from the public profile. Each experience entry also carries its own title when the profile shows one. |
| `connections` | integer | Connection count shown on the public profile. LinkedIn caps the display at 500, so 500 means 500 or more; see connectionsText. |
| `connectionsText` | string | The connection count as LinkedIn shows it, for example 500+. |
| `memberId` | string | LinkedIn's numeric member id for the profile, when the public page exposes it. Stable even if the profile URL changes. |
| `positions` | array | Every position in the profile's experience section, past roles included. Each entry has title, companyName, companyUrl, startDate, endDate, duration, location and isCurrent where the profile shows them. |
| `fromCache` | boolean | True when this row was served from the shared result cache instead of a new request: the opened profile for an enriched row, the search page otherwise. Billed like a fresh row. Search result pages are reused for up to 1… |
| `fetchedAt` | string | UTC time the row's data was fetched from LinkedIn's public pages (the profile page for an enriched row, the search page otherwise). For a cached row this is the original fetch time. |
| `errorType` | string | Short error class on error rows: 'SearchUnavailable' when the search could not be served (retry later). Absent on other error rows and on people. |
| `errorMessage` | string | Why a page could not be read. Only present on rows where resultType is 'error'. |

## Data source and terms

Public LinkedIn profiles found through web search and read from their public pages, collected by scraping. No login or cookies are used. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/linkedin-people-search-api
- Docs page: https://alphaosint.com/mcp/linkedin-people-search/
- All AlphaOSINT MCP servers: [index](../../README.md)
