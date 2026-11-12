# Google Hotels MCP server

Registry name: `io.github.johnisanerd/google-hotels`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Search hotels and vacation rentals for a place and dates and get nightly prices, ratings, amenities, property details, and optionally reviews and photos.

## When to use it

Lodging prices and availability for a destination and date range, which flight or maps tools don't return. Use it for travel agents, rate monitoring and market research.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/google-hotels-search-scraper`, which gives your agent a single tool, `johnvc--google-hotels-search-scraper`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/google-hotels-search-scraper` on your own Apify account and is billed there at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Setup | $0.02 | One-time setup fee per Actor run. We charge this to cover the cost of setting up the instance, provisioning memory, etc. |
| Page Processed | $0.02 | Fee per page of hotel search results processed. Returns hotel property listings with details, prices, ratings, and filters for that page. |
| Autocomplete Suggestion | $0.005 | Fee per autocomplete suggestion returned. Each suggestion includes the location or hotel name and, for hotels, a property token for chaining into details, photos, or reviews. |
| Photo Returned | $0.001 | Fee per hotel photo returned, including full-size and thumbnail URLs, gallery section, dimensions, and source. |
| Review Returned | $0.005 | Fee per guest review returned, including rating, review text, date, source platform, reviewer details, and the property's response. |

Free-plan rates as of 2026-11-12; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00001, $0.00005). Current prices are on the Actor's page: https://apify.com/johnvc/google-hotels-search-scraper

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/google-hotels-search-scraper`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http google-hotels "https://mcp.apify.com/?tools=johnvc/google-hotels-search-scraper"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "google-hotels": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/google-hotels-search-scraper"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "google-hotels": {
      "url": "https://mcp.apify.com/?tools=johnvc/google-hotels-search-scraper"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-hotels": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/google-hotels-search-scraper"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--google-hotels-search-scraper` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--google-hotels-search-scraper`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `search_type` | string: search, autocomplete, photos, reviews |  | `"search"` | Select what to fetch. 'search' (default) returns hotel search results for a query, or full property details when property_token is provided (stay dates optional - they default to tomorrow for one night). 'autocomplete'… |
| `q` | string |  | `"hotels in Paris"` | Hotel search query (e.g., 'hotels in Paris', 'Bali Resorts', 'vacation rentals in Miami'). REQUIRED for search (unless property_token is provided) and for autocomplete. For autocomplete, partial queries like 'hotels in… |
| `property_token` | string |  |  | Google Hotels property token for a single specific property - obtain this from the property_token field in a previous search or autocomplete result. REQUIRED for photos and reviews modes, and for property details in sea… |
| `gl` | string |  | `"us"` | Country code for localization (ISO 3166-1 alpha-2, e.g., 'us', 'fr', 'uk'). Optional. Defaults to 'us' if not specified. Applies to search, autocomplete, and reviews. |
| `hl` | string |  | `"en"` | Language code for localization (ISO 639-1, e.g., 'en', 'fr', 'es'). Optional. Defaults to 'en' if not specified. Applies to search, autocomplete, and reviews. |
| `currency` | string |  | `"USD"` | Currency code for prices (ISO 4217, e.g., 'USD', 'EUR', 'GBP'). Optional. Defaults based on country if not specified. Applies to search and autocomplete. |
| `check_in_date` | string |  | `"2026-11-27"` | Check-in date in YYYY-MM-DD format (e.g., '2026-12-13'). Required when searching by query (q) in search mode. Optional when fetching property details by property_token: defaults to tomorrow, and the effective date is ec… |
| `check_out_date` | string |  | `"2026-11-29"` | Check-out date in YYYY-MM-DD format (e.g., '2026-12-14'). Recommended when searching by query (q) in search mode. Must be after check_in_date. Optional when fetching property details by property_token: defaults to check… |
| `adults` | integer |  | `2` | Number of adult guests. Optional. Defaults to 2 if not specified. Search mode only. |
| `children` | integer |  | `0` | Number of child guests. Optional. Defaults to 0 if not specified. Search mode only. |
| `children_ages` | string |  |  | Comma-separated list of children ages as integers (e.g., '5,8,12'). Required if children > 0. Optional otherwise. Search mode only. |
| `min_price` | string |  | `"0.00"` | Minimum price filter in the specified currency. Optional. Must be a valid number (e.g., '50' or '99.99'). Default: '0.00' (no minimum). Search mode only. |
| `max_price` | string |  | `"0.00"` | Maximum price filter in the specified currency. Optional. Must be a valid number (e.g., '200' or '299.99'). Default: '0.00' (no maximum). Search mode only. |
| `stars` | string |  |  | Comma-separated list of star ratings to filter by (e.g., '3,4,5' for 3, 4, or 5 star hotels). Each value must be an integer between 1 and 5. Optional. Search mode only. |
| `amenities` | string |  |  | Comma-separated list of amenity IDs to filter by (integer IDs). Optional. See the Actor README for the full list of supported amenity IDs. Search mode only. |
| `hotel_class` | string |  |  | Comma-separated list of hotel star-class levels to filter by. Valid values: 2 (2-star), 3 (3-star), 4 (4-star), 5 (5-star). Value 1 is not supported. Example: '3,4,5' for mid-range and luxury hotels. Optional. Not compa… |
| `guest_rating` | string |  | `"0.0"` | Minimum guest rating filter (0.0 to 5.0). Optional. Must be a valid number (e.g., '4.0' or '4.5'). Default: '0.0' (no minimum). Search mode only. |
| `property_type` | string |  |  | Comma-separated list of property type IDs to filter by (integer IDs). Optional. See the Actor README for the full list of supported property type IDs. Search mode only. |
| `vacation_rentals` | boolean |  | `false` | Whether to include vacation rentals in search results. Optional. Defaults to false. Search mode only. |
| `rental_type` | string |  |  | Comma-separated list of rental type IDs to filter by (integer IDs). Only relevant when vacation_rentals is true. Optional. Search mode only. |
| `bedrooms` | integer |  |  | Number of bedrooms filter for vacation rentals. Only relevant when vacation_rentals is true. Optional. Search mode only. |
| `bathrooms` | integer |  |  | Number of bathrooms filter for vacation rentals. Only relevant when vacation_rentals is true. Optional. Search mode only. |
| `reviews_sort_by` | string: 1, 2, 3, 4 |  |  | Sort order for reviews mode. '1' = most helpful (default), '2' = most recent, '3' = highest score, '4' = lowest score. Only used when Search Type is 'reviews'. Optional. |
| `reviews_category_token` | string |  |  | Token to filter reviews by a specific review category or topic (e.g., cleanliness, service). Obtain category tokens from the reviews breakdown of a property details result. Only used when Search Type is 'reviews'. Optio… |
| `max_pages` | integer |  | `1` | Maximum number of result pages to fetch (1-indexed). Set to 0 for no limit (fetch all available pages). Default: 1. Applies to search, photos, and reviews pagination; autocomplete always uses a single request. Results f… |
| `output_file` | string |  |  | Optional filename to save results as JSON. If not provided, will auto-generate based on query and timestamp. |

### Example

Ask the agent in plain language, or call `johnvc--google-hotels-search-scraper` with arguments such as:

```json
{
  "q": "hotels in Paris",
  "gl": "us",
  "hl": "en",
  "currency": "USD",
  "check_in_date": "2026-11-27",
  "check_out_date": "2026-11-29"
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `search_parameters` | object | The complete set of input parameters used for this search, echoed back in each result page for traceability. |
| `search_metadata` | object | Aggregate statistics about the search run - total results available, pages processed, and pagination status. |
| `search_timestamp` | string | ISO 8601 timestamp of when this search page was executed (e.g., '2026-12-13T10:30:00.123456'). |
| `page_number` | integer | 1-indexed page number this dataset item represents. Each page of results is pushed as a separate dataset item. |
| `ads` | array | Sponsored hotel listing advertisements returned on this page, typically from OTA booking platforms. |
| `filters` | array | Filter options available for narrowing down results. Only present on the first page of results. |
| `refine_by` | array | Additional refinement options surfaced by Google Hotels for the current query. Only present on the first page. |
| `property_details` | object | Full details for a single property. Only present when property_token is used as input instead of a search query. |
| `error` | boolean | True when this dataset item represents an error record rather than search results. |
| `error_message` | string | Human-readable description of the error that occurred, if error is true. |
| `error_type` | string | Machine-readable error category (e.g., 'InsufficientFunds', 'DataValidationError', 'SearchError'). |
| `timestamp` | string | ISO 8601 timestamp of when the error occurred. Only present on error records. |
| `search_type` | string | Which mode produced this item: 'search' (hotel search pages and property details), 'autocomplete' (one item per suggestion), 'photos' (one item per photo), or 'reviews' (one item per review). |
| `query` | string | The search query used for autocomplete suggestions. Only present on autocomplete items. |
| `position` | integer | 1-indexed position of this suggestion, photo, or review within the run's results. |
| `value` | string | The autocomplete suggestion text (e.g., a city, region, or hotel name). Only present on autocomplete items. |
| `suggestion_type` | string | Category of the autocomplete suggestion (e.g., a location or a specific hotel). Only present on autocomplete items. |
| `location` | string | Address or location context for the autocomplete suggestion, when available. Only present on autocomplete items. |
| `property_token` | string | Unique Google Hotels property identifier. On autocomplete items it identifies a suggested hotel (feed it back into photos, reviews, or property details). On photos and reviews items it echoes the requested property. |
| `suggestion` | object | Full autocomplete suggestion object including highlighted words and identifiers. Only present on autocomplete items. |
| `section_title` | string | Title of the photo gallery section this photo belongs to (e.g., 'At a glance', 'Rooms'). Only present on photos items. |
| `photo_url` | string | URL of the full-size photo. Only present on photos items. |
| `thumbnail_url` | string | URL of the photo thumbnail. Only present on photos items. |
| `photo` | object | Full photo object including dimensions, source, and posting date. Only present on photos items. |
| `rating` | number | Star rating given by the reviewer. Only present on reviews items. |
| `review_date` | string | Date the review was posted (relative or absolute, as reported by Google Hotels). Only present on reviews items. |
| `review_snippet` | string | Text of the guest review. Only present on reviews items. |
| `review_source` | string | Platform the review came from (e.g., Google, Tripadvisor). Only present on reviews items. |
| `user_name` | string | Display name of the reviewer. Only present on reviews items. |
| `review` | object | Full review object including subratings, hotel highlights, images, and the property's response. Only present on reviews items. |

## Data source and terms

Google Hotels public search results, collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/google-hotels-search-scraper
- Docs page: https://alphaosint.com/mcp/google-hotels/
- All AlphaOSINT MCP servers: [index](../../README.md)
