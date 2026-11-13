# Yandex Reverse Image Search MCP server

Registry name: `io.github.johnisanerd/yandex-reverse-image-search`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Search Yandex by image URL and get the pages where the image appears, visually similar images, other sizes, matching shop products and image tags.

## When to use it

Searches by image rather than by text. Use it for image provenance, copyright checks, product matching and OSINT investigations.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/yandex-reverse-image-search`, which gives your agent a single tool, `johnvc--yandex-reverse-image-search`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/yandex-reverse-image-search` on your own Apify account and is billed there at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Result returned | $0.0065 | One reverse image result row: a page where the image appears, a similar image, an alternate size, an image tag, a shopping match, or a knowledge graph card. |

Free-plan rates as of 2026-11-13; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00001, $0.00001). Current prices are on the Actor's page: https://apify.com/johnvc/yandex-reverse-image-search

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/yandex-reverse-image-search`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http yandex-reverse-image-search "https://mcp.apify.com/?tools=johnvc/yandex-reverse-image-search"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "yandex-reverse-image-search": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/yandex-reverse-image-search"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "yandex-reverse-image-search": {
      "url": "https://mcp.apify.com/?tools=johnvc/yandex-reverse-image-search"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "yandex-reverse-image-search": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/yandex-reverse-image-search"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--yandex-reverse-image-search` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--yandex-reverse-image-search`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `image_url` | string | yes | `"https://substack-post-media.s3.amazonaws.com/public/images…` | Provide the public http(s) URL of the image to search by. Yandex fetches this URL, so it must be reachable from the internet (no localhost or private links). Example: `https://substack-post-media.s3.amazonaws.com/public… |
| `crop` | string |  |  | Optionally crop the image before searching, as four ';'-separated fractions between 0 and 1 in the order left;top;right;bottom. Example: `0.1;0.2;0.9;0.8` searches only the middle of the image. Leave blank to search the… |
| `include_matching_pages` | boolean |  | `true` | Return pages where this image (or a close match) appears online, with page title, link, and snippet. Rows with result_type 'matching_page'. On by default. |
| `include_similar_images` | boolean |  | `true` | Return visually similar images from across the web. Each row carries a thumbnail, the full-size image URL, and the site hosting it. Yandex returns no page title or snippet for this result type, so those columns stay emp… |
| `include_image_sizes` | boolean |  | `false` | Return other resolutions of the same image, categorized large / medium / small. Rows with result_type 'image_size'. Off by default. |
| `include_image_tags` | boolean |  | `false` | Return suggested search terms describing what is in the image. Rows with result_type 'image_tag'. Off by default. |
| `include_shopping_results` | boolean |  | `false` | Return e-commerce products that match the image content, with prices where available. Yandex only fills this section for a minority of images, so many searches return no product rows at all. Rows with result_type 'shopp… |
| `include_knowledge_graph` | boolean |  | `false` | Return the entity card when the image contains a recognizable subject (a person, landmark, product, or brand). One row with result_type 'knowledge_graph'. Off by default. |
| `yandex_domain` | string: yandex.com, yandex.ru, yandex.by, yandex.kz, yandex.uz, yandex.com.tr |  | `"yandex.com"` | The regional Yandex domain to search from. Defaults to 'yandex.com'. Results can differ by region. |
| `max_results` | integer |  | `50` | Cap the total number of result rows returned by this run. Results are sold in blocks of 10: the minimum is 10, and any other value rounds up to the next multiple of 10 (15 becomes 20). Every search bills at least one bl… |

### Example

Ask the agent in plain language, or call `johnvc--yandex-reverse-image-search` with arguments such as:

```json
{
  "image_url": "https://substack-post-media.s3.amazonaws.com/public/images/edbfb2cd-ebcb-4527-bec7-5315c182278f_445x445.png",
  "max_results": 50
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `result_type` | string: matching_page, similar_image, image_size, image_tag… | Discriminator for the row kind: 'matching_page' (a page where the image appears), 'similar_image', 'image_size' (another resolution of the same image), 'image_tag' (descriptive search term), 'shopping_result', 'knowledg… |
| `position` | integer | 1-based rank of this result within its result type. |
| `title` | string | Title of the page, image, product, or entity. Populated for 'matching_page', 'image_tag', 'shopping_result' and 'knowledge_graph' rows. Yandex returns no title for 'similar_image' or 'image_size' rows, so it is empty th… |
| `link` | string | URL of the page, image, or product this row points at. |
| `thumbnail` | string | Thumbnail image URL for this result. |
| `original` | string | Full-size image URL when the result carries one. Populated for 'matching_page' rows, and for 'similar_image' and 'image_size' rows where it is read back from the result link. |
| `source` | string | Source site or platform name for this result. Populated for 'matching_page' rows from the page's own site name, and derived from the image host for 'similar_image' and 'image_size' rows. |
| `source_link` | string | URL of the source site when the source was returned as an object. |
| `snippet` | string | Text snippet from the page where the image appears. Populated for 'matching_page' rows only. Yandex returns no snippet for any other result type. |
| `thumbnail_width` | integer | Width in pixels of the thumbnail image, when Yandex reports it. |
| `thumbnail_height` | integer | Height in pixels of the thumbnail image, when Yandex reports it. |
| `original_width` | integer | Width in pixels of the full-size image, when Yandex reports it. Useful for picking the highest-resolution copy of an image. |
| `original_height` | integer | Height in pixels of the full-size image, when Yandex reports it. |
| `description` | string | For 'knowledge_graph' rows: the entity blurb Yandex returns for a recognizable subject. |
| `text` | string | For 'image_tag' rows: the suggested search term describing the image. Also copied into 'title'. |
| `size` | string | For 'image_size' rows: the pixel dimensions of this alternate resolution, as reported by Yandex. |
| `size_category` | string | For 'image_size' rows: which size bucket this resolution belongs to (large, medium, or small). |
| `image_url` | string | The input image URL this reverse search was run for. |
| `yandex_domain` | string | The regional Yandex domain the search ran on. |
| `crop` | string | The crop box applied before searching, if any (left;top;right;bottom fractions). |
| `search_timestamp` | string | ISO 8601 timestamp of when the search was executed. |
| `error_message` | string | For 'error' rows: a human-readable explanation of what went wrong. |

## Data source and terms

Yandex's public reverse image search results, collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/yandex-reverse-image-search
- Docs page: https://alphaosint.com/mcp/yandex-reverse-image-search/
- All AlphaOSINT MCP servers: [index](../../README.md)
