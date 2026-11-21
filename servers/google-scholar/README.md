# Google Scholar MCP server

Registry name: `io.github.johnisanerd/google-scholar`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Search papers, get citation formats (MLA, APA, Chicago, BibTeX), author profiles with h-index and i10-index, an author's publications, per-article citation history and co-author networks.

## When to use it

Academic literature and citation data in one server with six modes. Use it for research assistants, literature reviews and citation lookups.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/google-scholar-api`. The Actor is a multi-tenant Server Actor, so the endpoint gives your agent one tool, `johnvc--google-scholar-api`, that sends a single HTTP request to the Actor's server interface and returns the JSON response, usually within seconds. Each request handles one item and starts no run in your account. The agent can't start other Actors through this URL.

To also run the Actor in batch, with many items per run and the full input listed below, use `https://mcp.apify.com/?tools=call-actor,johnvc/google-scholar-api`. It adds Apify's `call-actor` tool, which can start any Actor your Apify account allows. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each request through `johnvc--google-scholar-api` is charged to your Apify account at the Actor's prices and starts no run. A batch run through `call-actor` runs the Actor `johnvc/google-scholar-api` on your account at the same prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Setup | $0.005 | One-time setup fee per Actor run. Covers instance setup and API provisioning costs. |
| Search API query executed | $0.015 | Fee per query executed against the upstream search API. Charged once per page on paginated modes (search, author_articles) and once per call on single-shot modes (cite, author_profile, author_citation, author_co_authors… |

Free-plan rates as of 2026-11-21; paid Apify plans pay less per event. Batch runs also bill a token amount per run start and stored row ($0.00001, $0.00001). Current prices are on the Actor's page: https://apify.com/johnvc/google-scholar-api

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/google-scholar-api` (the server tool only)
- URL with batch runs: `https://mcp.apify.com/?tools=call-actor,johnvc/google-scholar-api`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http google-scholar "https://mcp.apify.com/?tools=johnvc/google-scholar-api"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "google-scholar": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/google-scholar-api"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "google-scholar": {
      "url": "https://mcp.apify.com/?tools=johnvc/google-scholar-api"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-scholar": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/google-scholar-api"
      ]
    }
  }
}
```

For batch runs, put the URL with batch runs in the same places.

## Tools

| Tool | What it does |
|---|---|
| `johnvc--google-scholar-api` | Sends one HTTP request to the Actor's server interface (operations below) and returns the JSON response. Charged per event; starts no run. |

With the URL with batch runs, Apify also adds:

| Tool | What it does |
|---|---|
| `call-actor` | Runs the Actor (or another Actor) with an input such as the batch input below. |
| `get-actor-run` | Status of a run started by `call-actor`. |
| `get-dataset-items` | Reads a run's result rows. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

### Parameters of `johnvc--google-scholar-api`

The tool takes `method`, `path`, and optionally `query` (query parameters by name) and `body` (a JSON body, POST only). The Actor documents these operations:

| Method | Path | What it does |
|---|---|---|
| `GET` | `/search` | One Google Scholar lookup |
| `POST` | `/search` | One Google Scholar lookup, JSON body |

Query parameters of `GET /search`:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `mode` | string |  | Which Google Scholar operation to run. Each mode uses different required fields. Defaults to 'search'. |
| `q` | string |  | Free-text query for mode=search. Supports advanced operators like author:smith or source:nature. Required for mode=search unless 'cites' or 'cluster' is provided. |
| `cites` | string |  | For mode=search only. Article identifier used to look up papers that cite this article. Combine with 'q' to search within citing papers. Mutually exclusive with 'cluster'. |
| `cluster` | string |  | For mode=search only. Article cluster identifier used to fetch all versions of a paper. Mutually exclusive with 'q' and 'cites'. |
| `result_id` | string |  | For mode=cite only. The result_id (cluster id) of the Google Scholar paper to fetch citation formats for. Obtain from an organic_results entry of mode=search. |
| `author_id` | string |  | For mode=author_profile, author_articles, author_citation, and author_co_authors. The Google Scholar author identifier (e.g., 'LSsXyncAAAAJ'). Obtain from a publication_info.authors entry of mode=search or from a Google… |
| `citation_id` | string |  | For mode=author_citation only. The citation_id of the specific article in the author's profile (obtain from articles[].citation_id of mode=author_articles). |
| `hl` | string |  | Language for the user interface and result display. Applies to all modes. Optional. |
| `lr` | string |  | For mode=search only. Restrict results to specific languages. Use 'lang_xx' codes separated by '\|', e.g. 'lang_en' or 'lang_en\|lang_fr'. |
| `as_ylo` | integer |  | For mode=search only. Earliest publication year to include (e.g., 2010). |
| `as_yhi` | integer |  | For mode=search only. Latest publication year to include (e.g., 2024). |
| `scisbd` | string |  | For mode=search only. Recency sort: 0 = relevance (default), 1 = abstracts only from the last year sorted by date, 2 = everything from the last year sorted by date. |
| `as_sdt` | string |  | For mode=search only. Controls what types of results to include. Common values: '0' exclude patents (default), '7' include patents, '4' case law (US courts). |
| `safe` | string |  | For mode=search only. Safe search filter. Use 'active' to enable or 'off' to disable. |
| `filter` | string |  | For mode=search only. 1 = enable the similar/omitted-results filter (default), 0 = disable it. |
| `as_vis` | string |  | For mode=search only. 0 = include citations in results (default), 1 = exclude citations. |
| `as_rr` | string |  | For mode=search only. 1 = restrict to review articles, 0 = all article types (default). |
| `sort` | string |  | For mode=author_profile and author_articles. 'title' sorts alphabetically, 'pubdate' sorts by publication date (newest first). Omit for the default citation-count sort. |
| `max_pages` | integer |  | For mode=search and author_articles only. Pages to fetch, 1 to 3 over HTTP (default 1). For more, start a normal Actor run. |
| `num` | integer |  | For mode=search (1-20) and mode=author_articles (1-100). Page size for paginated modes. Defaults to 10 for search, 20 for author_articles. |


### Batch input (for `call-actor`)

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `mode` | string: search, cite, author_profile, author_articles, author_citation, author_… | yes | `"search"` | Which Google Scholar operation to run. Each mode uses different required fields. Defaults to 'search'. |
| `q` | string |  | `"machine learning"` | Free-text query for mode=search. Supports advanced operators like author:smith or source:nature. Required for mode=search unless 'cites' or 'cluster' is provided. |
| `cites` | string |  |  | For mode=search only. Article identifier used to look up papers that cite this article. Combine with 'q' to search within citing papers. Mutually exclusive with 'cluster'. |
| `cluster` | string |  |  | For mode=search only. Article cluster identifier used to fetch all versions of a paper. Mutually exclusive with 'q' and 'cites'. |
| `result_id` | string |  |  | For mode=cite only. The result_id (cluster id) of the Google Scholar paper to fetch citation formats for. Obtain from an organic_results entry of mode=search. |
| `author_id` | string |  |  | For mode=author_profile, author_articles, author_citation, and author_co_authors. The Google Scholar author identifier (e.g., 'LSsXyncAAAAJ'). Obtain from a publication_info.authors entry of mode=search or from a Google… |
| `citation_id` | string |  |  | For mode=author_citation only. The citation_id of the specific article in the author's profile (obtain from articles[].citation_id of mode=author_articles). |
| `hl` | string: en, es, fr, de, it, pt … |  | `"en"` | Language for the user interface and result display. Applies to all modes. Optional. |
| `lr` | string |  |  | For mode=search only. Restrict results to specific languages. Use 'lang_xx' codes separated by '\|', e.g. 'lang_en' or 'lang_en\|lang_fr'. |
| `as_ylo` | integer |  |  | For mode=search only. Earliest publication year to include (e.g., 2010). |
| `as_yhi` | integer |  |  | For mode=search only. Latest publication year to include (e.g., 2024). |
| `scisbd` | string: 0, 1, 2 |  | `"0"` | For mode=search only. Recency sort: 0 = relevance (default), 1 = abstracts only from the last year sorted by date, 2 = everything from the last year sorted by date. |
| `as_sdt` | string: 0, 7, 4 |  | `"0"` | For mode=search only. Controls what types of results to include. Common values: '0' exclude patents (default), '7' include patents, '4' case law (US courts). |
| `safe` | string: active, off |  |  | For mode=search only. Safe search filter. Use 'active' to enable or 'off' to disable. |
| `filter` | string: 0, 1 |  | `"1"` | For mode=search only. 1 = enable the similar/omitted-results filter (default), 0 = disable it. |
| `as_vis` | string: 0, 1 |  | `"0"` | For mode=search only. 0 = include citations in results (default), 1 = exclude citations. |
| `as_rr` | string: 0, 1 |  | `"0"` | For mode=search only. 1 = restrict to review articles, 0 = all article types (default). |
| `sort` | string: title, pubdate |  |  | For mode=author_profile and author_articles. 'title' sorts alphabetically, 'pubdate' sorts by publication date (newest first). Omit for the default citation-count sort. |
| `max_pages` | integer |  | `1` | For mode=search and author_articles only. Maximum number of result pages to fetch. Use 0 for no limit. Defaults to 1. |
| `num` | integer |  |  | For mode=search (1-20) and mode=author_articles (1-100). Page size for paginated modes. Defaults to 10 for search, 20 for author_articles. |

### Example

Ask the agent in plain language, or call `johnvc--google-scholar-api` with arguments such as:

```json
{
  "method": "GET",
  "path": "/search",
  "query": {
    "q": "machine learning"
  }
}
```

A batch run through `call-actor` takes the Actor and its input:

```json
{
  "actor": "johnvc/google-scholar-api",
  "input": {
    "mode": "search",
    "q": "machine learning"
  }
}
```

### Output

The server tool's JSON response carries result rows with these fields (batch runs write the same rows):

| Field | Type | Description |
|---|---|---|
| `_mode` | string | Mode |
| `_query_index` | integer | Page Number or Call Index |
| `search_parameters` | object | Search Parameters |
| `search_metadata_status` | string | API Response Status |
| `search_timestamp` | string | Search Timestamp |
| `position` | integer | Position On Page |
| `result_id` | string | Paper Result ID |
| `paper_title` | string | Paper Title |
| `link` | string | Paper URL |
| `snippet` | string | Snippet |
| `case_id` | string | Case ID |
| `publication_info` | object | Publication Info |
| `resources` | array | Resource Links |
| `inline_links` | object | Inline Links |
| `style` | string | Citation Style |
| `text` | string | Formatted Citation Text |
| `export_links` | array | Bibliography Export Links |
| `author` | object | Author |
| `cited_by_summary` | object | Citation Metrics |
| `cited_by_graph` | array | Citations Per Year |
| `public_access` | object | Public Access |
| `co_authors_preview` | array | Co-Authors Preview |
| `articles_preview` | array | Articles Preview |
| `article_position` | integer | Article Position |
| `citation_id` | string | Citation ID |
| `authors` | string | Authors String |
| `publication` | string | Publication Venue |
| `year` | string | Year |
| `cited_by_value` | integer | Cited By Count |
| `cited_by_link` | string | Cited By URL |
| `publication_date` | string | Publication Date |
| `journal` | string | Journal |
| `volume` | string | Volume |
| `issue` | string | Issue |
| `pages` | string | Pages |
| `publisher` | string | Publisher |
| `paper_description` | string | Description / Abstract |
| `total_citations_all` | integer | Total Citations |
| `total_citations_link` | string | Total Citations URL |
| `citation_by_year` | array | Citation By Year |
| `scholar_articles` | array | Related Scholar Articles |
| `coauthor_name` | string | Co-Author Name |
| `coauthor_link` | string | Co-Author Profile URL |
| `coauthor_author_id` | string | Co-Author ID |
| `coauthor_affiliations` | string | Co-Author Affiliations |
| `coauthor_email` | string | Co-Author Email Domain |
| `coauthor_thumbnail` | string | Co-Author Photo URL |
| `error` | boolean | Error Flag |
| `error_message` | string | Error Message |
| `error_type` | string | Error Type |

## Data source and terms

Google Scholar public pages, collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/google-scholar-api
- Docs page: https://alphaosint.com/mcp/google-scholar/
- All AlphaOSINT MCP servers: [index](../../README.md)
