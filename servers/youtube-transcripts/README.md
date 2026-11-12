# YouTube Transcripts MCP server

Registry name: `io.github.johnisanerd/youtube-transcripts`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Get the transcript of one or many YouTube videos or Shorts, with timestamps and language selection, plus optional video metadata.

## When to use it

Video text for summarizing, searching and quoting videos. Use it to give an agent the content of a video rather than its statistics.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/YoutubeTranscripts`, which gives your agent a single tool, `johnvc--YoutubeTranscripts`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/YoutubeTranscripts` on your own Apify account and is billed there at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Video Processed | $0.00275 | Charged per YouTube video successfully transcribed. Includes the timestamped and plain-text transcript plus basic video metadata (title, channel, views, duration, thumbnail). Failed videos, videos without captions, and… |
| Extended video metadata | $0.003 | Charged only when include_extended_metadata is true and the extra lookup succeeds (adds like count, upload date, categories and availability). Basic metadata is included free with every transcript. Failures are not char… |

Free-plan rates as of 2026-11-12; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00001, $0.00001). Current prices are on the Actor's page: https://apify.com/johnvc/YoutubeTranscripts

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/YoutubeTranscripts`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http youtube-transcripts "https://mcp.apify.com/?tools=johnvc/YoutubeTranscripts"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "youtube-transcripts": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/YoutubeTranscripts"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "youtube-transcripts": {
      "url": "https://mcp.apify.com/?tools=johnvc/YoutubeTranscripts"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "youtube-transcripts": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/YoutubeTranscripts"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--YoutubeTranscripts` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--YoutubeTranscripts`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `youtube_url` | string or array |  | `"https://www.youtube.com/watch?v=1UL8iZJD38U"` | Required unless 'channel' is provided. Provide one YouTube URL as a string, or multiple as an array (max 100 URLs per run). Works with standard videos, Shorts, youtu.be short links, embed URLs, and m.youtube.com mobile… |
| `languages` | array |  | `["en"]` | Ordered list of ISO 639-1 language codes. The first available transcript matching one of these languages is returned. Example: ["en", "es", "fr"] tries English first, then Spanish, then French. Defaults to ["en"] when o… |
| `translate_to` | string |  |  | Optional. If set to an ISO 639-1 code (e.g. "es", "fr", "de"), the picked transcript is translated to this language. Requires the source transcript to be translatable - run with list_only=true first to see translation_l… |
| `transcript_type` | string: any, manual, generated |  | `"any"` | Filter which transcript variant to consider when both manually-created and auto-generated captions exist for a language. "any" picks whichever matches the language priority first; "manual" only considers human-made capt… |
| `output_formats` | array |  | `[]` | Optional list of extra output formats to include in the dataset alongside the default structured fields. Allowed values: "srt" (SubRip subtitles), "vtt" (WebVTT subtitles), "text" (plain text, newline-separated). Unknow… |
| `preserve_formatting` | boolean |  | `false` | If true, keep YouTube's inline HTML formatting tags (<i>, <b>) in transcript text. Default false (strips them for clean text). |
| `list_only` | boolean |  | `false` | If true, do NOT fetch any transcript. Instead, for each URL return the list of all available transcripts with their language code, generated/manual status, is_translatable flag, and translation_languages. Useful for dis… |
| `include_metadata` | boolean |  | `true` | If true, attach video metadata from the same YouTube response that carries the captions: title, description, channel_name, channel_id, channel_url, view_count, video_duration_seconds, thumbnail_url, tags, was_live. No e… |
| `include_extended_metadata` | boolean |  | `false` | If true, run a second lookup per video for the fields the caption response does not carry: like_count, upload_date, categories, availability. Adds about 1-3 seconds per video and is charged as a videometadata event when… |
| `channel` | string or array |  |  | Optional. One YouTube channel as a string, or multiple as an array. Accepts an @handle ("@mkbhd"), a bare handle ("mkbhd"), a channel ID ("UCBJycsmduvYEL83R_U4JriQ"), or any channel URL (/channel/, /c/, /user/, /@handle… |
| `max_videos` | integer |  | `100` | Maximum number of videos to list per channel, newest first. Default 100. Values above 1000 are capped at 1000 (and values below 1 are raised to 1) with a log warning rather than failing the run. When channel_transcripts… |
| `channel_transcripts` | boolean |  | `false` | If true, every video listed from the channel(s) is also queued for transcript extraction (newest first, deduplicated against youtube_url entries, subject to the 100 videos per run limit). Each successful transcript is c… |

### Example

Ask the agent in plain language, or call `johnvc--YoutubeTranscripts` with arguments such as:

```json
{
  "youtube_url": "https://www.youtube.com/watch?v=1UL8iZJD38U",
  "languages": [
    "en"
  ],
  "output_formats": []
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `url` | string | The original YouTube video URL that was processed. |
| `video_id` | string | The YouTube video ID (11 characters). |
| `language` | string | The transcript language name (e.g., 'English', 'English (auto-generated)'). |
| `language_code` | string | The ISO language code of the transcript (e.g., 'en', 'es', 'fr'). |
| `is_generated` | boolean | True if the transcript was auto-generated by YouTube, false if manually created. |
| `is_translatable` | boolean | Whether the transcript can be translated to other languages. May be null if not available. |
| `translation_languages` | array | List of language codes this transcript can be translated to. May be null if not available. |
| `total_seconds` | number | Total duration of the video in seconds, derived from the last transcript snippet. |
| `timestamped` | array | Array of transcript snippets with timestamps. Each snippet has text, start (seconds), and duration (seconds). |
| `non_timestamped` | string | Full transcript text without timestamps: all snippets concatenated. Use this for LLM input or readable export. |
| `timestamp` | string | ISO-format timestamp of when the video was processed. |
| `success` | boolean | True if the video was successfully transcribed, false if processing failed. |
| `cached` | boolean | True if this transcript came from the cache instead of a fresh fetch from YouTube. See fetched_at for its age; cached copies are at most 90 days old. Also present on the error row of a video with no usable captions: tru… |
| `fetched_at` | string | ISO-format UTC timestamp of when the transcript was fetched from YouTube. Equal to the run time for fresh rows; earlier for cached rows. On the error row of a video with no usable captions, it is when YouTube was last c… |
| `cache_age_days` | integer | Whole days between fetched_at and this run. Present only on cached rows. |
| `error` | boolean | True if an error occurred during processing; absent or false on success. |
| `error_message` | string | Human-readable description of the error, if any. |
| `error_type` | string | Type/class name of the error (e.g., 'ValueError', 'ValidationError', 'RequestBlocked'). A video with no usable captions reports 'NoTranscriptFound' (captions exist, but not in the requested languages or type; available_… |
| `is_permanent_error` | boolean | Present on the error row of a video whose transcript could not be fetched. True when asking again for the same video and languages cannot help: no usable captions, captions disabled, or the video is unavailable or age-r… |
| `is_blocking_error` | boolean | Present on the error row of a video whose transcript could not be fetched. True when YouTube refused the request itself, which is temporary: the same video may succeed in a later run. Always false when is_permanent_erro… |
| `retry_attempts` | integer | Present on the error row of a video that ended in a permanent or a blocking error: how many fetch attempts were made before the row was written. 0 when a 'no captions' answer came from the cache. |
| `translated_to` | string | ISO 639-1 language code the transcript was translated into. Only present when the translate_to input was set and translation succeeded. |
| `srt` | string | Transcript formatted as a SubRip (.srt) file. Present when 'srt' is included in output_formats. |
| `vtt` | string | Transcript formatted as a WebVTT (.vtt) file. Present when 'vtt' is included in output_formats. |
| `text` | string | Transcript as plain text, snippets joined with newlines (TextFormatter output). Present when 'text' is included in output_formats. |
| `list_only` | boolean | True if this dataset item was produced by a list_only=true run. The available_transcripts field will be populated and no transcript was actually fetched. |
| `available_transcripts` | array | Only present in list_only mode. Each entry describes one transcript variant YouTube exposes for this video: language, language_code, is_generated, is_translatable, translation_languages. One exception: the error row of… |
| `source_type` | string | Human-readable mirror of is_generated. "Manual" for human-created captions, "Auto-generated" for YouTube ASR (and for any translated transcript, since YouTube serves translations through the auto-gen pipeline). |
| `snippet_count` | integer | Number of timestamped snippets in the transcript (equal to len(timestamped)). |
| `duration_human` | string | Total duration formatted as a short human-readable string, e.g. "1h 19m 42s", "2m 7s", or "18s". See total_seconds for the raw float value. |
| `channel_name` | string | Name of the YouTube channel that uploaded the video. Populated when include_metadata is true. |
| `channel_id` | string | Stable YouTube channel ID (e.g., UC4QobU6STFB0P71PMvOGN5A). |
| `channel_url` | string | Direct URL to the YouTube channel. |
| `view_count` | integer | Total view count at the moment metadata was extracted. |
| `like_count` | integer | Total like count at the moment metadata was extracted. YouTube hides this for some videos; field is omitted when unavailable. |
| `video_duration_seconds` | integer | Video duration as reported by YouTube's player. Distinct from total_seconds (which is derived from the last transcript snippet); the two can differ slightly. |
| `upload_date` | string | Date the video was uploaded, formatted as ISO YYYY-MM-DD. |
| `thumbnail_url` | string | URL to YouTube's default thumbnail for the video. |
| `tags` | array | Tags the uploader assigned to the video. |
| `categories` | array | YouTube category labels for the video (e.g. "Film & Animation"). |
| `availability` | string | YouTube availability status, typically one of "public", "unlisted", "private", "premium_only", "subscriber_only", "needs_auth", "public_listed_unlisted". |
| `was_live` | boolean | True if the video was originally a livestream (now a replay). |
| `metadata_error` | string | If include_metadata was requested but metadata extraction failed, this field carries the error reason. The transcript fields are still populated. |
| `metadata_source` | string | Where the metadata fields came from: innertube (free, from the same YouTube response that carries the captions) or yt-dlp (include_extended_metadata, adds like_count, upload_date, categories, availability). Absent when… |
| `translation_error` | string | Set when translate_to was requested but the translation could not be delivered (the language is not offered, or YouTube throttled the translated caption download). The item then carries the original-language transcript… |
| `result_type` | string | Set to "channel_video" on rows produced by channel listing (the 'channel' input). Absent on transcript rows. |
| `source_channel` | string | The channel reference (name, @handle, ID, or URL) from the input that produced this row. Present on channel_video rows and channel listing errors. |
| `position` | integer | 1-based position of the video within its channel listing, newest first. Present on channel_video rows. |

## Data source and terms

YouTube's public captions and subtitles, collected by scraping. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/YoutubeTranscripts
- Docs page: https://alphaosint.com/mcp/youtube-transcripts/
- All AlphaOSINT MCP servers: [index](../../README.md)
