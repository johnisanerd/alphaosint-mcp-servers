# LinkedIn Learning MCP server

Registry name: `io.github.johnisanerd/linkedin-learning`. Maintained by AlphaOSINT (Apify developer `johnvc`, GitHub `johnisanerd`).

## What it does

Search LinkedIn Learning courses by keyword, level, length or software and get full course records with rating, review text, syllabus, instructors, skills and certificates.

## When to use it

Course catalog data for training and upskilling. Use it for learning-path recommendations, course comparison and skills research.

## How it works

The server runs on Apify's hosted MCP endpoint, so there is nothing to install or host. Its URL pins one Actor with `?tools=johnvc/linkedin-learning-api`, which gives your agent a single tool, `johnvc--linkedin-learning-api`, whose parameters are the Actor's typed input schema. The agent can call that tool directly without searching for an Actor first, and it can't start other Actors through this server. For general access to the whole Apify Store, use `https://mcp.apify.com` without the `tools` parameter.

## Pricing

Each tool call runs the Apify Actor `johnvc/linkedin-learning-api` on your own Apify account and is billed there at the Actor's prices:

| Charge | Price (USD) | What it covers |
|---|---|---|
| Course found | $0.00001 | Charged once for each course returned by a search or topic page, with its title, instructors, length, level, thumbnail and link. Not charged for duplicates, for the popular-courses list LinkedIn shows when a query match… |
| Full course record | $0.00001 | Charged once for each full course record returned: rating, learner reviews, the complete syllabus with per-lesson descriptions, free-lesson flags, instructors, skills and certificate details. Replaces the search charge… |

Free-plan rates as of 2026-11-12; paid Apify plans pay less per event. Apify also bills a token amount per run start and stored row ($0.00001, $0.00001). Current prices are on the Actor's page: https://apify.com/johnvc/linkedin-learning-api

## Endpoint

- Transport: Streamable HTTP
- URL: `https://mcp.apify.com/?tools=johnvc/linkedin-learning-api`
- Auth: Apify OAuth (opens on first use), or the header `Authorization: Bearer <APIFY_TOKEN>` (Apify Console → Settings → API & Integrations)

## Setup

**Claude Code**

```bash
claude mcp add --transport http linkedin-learning "https://mcp.apify.com/?tools=johnvc/linkedin-learning-api"
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "linkedin-learning": {
      "type": "http",
      "url": "https://mcp.apify.com/?tools=johnvc/linkedin-learning-api"
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "linkedin-learning": {
      "url": "https://mcp.apify.com/?tools=johnvc/linkedin-learning-api"
    }
  }
}
```

**Claude Desktop**: Settings → Connectors → Add custom connector, and paste the URL. Older versions without remote connectors can bridge through `mcp-remote` in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "linkedin-learning": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=johnvc/linkedin-learning-api"
      ]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `johnvc--linkedin-learning-api` | Runs the Actor with the parameters below and returns the result rows. |
| `get-actor-run` | Status of a run the tool started (for long runs). |
| `get-dataset-items` | Pages through a run's full output when it is larger than the inline result. |
| `get-key-value-store-record` | Reads a record a run stored. |
| `abort-actor-run` | Stops a run. |

Apify's endpoint adds the four helper tools whenever an Actor tool is loaded.

### Parameters of `johnvc--linkedin-learning-api`

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `mode` | string: search, details | yes | `"search"` | Choose what to collect. Use 'search' to find courses by keyword with filters, or 'details' to pull the full record for course URLs you already have (ratings, reviews, syllabus, instructors, certificate). |
| `queries` | array |  | `["python"]` | Keywords to search, one per line. Each query is searched separately and its results are labelled with the query that found them. Used in 'search' mode only. Leave empty if you are browsing topic pages instead. |
| `topics` | array |  | `[]` | Optional LinkedIn Learning topic slugs or topic URLs to browse, such as 'python' or https://www.linkedin.com/learning/topics/python. Topic pages are an alternative to keyword search and return the same course fields. |
| `sortBy` | string: RELEVANCE, POPULARITY, RECENCY |  | `"RELEVANCE"` | Order the search results. 'Most relevant' is LinkedIn's default ranking, 'Most popular' favours high view counts, and 'Newest' favours recent release dates. |
| `difficultyLevel` | string: ANY, BEGINNER, INTERMEDIATE, ADVANCED |  | `"ANY"` | Keep only courses at one skill level. Leave as 'Any level' to include all of them. |
| `entityType` | string: ANY, COURSE, VIDEO, LEARNING_PATH |  | `"ANY"` | Keep only one kind of content. Courses are full multi-lesson courses, videos are single lessons, and learning paths are curated multi-course tracks. |
| `duration` | string: ANY, BETWEEN_0_TO_10_MIN, BETWEEN_10_TO_30_MIN, BETWEEN_30_TO_60_MIN, B… |  | `"ANY"` | Keep only courses that fall in one length bracket. |
| `softwareNames` | array |  | `[]` | Keep only courses that teach this tool, using LinkedIn's own label such as Python, Microsoft Excel, SQL, ChatGPT or Claude. The schema accepts up to 10, but LinkedIn applies only the first label it receives, so pass one… |
| `maxItems` | integer |  | `50` | How many courses to return for each query. LinkedIn serves at most 50 results per query and filter combination, so ask for more than 50 only with 'Widen coverage' turned on. Up to 1000 per query. Need larger batches? Co… |
| `expandWithFilters` | boolean |  | `false` | Run the same query again across LinkedIn's own filter combinations (sort order, content type, difficulty, length) and merge the unique courses. This is the only way past the 50-per-query ceiling. It fetches more pages a… |
| `enrichDetails` | boolean |  | `false` | Open each course found by the search and return its full record, including rating, review text, syllabus and instructors. Enriched rows are billed at the course details rate instead of the search result rate, never both… |
| `courseUrls` | array |  | `[]` | LinkedIn Learning course, lesson or learning path URLs to collect in full, one per line. A course URL returns the full course record, a lesson URL returns that lesson linked to its parent course, and a learning path URL… |
| `maxConcurrency` | integer |  | `5` | How many course pages to read at once, in both 'details' mode and when 'Include full course details' is on. Raise it to finish a large run faster, lower it if you ever see rate limiting. |
| `requestTimeoutSecs` | integer |  | `40` | How long to wait for a single page before giving up and retrying it. |

### Example

Ask the agent in plain language, or call `johnvc--linkedin-learning-api` with arguments such as:

```json
{
  "mode": "search",
  "queries": [
    "python"
  ],
  "courseUrls": [
    "https://www.linkedin.com/learning/python-essential-training-18764650"
  ]
}
```

### Output

JSON rows with these fields:

| Field | Type | Description |
|---|---|---|
| `resultType` | string: search_result, course_detail, lesson, learning_path… | Which kind of row this is: a search result, a full course record, a lesson, a learning path, a no-match notice, or an error for one input. |
| `title` | string | Course, lesson, or learning path title as published on LinkedIn Learning. |
| `courseUrl` | string | Canonical LinkedIn Learning course link with tracking parameters removed. |
| `courseId` | string | Identifier for the COURSE, taken from the trailing number in its URL, or the URL slug when a course has no number. A lesson row carries its parent course's id, so lessons can be joined to their course; use courseUrl or… |
| `sourceUrl` | string | The URL supplied as input or the page this row was read from. |
| `lessonUrl` | string | Direct link to a single lesson, when the row is a lesson. |
| `pathUrl` | string | Direct link to a learning path, when the row is a learning path. |
| `description` | string | Full course description as published on the course page. |
| `difficultyLevel` | string | Skill level LinkedIn assigns to the course. |
| `entityType` | string: COURSE, VIDEO, LEARNING PATH | Whether the search result is a course, a single video lesson, or a learning path. LinkedIn labels these COURSE, VIDEO and LEARNING PATH. |
| `instructors` | array | Everyone credited as an instructor. Search rows carry the name only; full course records add job title, LinkedIn profile link and photo. |
| `skills` | array | Skills and technologies the course covers, each linking to its LinkedIn Learning topic page. |
| `categoryPath` | array | Category hierarchy the course sits in, from broadest to narrowest. |
| `durationText` | string | Course length as published, in ISO 8601 form on detail rows and as displayed text on search rows. |
| `durationSeconds` | integer | Course length in whole seconds, parsed for sorting and filtering. |
| `enrollmentCount` | integer | How many people have taken the course to date. |
| `ratingValue` | number | Average learner rating out of 5. |
| `ratingCount` | integer | How many learners rated the course. |
| `reviews` | array | Written learner reviews with the rating, the review text, and the reviewer's name, job title and profile link. |
| `tableOfContents` | array | Full syllabus: every section with its lessons, each carrying a title, a written description, its length, and whether it can be watched free. |
| `lessonCount` | integer | How many lessons the course contains. |
| `freeLessonCount` | integer | How many lessons can be watched without a subscription. |
| `hasCertificate` | boolean | Whether the course awards a certificate of completion. |
| `certificateName` | string | Name of the credential awarded. |
| `accessModel` | string | How the course is made available. LinkedIn Learning courses are subscription based and carry no individual price. |
| `language` | string | Language the course is taught in. |
| `provider` | string | Organization publishing the course. |
| `dateCreated` | string | When the course was created. |
| `datePublished` | string | When the course was published. |
| `thumbnailUrl` | string | Course artwork image link. The query string is part of the signed image URL and is preserved. |
| `isFree` | boolean | Whether this lesson can be watched without a subscription. |
| `requiresSubscription` | boolean | Whether this lesson needs a LinkedIn Learning subscription. |
| `courses` | array | Courses that make up a learning path, in order. |
| `courseCount` | integer | How many courses the learning path contains. |
| `searchQuery` | string | The query or topic that returned this row. |
| `searchType` | string: query, topic | Whether the row came from a keyword search or a topic page. |
| `searchPosition` | integer | Rank this course held in the search results that found it, on enriched rows. |
| `position` | integer | Rank of this result within its search page, starting at 1. |
| `appliedFilters` | object | Which LinkedIn filters were in force for the request that surfaced this row. |
| `approximateTotalResults` | integer | How many courses LinkedIn reports for this query. Approximate: the same query can report different totals across page variants, so treat it as a size signal rather than an exact count. |
| `viewersText` | string | Viewer count as displayed on the search card. |
| `releaseText` | string | Release date as displayed on the search card. |
| `parseSource` | string: jsonld, dom | Whether the record was read from the page's structured data or from its markup. |
| `message` | string | Explanatory note, used on no-match rows. |
| `errorType` | string | Category of failure for an error row. |
| `errorMessage` | string | What went wrong, phrased for the person running the actor. |
| `httpStatus` | integer | Status code LinkedIn returned, when there was one. |
| `fetchedAt` | string | When this row was collected, in UTC. |
| `fromCache` | boolean | True when this course record was served from the shared result cache instead of a new page read; fetchedAt then holds the time it was originally read. Billed like a fresh record. Only full course records are cached; sea… |

## Data source and terms

LinkedIn Learning's public course pages, collected by scraping. No login or cookies are used. The server returns the data as published at the time of the call. You are responsible for using it in line with the source's terms and the laws that apply to you. AlphaOSINT is not affiliated with the source.

## Links

- Actor on Apify: https://apify.com/johnvc/linkedin-learning-api
- Docs page: https://alphaosint.com/mcp/linkedin-learning/
- All AlphaOSINT MCP servers: [index](../../README.md)
