# YouTube Shorts MCP server

Registry name: `io.github.johnisanerd/youtube-shorts`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

List the Shorts on a channel (or fetch given Short links) with views, likes, comments, publish time, duration, hashtags and channel statistics, sorted and filtered by date.

## How it differs

Short-form video performance for a channel. Use it for creator analytics, trend research and competitor content tracking.

**From the other AlphaOSINT servers:** each server wraps exactly one Apify Actor and does one job; the [index](../../README.md) lists them side by side.

**From Apify's shared endpoint:** `https://mcp.apify.com` on its own exposes general tools (`search-actors`, `call-actor`) that let an agent look for and run any of thousands of Actors. This server's URL pins one Actor with `?tools=johnvc/youtube-shorts-api`, so the agent gets a single tool, `johnvc--youtube-shorts-api`, whose parameters are this Actor's typed input schema. There is no search or Actor-selection step, and the agent cannot start other Actors through it.

## Hosted on Apify, billed to your Apify account

This server is not self-hosted. It runs on Apify's hosted MCP endpoint (`mcp.apify.com`), which starts the Apify Actor `johnvc/youtube-shorts-api` for each tool call. You need an Apify account, and **every call is billed to that account** at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Short | $0.00001 | Charged per YouTube Short returned in the dataset (video metrics plus channel stats in one row). Error rows, empty channels and skipped items are not charged. |
| Date filter | $0.00001 | Small extra charge per returned Short, applied only when oldestPostDate is set. |

Free-plan rates as of 2026-11-12; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00001, $0.00001). Current prices are on the Actor's page: https://apify.com/johnvc/youtube-shorts-api

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/youtube-shorts-api`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http youtube-shorts "https://mcp.apify.com/?tools=johnvc/youtube-shorts-api"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "youtube-shorts": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/youtube-shorts-api"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "youtube-shorts": {
      "url": "https://mcp.apify.com/?tools=johnvc/youtube-shorts-api"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "youtube-shorts": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/youtube-shorts-api"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--youtube-shorts-api` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--youtube-shorts-api`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `channels` | array |  | `["siliconimist"]` | List YouTube channels to read Shorts from. Use the handle with or without @ (siliconimist, @MrBeast), a channel URL (https://www.youtube.com/@nasa), or a channel id (UC...). Each channel returns up to maxResultsShorts S… |
| `startUrls` | array |  |  | Paste individual YouTube Short or video links to fetch just those items (https://www.youtube.com/shorts/<id>, watch?v=<id>, or youtu.be/<id>). Optional; combine freely with channels. Up to 200 links per run. The date fi… |
| `maxResultsShorts` | integer |  | `10` | Limit the number of Shorts returned from each channel (1 to 500). Runs stop at 1,000 Shorts in total. |
| `sortChannelShortsBy` | string: NEWEST, POPULAR, OLDEST |  |  | Choose the order of a channel's Shorts tab: NEWEST (default), POPULAR, or OLDEST. Maps to the three sort buttons on the channel page. Ignored (forced to NEWEST) when oldestPostDate is set. |
| `oldestPostDate` | string |  |  | Return only Shorts published on or after this date. Use an absolute date (2025-06-03) or a relative span such as 7 days, 2 weeks, or 3 months. Setting it forces NEWEST order so the listing can stop at the first older Sh… |

### Example

Ask the agent in plain language, or call `johnvc--youtube-shorts-api` with arguments such as:

```json
{
  "channels": [
    "siliconimist"
  ],
  "maxResultsShorts": 10
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `title` | string | Title of the Short. |
| `translatedTitle` | string | Reserved for a translated title; null in this version. |
| `translatedText` | string | Reserved for a translated description; null in this version. |
| `type` | string: shorts, None | Content type, always shorts for a Short row. |
| `id` | string | YouTube video id of the Short. |
| `url` | string | Canonical Short URL. |
| `thumbnailUrl` | string | Largest available thumbnail image. |
| `viewCount` | integer | Exact view count at fetch time. |
| `date` | string | Publish timestamp in ISO 8601 UTC. Day precision (YYYY-MM-DD) only in the rare case YouTube withholds the exact time. |
| `likes` | integer | Exact like count at fetch time. |
| `location` | string | Location attached to the Short when the creator set one; usually null. |
| `channelName` | string | Display name of the channel that published the Short. |
| `channelUrl` | string | Canonical channel URL (channel id form). |
| `channelId` | string | YouTube channel id (UC...). |
| `collaborators` | array | Collaborating channels on the Short; empty when none. |
| `channelUsername` | string | Channel handle without the @ sign. |
| `channelDescription` | string | The channel's About text. |
| `channelJoinedDate` | string | Date the channel was created, as YouTube shows it. |
| `channelDescriptionLinks` | array | Links from the channel's About section as {text, url} objects. |
| `channelLocation` | string | Country the channel lists in its About section. |
| `channelAvatarUrl` | string | Channel profile image URL. |
| `channelBannerUrl` | string | Channel banner image URL. |
| `channelTotalVideos` | integer | Total videos on the channel. |
| `channelTotalViews` | integer | Total views across the channel. |
| `numberOfSubscribers` | integer | Subscriber count. Exact below 1,000, otherwise parsed from YouTube's rounded figure (15.1M = 15100000). |
| `isChannelVerified` | boolean | Whether the channel shows the verified badge. |
| `inputChannelUrl` | string | Normalized URL of the channel that was requested. |
| `isAgeRestricted` | boolean | Whether YouTube marks the Short as age-restricted. |
| `aboutChannelInfo` | object | All channel fields repeated in one object for convenience. |
| `duration` | string | Length as HH:MM:SS. |
| `commentsCount` | integer | Comment count. Exact below 1,000, otherwise parsed from YouTube's rounded figure (11K = 11000). Null when comments are turned off. |
| `text` | string | Full description text of the Short. |
| `descriptionLinks` | array | URLs found in the description as {url, text} objects. |
| `subtitles` | array | Reserved; null in this version. Use the YouTube Transcripts API for captions. |
| `order` | integer | Zero-based position of the Short in the returned list for its channel. |
| `commentsTurnedOff` | boolean | True when the creator disabled comments on the Short. |
| `fromYTUrl` | string | The YouTube page the Short was read from: the channel's Shorts tab, or the Short link itself for direct links. |
| `isMonetized` | boolean | Reserved; YouTube does not expose monetization publicly, so this is null. |
| `hashtags` | array | Hashtags found in the title and description, with the # sign. |
| `tags` | array | The creator's video keywords (the tags set in YouTube Studio), in the order YouTube returns them, without a # sign. Empty list when the creator set none. Not part of the drop-in contract; an extra key that existing pipe… |
| `isMembersOnly` | boolean | True when the Short is restricted to channel members. |
| `input` | string | The exact input value (channel or link) that produced this row. |
| `fromChannelListPage` | string | shorts when the row came from a channel's Shorts tab; null for direct links. |
| `error` | string | Present only on error rows: CHANNEL_DOES_NOT_EXIST, CHANNEL_HAS_NO_SHORTS, DATE_FILTER_TOO_STRICT, VIDEO_UNAVAILABLE, AGE_RESTRICTED, INVALID_INPUT, NO_RESULTS, YOUTUBE_BLOCKED, or INPUT_TRUNCATED. Error rows are never… |
| `note` | string | Human-readable explanation on error rows. |

## Data source and terms

YouTube's public channel and Shorts pages, collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/youtube-shorts-api
- Docs page: https://alphaosint.com/mcp/youtube-shorts/
- All AlphaOSINT MCP servers: [index](../../README.md)
