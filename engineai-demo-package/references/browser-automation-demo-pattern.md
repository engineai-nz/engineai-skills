# Browser Automation Demo Pattern — CDS Worked Example

Built May 30, 2026 for the CDS Civil demo. Reusable for any client who has
"that website someone copy-pastes from" — which is every client.

## Architecture

```
Telegram: "GeoTech brief for Westgate Trunk Sewer"
  → Hermes Agent recognizes intent
  → MCP tool: cds_demo.cds_geotech_brief(project="Westgate Trunk Sewer")
  → MCP server (server.py) calls orchestrator
  → Orchestrator spawns 3x Playwright Chromium headless browsers IN PARALLEL:
      1. nzgd-scrape.mjs — NZ Geotechnical Database
      2. council-gis-scrape.mjs — Auckland Council GeoMaps
      3. supplier-scrape.mjs — Supplier pricing portals
  → Each script: navigate → extract DOM data → take retina screenshot → output JSON
  → Orchestrator compiles structured brief from all 3 results
  → Returns text + 3 PNG screenshots
  → Lands in Telegram in ~3-5 seconds
```

## File Layout

```
~/.hermes/demos/[client_slug]/
├── playwright-use-cases.md          # Use case document for the presentation
├── cds-demo-config.yaml             # Hermes config snippet to wire MCP server
├── playwright-scripts/
│   ├── package.json                 # npm project (playwright dependency)
│   ├── playwright-utils.mjs         # Shared: browser launch, mock URL, data extractors
│   ├── nzgd-scrape.mjs              # Scraper #1: borehole data + screenshot
│   ├── council-gis-scrape.mjs       # Scraper #2: GIS layers + hazards + screenshot
│   ├── supplier-scrape.mjs          # Scraper #3: pricing rows + screenshot
│   ├── geotech-brief.mjs            # Orchestrator: runs all 3 in parallel, compiles brief
│   ├── nzgd-mock.html               # Synthetic NZGD page (looks real, no login needed)
│   ├── council-gis-mock.html        # Synthetic Council GIS page with layers overlay
│   ├── supplier-mock.html           # Synthetic supplier pricing portal
│   ├── output/                      # Screenshots land here
│   └── briefs/                      # Compiled briefs (JSON + markdown) land here
└── mcp-server/
    └── server.py                    # MCP server exposing tools to Hermes agent
```

## Key Technical Decisions

### Why mock HTML instead of mocking the network
The Playwright scripts navigate to real-looking synthetic HTML pages via `file://`
URL. This means:
- Screenshots look authentic (rendered by real Chromium with real CSS)
- Data extraction uses the same DOM selectors that would work on the real site
- Switching to live mode = change the URL and add login steps — scripts stay the same

### Why 3 separate scripts + orchestrator instead of one big script
- Each scraper can run independently for debugging
- `Promise.all()` runs them truly in parallel (3 browser processes simultaneously)
- Adding scraper #4 is a one-line addition to the orchestrator
- Each scraper has its own timeout — one failing doesn't block others

### Why retina screenshots (deviceScaleFactor=2)
The synthetic HTML pages are information-dense (maps, tables, layer panels). At 1x
they look fuzzy when zoomed. At 2x they're sharp enough to project on a screen
or include in a proposal.

## Timing

| Stage | Duration |
|---|---|
| 3 parallel Playwright sessions | 3.4-3.8s |
| Data extraction + compilation | < 100ms |
| Total demo pipeline | ~4s |

Compare to manual: 40-60 minutes per tender brief.

## Switching to Live Mode

When the client gives you credentials:
1. Add login/redirect steps to each scraper script
2. Change the URL in `getProductionUrl()` in playwright-utils.mjs
3. Set `PLAYWRIGHT_MODE=live`
4. Test against real portals

The mock/live split means you can develop and demo without client credentials,
then flip the switch when they hand them over.

## Pitfalls

- **Playwright npm install:** The module is not in global node_modules. Always
  `npm install playwright` locally in the scripts directory before running.
- **MCP SDK API churn:** The `mcp` Python package changed between v0.4 and v0.5.
  `server.run()` now takes `(read_stream, write_stream, InitializationOptions)`.
  The old `server.run(stdio_server())` pattern broke. Pin the SDK or use the
  boilerplate in Step 2.5 of the demo skill.
- **JSON parsing from subprocess stdout:** The orchestrator outputs log lines
  before JSON. Using `OUTPUT_MODE=json` (env var) makes it output clean JSON only.
  The MCP server always calls with this flag set.
- **Screenshot path stability:** Each run generates new timestamped files. Old
  screenshots accumulate in `output/`. Clean before a demo or after.
- **Not all MCP server return types accept ImageContent:** Some Hermes MCP
  transport layers only handle TextContent. The CDS MCP server is tested against
  the native stdio transport which handles both.