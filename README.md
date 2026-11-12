# AlphaOSINT MCP servers

Remote MCP servers published in the [official MCP Registry](https://registry.modelcontextprotocol.io) under `io.github.johnisanerd/*`. Each one wraps a single Apify Actor maintained by AlphaOSINT (Apify developer `johnvc`) and does one job: job listings, flight fares, company funding, YouTube transcripts and so on.

**Hosted and paid.** These servers are not self-hosted. Every server runs on Apify's hosted MCP endpoint (`mcp.apify.com`), and each tool call is billed to the user's own Apify account at that Actor's prices. Each server's README lists the prices.

**How they differ from Apify's shared endpoint.** `https://mcp.apify.com` on its own gives an agent general tools for searching and running any Actor. Each server here pins one Actor in its URL (`?tools=johnvc/<actor>`), so the agent sees one tool whose parameters are that Actor's typed input schema, with no search step.

Each folder under [`servers/`](servers/) has the server's README: its tools and parameters, an example call, output fields, setup for Claude Code, VS Code, Cursor and Claude Desktop, and how it differs from the other servers. The registry entry for each server points at its folder.

## Servers

<!-- servers:start -->
| Server | Registry name | What it does |
|---|---|---|
| [Google Jobs](servers/google-jobs/) | `io.github.johnisanerd/google-jobs` | Search job postings by keyword and location across Google's 184 country domains and get structured rows with title, company, location, posting age, application links and the full description. |
| [Google Flights](servers/google-flights/) | `io.github.johnisanerd/google-flights` | Search one-way, round-trip and multi-city itineraries and get prices, airlines, stops, layovers, durations and optional booking options as JSON. |
| [Google Hotels](servers/google-hotels/) | `io.github.johnisanerd/google-hotels` | Search hotels and vacation rentals for a place and dates and get nightly prices, ratings, amenities, property details, and optionally reviews and photos. |
| [Google Local](servers/google-local/) | `io.github.johnisanerd/google-local` | Search local businesses for a query and place and get name, rating, review count, phone, hours, address, place ID and coordinates. |
| [Google Scholar](servers/google-scholar/) | `io.github.johnisanerd/google-scholar` | Search papers, get citation formats (MLA, APA, Chicago, BibTeX), author profiles with h-index and i10-index, an author's publications, per-article citation history and co-author networks. |
| [Google Shopping](servers/google-shopping/) | `io.github.johnisanerd/google-shopping` | Search products and get listings with price, seller, rating, delivery information and discount tags, with filters for location, price range, sort order, free shipping and sale items. |
| [Google AI Overview](servers/google-ai-overview/) | `io.github.johnisanerd/google-ai-overview` | Fetch the AI Overview Google shows for one or many queries, with the generated answer text and its cited sources, for a chosen country and language. |
| [Baidu Search](servers/baidu-search/) | `io.github.johnisanerd/baidu-search` | Run Baidu web searches with device, location and time filters and get organic results and related search features as structured rows, paginated. |
| [DuckDuckGo Search](servers/duckduckgo/) | `io.github.johnisanerd/duckduckgo` | Run DuckDuckGo searches with region, safe-search and date filters and get organic results, ads, knowledge graph, news, images, videos and related searches. |
| [Fuel Prices](servers/fuel-prices/) | `io.github.johnisanerd/fuel-prices` | Look up current gas and diesel prices at US stations by ZIP code, city or GPS coordinates and get station name, address, distance, cash and credit prices across six grades, and posted times. |
| [LinkedIn Learning](servers/linkedin-learning/) | `io.github.johnisanerd/linkedin-learning` | Search LinkedIn Learning courses by keyword, level, length or software and get full course records with rating, review text, syllabus, instructors, skills and certificates. |
| [Startup Investors](servers/startup-investors/) | `io.github.johnisanerd/startup-investors` | Search investment firms by type, stage, sector and location and get firm profiles, with optional partner contacts. |
| [US Congress Stock Trades](servers/us-congress-trades/) | `io.github.johnisanerd/us-congress-trades` | Search reported stock transactions by member, ticker, report date or date range and get the transaction, asset, amount range and filing details. |
| [YouTube Shorts](servers/youtube-shorts/) | `io.github.johnisanerd/youtube-shorts` | List the Shorts on a channel (or fetch given Short links) with views, likes, comments, publish time, duration, hashtags and channel statistics, sorted and filtered by date. |
| [YouTube Transcripts](servers/youtube-transcripts/) | `io.github.johnisanerd/youtube-transcripts` | Get the transcript of one or many YouTube videos or Shorts, with timestamps and language selection, plus optional video metadata. |
| [Crunchbase Company](servers/crunchbase-company/) | `io.github.johnisanerd/crunchbase-company` | Look up companies by Crunchbase organization URL and get funding rounds and totals, investors, industries, headquarters, employee count, rank and operating status. |
| [LinkedIn People Search](servers/linkedin-people-search/) | `io.github.johnisanerd/linkedin-people-search` | Find people by name, job title, employer, school or location and get profile URL, headline, current employer, location, and optionally about text, work history and education. |
| [Workday Careers](servers/workday-careers/) | `io.github.johnisanerd/workday-careers` | List every job on a company's Workday careers site with title, location, posted date, full description, pay range when published, employment type, remote status and apply link. |
<!-- servers:end -->

## Maintenance

The READMEs are generated by `scripts/build_readmes.py` from the server list in AlphaOSINT's website repository and each Actor's public input schema, dataset schema and prices on the Apify API. Regenerate after an Actor's schema or price changes:

```bash
uv run --with pyyaml python scripts/build_readmes.py <path to website-alphaosint>/_data/mcp_servers.yml
```

Docs pages with the same content: https://alphaosint.com/mcp/

## License

MIT
