# Scaffold Manifest — Hybrid Auto-Scaffold for a New Demo

This is the build manifest the skill follows to stamp a runnable client demo from the CDS template set. It is **hybrid auto-scaffold**: files 1–7 are generated deterministically from a small config object, and a handful of clearly-marked `// PER-CLIENT TODO` blocks are left for the agent to fill after inspecting the real site or mock HTML. It is neither full-auto (the bespoke DOM/section logic genuinely needs eyes on the page) nor guide-only (the skeleton, plumbing, and invariants are all stamped for you).

Read this alongside `browser-automation-demo-pattern.md` (the CDS worked example) and the `runbook-creator` skill (for the runbook emission step at the end).

---

## 0. The per-client config object (collect once, fills every placeholder)

The skill collects this during the interactive build interview (client name → research → personas → data map). Every placeholder `{{LIKE_THIS}}` in the skeletons below is filled from this object. Confirm it with the human before stamping.

```jsonc
{
  "client_slug": "cds",                        // dir + file prefix + RESULT sentinel root
  "client_name": "CDS New Zealand Ltd",
  "client_site": "https://www.cdsnz.co.nz",    // brand-scrape target (Pattern 5)
  "deliverable_noun": "GeoTech Brief",         // "Candidate Report", "Site Pack", ...
  "primary_entity_arg": "project",             // the one CLI arg every script takes
  "sources": [                                 // 1..N data sources, one scraper each
    { "id": "nzgd",     "label": "NZ Geotechnical Database", "mock_html": "nzgd-mock.html",      "key_selector": ".result-card", "extract": "cards->{id,depth,soil}" },
    { "id": "council",  "label": "Auckland Council GeoMaps", "mock_html": "council-gis-mock.html","key_selector": ".info-row",     "extract": "info-row->kv" },
    { "id": "supplier", "label": "Supplier Portal",          "mock_html": "supplier-mock.html",   "key_selector": "table tbody tr","extract": "table->rows" }
  ],
  "brand": { "primary": "#FF4000", "ink": "#1a1a1a", "muted": "#767676", "font": "Raleway", "logo": "assets/cds-logo.png" },
  "sender": "Joe Ward <joe@engineai.co.nz>",
  "default_recipients": ["joe@engineai.co.nz"], // SAFE default — NEVER the client until told
  "mcp_tools": ["brief", "email_report"],       // tool names become {{slug}}_{{tool}}

  // --- PORTABLE agent-config switch (Section 8) ---
  "target_agent": "leo"                         // "leo" | "gilfoyle" (or any personal Hermes id)
}
```

The `brand` block is **scraped, not hand-typed** — Pattern 5 (`brand-scrape.mjs`) runs first against `client_site`, writes `brand.json`, and pre-populates `primary`/`font`/`logo`. The agent confirms or overrides.

---

## 1. The file tree a new demo generates

```
~/.hermes/demos/{{slug}}/
├── playwright-scripts/
│   ├── lib/
│   │   └── playwright-utils.mjs          # P1 — shared lib: sentinel contract + per-source extract* TODOs
│   ├── {{source}}-scrape.mjs    (×N)     # P2 — one scraper per sources[] entry
│   ├── {{slug}}-brief.mjs                # P3 — orchestrator (execFileAsync + Promise.all)
│   ├── report-build.mjs                  # P4 — HTML→PDF branded report; section body = TODO
│   ├── brand-scrape.mjs                  # P5 — brand harvester; run ONCE at scaffold time
│   ├── mocks/
│   │   └── {{source}}-mock.html  (×N)    # offline demo data — runs with zero credentials
│   ├── output/                           # screenshots land here (gitignored)
│   ├── briefs/                           # orchestrator JSON/MD artifacts
│   ├── reports/                          # generated PDFs
│   ├── assets/                           # logo/favicon/og-image downloaded by brand-scrape
│   └── package.json                      # playwright dependency
├── mcp-server/
│   └── server.py                         # P6 — tool defs + sentinel parsing + email send
├── agent-config/
│   └── target.json                       # PORTABLE switch payload (Section 8) — leo | personal
└── RUNBOOK.md                            # local copy; canonical lives in engine-ai-os/Runbooks (Section 9)

~/.hermes/scripts/demo-model.sh           # P7 — SHARED model toggle (not per-demo; created once)
```

Invariant: each `sources[]` entry produces exactly **three** stamped artifacts — a scraper (`{{source}}-scrape.mjs`), a mock (`mocks/{{source}}-mock.html`), and an `extract{{Source}}()` function in `playwright-utils.mjs`.

---

## 2. What each file contains (generalized skeleton)

### File 1 — `playwright-scripts/lib/playwright-utils.mjs` (Pattern 1, the keystone)

The single most load-bearing convention. Every script emits **exactly one sentinel-prefixed compact-JSON line on stdout**; all human/diagnostic output goes to **stderr**. Consumers scan for the **last** sentinel line and `JSON.parse` the tail — no fragile brace-matching of pretty-printed JSON.

```js
import { chromium } from 'playwright';
import { mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SCREENSHOT_DIR = join(__dirname, '..', 'output');
const MOCK_HTML_DIR  = join(__dirname, '..', 'mocks');
mkdirSync(SCREENSHOT_DIR, { recursive: true });

export const MODE = process.env.PLAYWRIGHT_MODE || 'mock';   // mock | live
export const RESULT_PREFIX = '__{{SLUG_UPPER}}_RESULT__';

export function emitResult(r) { process.stdout.write(RESULT_PREFIX + JSON.stringify(r) + '\n'); }

export function parseResult(stdout) {                         // read the LAST sentinel line
  const lines = stdout.split('\n');
  for (let i = lines.length - 1; i >= 0; i--) {
    const idx = lines[i].indexOf(RESULT_PREFIX);
    if (idx !== -1) return JSON.parse(lines[i].slice(idx + RESULT_PREFIX.length));
  }
  throw new Error('no ' + RESULT_PREFIX + ' line in script output');
}

export function getScreenshotPath(name) {
  const ts = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '');
  return join(SCREENSHOT_DIR, `${name}-${ts}.png`);
}
export async function launchBrowser() { return chromium.launch({ headless: true }); }
export async function newPage(b) { return b.newPage({ viewport: { width: 1400, height: 900 }, deviceScaleFactor: 2 }); } // retina
export const mockUrl = (f) => `file://${join(MOCK_HTML_DIR, f)}`;
export const getProductionUrl = (site) => ({ {{SOURCE_ID}}: '{{LIVE_URL}}' }[site] || '#');

// --- PER-CLIENT TODO: one extract<Source>(page) per source, written AFTER
//     inspecting the real/mock DOM. Each is a page.evaluate returning plain JSON. ---
export async function extract{{Source}}(page) {
  return page.evaluate(() => { /* querySelectorAll('{{KEY_SELECTOR}}') -> [{...}] */ });
}
```

- **Auto from config:** the whole shell, the `RESULT_PREFIX` sentinel, the `getProductionUrl` map.
- **Human fills:** each `extract{{Source}}()` body (the only file-1 bespoke piece).

### File 2 — `playwright-scripts/{{source}}-scrape.mjs` (Pattern 2, ×N)

Identical shape for every source: take the entity arg, branch `mock|live`, wait for a selector (non-fatal fallback), extract, full-page screenshot, `emitResult`. Diagnostics to stderr only.

```js
import { launchBrowser, newPage, getScreenshotPath, mockUrl, getProductionUrl,
         extract{{Source}}, MODE, emitResult } from './lib/playwright-utils.mjs';

const ENTITY = process.argv[2] || '{{DEFAULT_ENTITY}}';

async function main() {
  console.error(`[{{source}}] start: ${ENTITY} (mode=${MODE})`);
  const browser = await launchBrowser();
  const page = await newPage(browser);
  try {
    await page.goto(MODE === 'mock' ? mockUrl('{{MOCK_HTML}}') : getProductionUrl('{{source}}'),
                    { waitUntil: 'networkidle' });
    await page.waitForSelector('{{KEY_SELECTOR}}', { timeout: 10000 })
              .catch(() => console.error('[{{source}}] selector fallback'));
    const data = await extract{{Source}}(page);
    const screenshot = getScreenshotPath('{{source}}');
    await page.screenshot({ path: screenshot, fullPage: true });
    emitResult({ source: '{{SOURCE_LABEL}}', entity: ENTITY, mode: MODE,
                 count: data.length, rows: data, screenshot,
                 assessment: { /* PER-CLIENT derived fields */ } });
  } finally { await browser.close(); }
}
main().catch(() => process.exit(1));
```

- **Auto:** the control flow, mode branch, screenshot, emit shape.
- **Human fills:** the `assessment` block (derived/scored fields specific to the deliverable).

### File 2b — `playwright-scripts/mocks/{{source}}-mock.html` (×N)

A static HTML stub per source carrying believable synthetic data, structured so the source's `key_selector` matches. This is what makes the demo runnable **offline with zero credentials**. Skeleton is auto-stamped (a wrapper plus N rows); the human edits the synthetic values to match the client's domain tension.

### File 3 — `playwright-scripts/{{slug}}-brief.mjs` (Pattern 3, orchestrator)

Runs all scrapers **truly in parallel** with `execFileAsync` + `Promise.all` (NOT `execSync` in a loop — that silently serializes). Each child runs its own headless browser. Dual output: `OUTPUT_MODE=json` → single `emitResult` line for the MCP server; otherwise human console + writes `.json`/`.md` artifacts.

```js
import { execFile } from 'child_process'; import { promisify } from 'util';
import { join, dirname } from 'path'; import { fileURLToPath } from 'url';
import { mkdirSync, writeFileSync } from 'fs';
import { parseResult, emitResult } from './lib/playwright-utils.mjs';
const execFileAsync = promisify(execFile);
const DIR = dirname(fileURLToPath(import.meta.url));
const ENTITY = process.argv[2] || '{{DEFAULT_ENTITY}}';
const MODE = process.env.PLAYWRIGHT_MODE || 'mock';
const JSON_ONLY = process.env.OUTPUT_MODE === 'json';

async function runScript(name, arg) {
  const { stdout } = await execFileAsync('node', [join(DIR, name), arg],
    { env: { ...process.env, PLAYWRIGHT_MODE: MODE }, encoding: 'utf-8',
      timeout: 60000, maxBuffer: 10 * 1024 * 1024 });
  return parseResult(stdout);
}

async function main() {
  const t0 = Date.now();
  const [{{RESULT_VARS}}] = await Promise.all([
    {{#each sources}}runScript('{{id}}-scrape.mjs', ENTITY),{{/each}}
  ]);
  const brief = {
    entity: ENTITY, generated: new Date().toISOString(),
    elapsed_seconds: +((Date.now() - t0) / 1000).toFixed(1), mode: MODE,
    summary: `{{SUMMARY_TEMPLATE}}`,
    /* PER-CLIENT TODO: fold each source result into structured sections */
    screenshots: [{{#each sources}}{{var}}.screenshot,{{/each}}],
  };
  const slug = ENTITY.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
  mkdirSync(join(DIR, 'briefs'), { recursive: true });
  writeFileSync(join(DIR, 'briefs', `${slug}-${Date.now()}.json`), JSON.stringify(brief, null, 2));
  if (JSON_ONLY) emitResult(brief); else console.log(/* human summary */);
}
main().catch(e => { console.error('orchestrator:', e.message); process.exit(1); });
```

- **Auto:** the `Promise.all` source list, the parse/write plumbing, dual output.
- **Human fills:** the `summary` string and the compile-into-sections block.

### File 4 — `playwright-scripts/report-build.mjs` (Pattern 4, HTML→PDF)

Runs the orchestrator with `OUTPUT_MODE=json`, parses the sentinel, **base64-inlines all images** as data-URIs (so the PDF is self-contained), builds one branded HTML string, then `chromium → setContent(networkidle) → page.pdf(A4, printBackground, zero margins)`, and `emitResult({ pdf, title, summary })`.

```js
const C = { primary: '{{BRAND_PRIMARY}}', ink: '{{BRAND_INK}}',
            muted: '{{BRAND_MUTED}}', panel: '#f7f7f8', line: '#e6e6e8' };
const dataUri = (p, mime) => existsSync(p) ? `data:${mime};base64,${readFileSync(p).toString('base64')}` : '';
const esc = s => String(s ?? '').replace(/[&<>"']/g, c =>
  ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

async function getBrief() {
  const { stdout } = await execFileAsync('node', [join(__dirname, '{{slug}}-brief.mjs'), ENTITY],
    { env: { ...process.env, PLAYWRIGHT_MODE: MODE, OUTPUT_MODE: 'json' },
      encoding: 'utf-8', timeout: 60000, maxBuffer: 10 * 1024 * 1024 });
  return parseResult(stdout);
}

function buildHtml(b) {
  const logo  = dataUri(join(ASSETS, '{{LOGO_FILE}}'), 'image/png');
  const shots = (b.screenshots || []).map(s => dataUri(s, 'image/png'));
  return `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    @import url('https://fonts.googleapis.com/css2?family={{BRAND_FONT}}:wght@400;600;800&display=swap');
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:'{{BRAND_FONT}}',-apple-system,Arial,sans-serif;color:${C.ink};
         -webkit-print-color-adjust:exact;print-color-adjust:exact;font-size:12px}
    .rule{height:5px;background:${C.primary}} .kicker{color:${C.primary}}
    /* masthead / titleblock / summary / section / figure / footer — verbatim shell */
  </style></head><body>
    <div class="masthead">${logo ? `<img src="${logo}"/>` : '{{CLIENT_NAME}}'}</div>
    <div class="rule"></div>
    <!-- PER-CLIENT TODO: <section> layout for this deliverable -->
    <div class="footer"><b>{{CLIENT_NAME}}</b> · {{DELIVERABLE_NOUN}}
         <span class="confidential">COMMERCIAL IN CONFIDENCE</span></div>
  </body></html>`;
}

async function main() {
  const b = await getBrief();
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.setContent(buildHtml(b), { waitUntil: 'networkidle' });
  const slug = ENTITY.toLowerCase().replace(/[^a-z0-9]+/g, '-');
  const pdf = join(REPORT_DIR, `{{SLUG_UPPER}}-{{DELIVERABLE_NOUN}}-${slug}.pdf`);
  await page.pdf({ path: pdf, format: 'A4', printBackground: true,
                   margin: { top: '0', bottom: '0', left: '0', right: '0' } });
  await browser.close();
  emitResult({ entity: ENTITY, pdf, title: `{{CLIENT_NAME}} {{DELIVERABLE_NOUN}} — ${ENTITY}`, summary: b.summary });
}
```

- **Auto:** brand CSS shell, `dataUri`/`esc` helpers, the PDF call, masthead/footer.
- **Human fills:** the `<section>` body layout for this deliverable.

### File 5 — `playwright-scripts/brand-scrape.mjs` (Pattern 5, run ONCE)

The auto-branding engine. Point it at `{{CLIENT_SITE}}`; it returns logo candidates, a colour palette (weighted frequency of computed colours on header/nav/button/headings — backgrounds weighted ×3, text ×1), fonts, and downloads raster logo/favicon/og-image into `assets/`. Writes `brand.json` and emits a compact JSON line. **Reusable verbatim** — only `SITE` and the asset filename prefix change. The skill runs this first and pipes palette[0]/fonts[0]/downloaded[0] into the `brand{}` config block.

### File 6 — `mcp-server/server.py` (Pattern 6, tools + sentinel + email)

```python
SCRIPTS_DIR = Path(os.path.expanduser("~/.hermes/demos/{{slug}}/playwright-scripts"))
RESULT_PREFIX = "__{{SLUG_UPPER}}_RESULT__"
GAPI = os.path.expanduser("~/.hermes/skills/productivity/google-workspace/scripts/google_api.py")
SENDER = "{{SENDER}}"
DEFAULT_RECIPIENTS = {{DEFAULT_RECIPIENTS}}   # SAFE default — never the client until told

def _resolve_node() -> str:                   # launchd/gateway runs minimal PATH; bare `node` fails
    env_bin = os.environ.get("{{SLUG_UPPER}}_NODE_BIN")
    if env_bin and Path(env_bin).exists(): return env_bin
    if (f := shutil.which("node")): return f
    for c in ("/opt/homebrew/opt/node/bin/node","/opt/homebrew/bin/node","/usr/local/bin/node"):
        if Path(c).exists(): return c
    return "node"
NODE_BIN = _resolve_node()

def run_script(name, *args):                  # Python mirror of parseResult()
    env = {**os.environ, "PLAYWRIGHT_MODE": "mock", "OUTPUT_MODE": "json"}
    r = subprocess.run([NODE_BIN, str(SCRIPTS_DIR/name), *args], env=env,
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0: raise RuntimeError(f"exit {r.returncode}: {r.stderr[:500]}")
    for line in reversed(r.stdout.splitlines()):
        i = line.find(RESULT_PREFIX)
        if i != -1: return json.loads(line[i+len(RESULT_PREFIX):])
    raise RuntimeError(f"no {RESULT_PREFIX}: {r.stdout[:500]}")

# Tool defs: one Tool(...) per mcp_tools[], named {{slug}}_{{tool}}.
# The email_report tool's DESCRIPTION carries a directive prompt:
#   "ALWAYS use this when asked to email/send the report. Do NOT hand-compose,
#    do NOT ask for approval first." — this steers the model to the tool.
# call_tool returns TextContent + base64 ImageContent per screenshot.
```

- **Keep verbatim:** `_resolve_node` (launchd PATH fix), `run_script` (sentinel parse), the directive-style email-tool description.
- **Human fills:** the tool list, per-tool `format_*()` output formatting (→ Telegram/text).

### File 7 — `~/.hermes/scripts/demo-model.sh` (Pattern 7, SHARED — created once)

Flips the gateway's single `model.default` between a daily-driver model and a stronger demo model, then `launchctl kickstart -k` + sleep to reload. Generalize as `demo-model.sh {{DEMO_MODEL}} {{DAILY_MODEL}}` with `pro|flash|status` verbs. Verbatim except the two model IDs and the launchd label `ai.hermes.gateway`. **Never run at the shell during a live demo** — switch the model *in-chat* instead (see Reliability, Section 7).

### Email send — the cross-cutting gotcha (Pattern 7)

`email_report` builds the branded PDF then shells to `google_api.py gmail send --to … --from … --html --body <html> --attach <pdf>`. **Load-bearing:** the `gws` CLI passes the raw MIME as an argv parameter, which blows the OS arg-length limit on any PDF-sized payload. So the code branches — `gws` only when there are **no** attachments; **whenever there is an attachment, fall back to the Python Google client** (`service.users().messages().send(body={'raw': ...})`, POSTed over HTTP). Any scaffolded demo that emails attachments MUST use the Python-client path, never `gws --attach`.

---

## 3. The auto vs. manual split (the "hybrid" line)

| Layer | How it's produced |
|---|---|
| P1 lib shell, sentinel, `getProductionUrl` map | **Fully auto** from config |
| P2/P3 control flow, mode branch, parse/write plumbing | **Fully auto** |
| P4 brand CSS shell + PDF call + helpers | **Fully auto** |
| P5 brand-scrape | **Verbatim** (only `SITE` changes) |
| P6 `_resolve_node`, `run_script`, email plumbing | **Verbatim** |
| P7 model toggle + email Python-client path | **Verbatim** (model IDs only) |
| Brand colours / font / logo | **Scraped** by P5 → `brand.json` → config (agent confirms) |
| Per-source `extract{{Source}}()` DOM selectors (P1) | **Human fills** after inspecting site/mock |
| Orchestrator compile-into-sections block (P3) | **Human fills** |
| Report `<section>` layout (P4) | **Human fills** |
| Mock HTML synthetic values (P2b) | **Human fills** (skeleton auto) |

**Invariants to preserve in every clone:** stdout = one sentinel JSON line, stderr = everything else · parse the **LAST** sentinel line · `execFileAsync` + `Promise.all` for real parallelism · inline images as data-URIs for self-contained PDFs · `_resolve_node` for launchd PATH · Python client (not `gws`) for attachments · default recipients = internal, **never** the client until explicitly told.

---

## 4. Placeholder reference

| Placeholder | Source field | Used in |
|---|---|---|
| `{{slug}}` / `{{SLUG_UPPER}}` | `client_slug` | dir, file prefixes, sentinel, tool names, `_NODE_BIN` env |
| `{{CLIENT_NAME}}` | `client_name` | report masthead/footer, MCP, runbook |
| `{{CLIENT_SITE}}` | `client_site` | brand-scrape `SITE` |
| `{{DELIVERABLE_NOUN}}` | `deliverable_noun` | report title, PDF filename, footer |
| `{{DEFAULT_ENTITY}}` / entity arg | `primary_entity_arg` | every script's `process.argv[2]` |
| `{{source}}` / `{{Source}}` / `{{SOURCE_LABEL}}` | `sources[].id` / `.label` | scraper names, extract fns, emit `source` |
| `{{MOCK_HTML}}` | `sources[].mock_html` | scraper mock branch |
| `{{KEY_SELECTOR}}` | `sources[].key_selector` | `waitForSelector` + extract |
| `{{LIVE_URL}}` | (filled at go-live) | `getProductionUrl` map |
| `{{BRAND_PRIMARY/INK/MUTED}}` / `{{BRAND_FONT}}` / `{{LOGO_FILE}}` | `brand.*` | report CSS |
| `{{SENDER}}` / `{{DEFAULT_RECIPIENTS}}` | `sender` / `default_recipients` | MCP email |
| `{{slug}}_{{tool}}` | `mcp_tools[]` | MCP Tool names |
| `{{DEMO_MODEL}}` / `{{DAILY_MODEL}}` | (runtime config) | `demo-model.sh` |
| `{{TARGET_AGENT}}` | `target_agent` | portable switch (Section 8) |

---

## 5. Step-by-step generation checklist

1. **Collect config** through the interview; confirm the config object with the human.
2. **Run brand-scrape first.** Stamp `brand-scrape.mjs`, run it against `client_site`, parse `brand.json`, populate `brand{}` (agent confirms palette/font/logo or overrides).
3. **Create the tree.** `~/.hermes/demos/{{slug}}/{playwright-scripts/{lib,mocks,output,briefs,reports,assets},mcp-server,agent-config}` + `package.json` (playwright dep).
4. **Stamp File 1** `lib/playwright-utils.mjs` with the sentinel and one `extract{{Source}}()` TODO per source.
5. **Stamp File 2 ×N** one `{{source}}-scrape.mjs` per `sources[]` entry.
6. **Stamp File 2b ×N** one `mocks/{{source}}-mock.html` stub per source (skeleton + N rows matching `key_selector`).
7. **Stamp File 3** `{{slug}}-brief.mjs` orchestrator with the `Promise.all` source list.
8. **Stamp File 4** `report-build.mjs` with brand CSS shell.
9. **Stamp File 6** `mcp-server/server.py` with `_resolve_node`/`run_script` verbatim, one Tool per `mcp_tools[]`, directive email description.
10. **Stamp File 7** `~/.hermes/scripts/demo-model.sh` if it does not already exist (shared, created once per host).
11. **HUMAN FILLS the bespoke blocks** after inspecting site/mock HTML: each `extract{{Source}}()` (step 4), each `assessment` block (step 5), mock synthetic values (step 6), orchestrator sections + summary (step 7), report `<section>` layout (step 8).
12. **Write the portable agent-config** (`agent-config/target.json`) and wire to the chosen target (Section 8).
13. **Run mock end-to-end:** `PLAYWRIGHT_MODE=mock node {{slug}}-brief.mjs "<entity>"` then `report-build.mjs` → confirm a PDF lands in `reports/`.
14. **Register the MCP server** with the target agent and validate the **real path** (chat message → correct tool fires), not the tool in isolation.
15. **Switch demo model in-chat**, run the dry-run harness (Section 7), confirm every scripted question fires the right tool.
16. **Emit the runbook** (Section 9) only after the end-to-end live-gateway validation passes.

---

## 6. Configuration files written

- `playwright-scripts/package.json` — `{ "type": "module", "dependencies": { "playwright": "^1.x" } }`.
- `mcp-server/` registration entry — added to the **target agent's** MCP config (path depends on target; Section 8).
- `agent-config/target.json` — the portable switch payload (Section 8).
- `brand.json` — emitted by brand-scrape; the source of brand placeholders.

---

## 7. Reliability hardening (bake into the agent + a dry-run harness)

1. **Switch the model in-chat, session-scoped — never at the shell.** Before the demo run the in-chat switch to Pro (`/model <pro>`); restore Flash (`/model <flash>`) after. NEVER paste shell/restart commands (`launchctl kickstart`, gateway restarts, `hermes …`) into the demo chat — that reboots the gateway and kills the live session.
2. **Pin the behaviour guardrail verbatim in the demo path:** for any demo request, call the matching tool, present ONLY its result cleanly, then STOP. No terminal commands, no file edits, no codebase searches, no installs, no extra "helpful" engineering — this is a client-facing path.
3. **Grounding rule:** answer only from tool output; never invent figures. If uncertain, refuse rather than free-form. Never reveal data is synthetic unless asked.
4. **Fallback model = Flash, not a free/over-eager model.** Free models ignore behaviour instructions; keep them off any live demo path.
5. **Test the REAL path:** send an actual chat message and confirm the model fires the correct tool (e.g. "give me the GeoTech brief" → `{{slug}}_brief`). Calling the MCP tool directly proves nothing about message→tool routing.
6. **Pre-warm every dependency** (browsers, OAuth tokens, caches) so there's nothing for the model to "helpfully fix" live.
7. **Put the wow in an emailed PDF, not inline chat** — inline media is unreliable on weaker models. Deliver the branded artifact via `{{slug}}_email_report`.
8. **Dry-run harness:** a script that fires every scripted demo question through the live gateway and asserts the correct tool call + non-empty sentinel result; include fallback phrasing for tool timeouts.

---

## 8. The portable agent-config switch (Leo vs personal Hermes)

The same demo wires to **either** Leo (the shared/managed EngineAI Chief-of-Staff Hermes) **or** a personal/local Hermes (e.g. Gilfoyle), selected by a single `target_agent` variable. Keep all wiring agent-agnostic; only the four bindings below change.

`agent-config/target.json`:
```jsonc
{
  "target_agent": "leo",                  // "leo" | "gilfoyle" (any personal Hermes id)
  "leo": {
    "mcp_config_path": "<Leo gateway MCP config>",     // managed, shared
    "channel": { "platform": "telegram|slack", "id": "<Leo demo channel>" },
    "persona": "Leo — EngineAI Chief of Staff",
    "secret_store": "<Leo managed credential store>"
  },
  "gilfoyle": {
    "mcp_config_path": "~/.hermes/config/mcp.json",    // local, personal
    "channel": { "platform": "telegram", "id": "<personal demo channel>" },
    "persona": "Gilfoyle — personal Hermes",
    "secret_store": "~/.hermes/secrets/"               // local
  }
}
```

What the switch controls — and what differs per target:

| Concern | Leo (shared/managed) | Personal Hermes (Gilfoyle) |
|---|---|---|
| MCP registration path | Leo's managed gateway MCP config | local `~/.hermes/config/mcp.json` |
| Channel + ownership | EngineAI-owned demo channel; team-visible | personal channel; only you see it |
| Persona | "Leo — EngineAI Chief of Staff" | "Gilfoyle" (personal voice) |
| Secret / credential storage | Leo managed store | local `~/.hermes/secrets/` |
| Who can see the demo | EngineAI team / client on shared channel | private to the operator |
| Model toggle | via Leo's gateway label | via local `demo-model.sh` + local launchd label |

**The wiring step (step 12):** read `target_agent`, then (a) register `mcp-server/server.py` at that target's `mcp_config_path`, (b) point the demo at that target's `channel`, (c) set the agent's standing persona/instructions to that target's `persona` (plus the Section-7 guardrail), (d) resolve secrets from that target's store. Everything else — the scripts, the sentinel contract, the PDF pipeline — is identical across targets.

**Migrating personal → Leo for delivery:** flip `target_agent` to `leo`, re-run step 12 (re-register the MCP server at Leo's config path, repoint the channel, swap the persona), move credentials into Leo's managed store, then re-run steps 14–15 (validate the real path + dry-run) against Leo before any client-facing run.

---

## 9. Per-client runbook emission

**When:** at the end of a successful build, **after** the demo path has been validated end-to-end through the **live gateway** (not just tools-called-directly). Emitting before validation produces a runbook with unchecked validation boxes — the one section that must be true.

**What:** fill `live-agent-demo-template.md` — every `{CURLY_BRACE}` placeholder filled, all _italic guidance_ deleted — matching the shape of `live-agent-demo-cds-example.md` (the gold-standard target). Cross-reference the `runbook-creator` skill.

**Naming:** filename = **skill folder name** (README rule: "Runbook filename = skill folder name … keep them in lockstep"). If the build's skill lives at `Skills/{skill-folder}/`, the runbook is `Runbooks/{skill-folder}.md`. The template's own `Runbooks/{client}-{demo}.md` is the fallback only when there is no paired skill folder.

**Placeholder → data mapping** (all collected during the build):

| Template section | Filled from |
|---|---|
| Title `{Client} {Demo} — Presentation Runbook` | client name + demo name |
| Audience · Presenter · Date | attendees, presenter (default `joe@engineai.co.nz`), demo date |
| The demo in one line | agreed value prop, framed as time/effort saved |
| Where the visuals live | output split: which surface returns text reliably + the bulletproof hero artifact and where it lands |
| Validation status checkboxes | actual end-to-end results: each command fired on natural phrasing via live gateway; hero artifact confirmed delivered; exact model tested on |
| Part 0 / Part 1 host machine | host that runs the agent + wake/plug-in steps |
| In-chat model commands | demo model + daily model + exact in-chat switch commands (`/model {demo}` ↔ `/model {daily}`) |
| Chat surface | Telegram/Slack/web + specific chat name |
| Commands 1–3 / cheat card | exact validated phrasings from rehearsal + blunt fallback `Run the {tool} for {input}`; Command 3 = hero-artifact trigger |
| Part 2 beats | manual status quo, data sources pulled, time taken, finale artifact contents |
| Honesty rules | mock/sandbox vs live; which figures illustrative; where the artifact is sent (presenter, not client, if it holds sample data) |
| Safety-net paths | absolute path to pre-generated hero artifact + screenshots on host |
| Break-glass table | tool-specific blunt re-phrasing + backup-artifact location |
| Model / reliability notes | the Section-7 guardrail added to standing instructions; demo vs fallback model rationale |
| Under the hood | tools/MCP exposed (names), data sources, mock-vs-live split, artifact pipeline, backup repo, roadmap to authenticated/live |

CDS worked reference (the example file, lines 1–126): tools `cds_geotech_brief` / `cds_consent_status` / `cds_supplier_check` / `cds_email_report`; model commands `/model deepseek/deepseek-v4-pro` ↔ `/model deepseek/deepseek-v4-flash`; artifact `~/.hermes/demos/cds/reports/CDS-GeoTech-Brief-westgate-trunk-sewer.pdf`; backup repo `github.com/Tradie-AI-2000/wardo-hermes`.

**After writing — commit + link:**
1. **Write** the filled file to `/Users/joeward/Developer/EngineAI/engine-ai-os/Runbooks/{skill-folder}.md` (the private repo).
2. **Commit it into `engine-ai-os/Runbooks`** so every build leaves a durable, versioned operating procedure beside the template and the CDS example.
3. **Link it from `Runbooks/README.md`** — add a per-client / service-offering row following the existing pattern:
   `| [{Client} {Demo}]({skill-folder}.md) | [`../Skills/{skill-folder}/`](../Skills/{skill-folder}/) | {one-line description} |`
   This keeps the "filename = skill folder name … lockstep" invariant true and makes the runbook discoverable, not orphaned.

**Paths:**
- Template: `/Users/joeward/Developer/EngineAI/engine-ai-os/Runbooks/live-agent-demo-template.md`
- Worked example: `/Users/joeward/Developer/EngineAI/engine-ai-os/Runbooks/live-agent-demo-cds-example.md`
- Index to update: `/Users/joeward/Developer/EngineAI/engine-ai-os/Runbooks/README.md`
- Emit target: `/Users/joeward/Developer/EngineAI/engine-ai-os/Runbooks/{skill-folder}.md`
- Local copy: `~/.hermes/demos/{{slug}}/RUNBOOK.md`
