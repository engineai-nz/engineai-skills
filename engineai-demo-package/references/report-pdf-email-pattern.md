# Reference: Branded PDF Report → Client Inbox

The "leave-behind" finale of a demo. The agent harvests the client's brand off their
website, renders an on-brand HTML report to PDF via Playwright (with the live
data-source screenshots embedded), and emails the PDF as an attachment from a Workspace
account. The client walks out of the meeting with a tangible, on-brand artifact in their
real inbox.

This doc gives generalized, copy-pasteable skeletons. All client specifics are written as
`{{PLACEHOLDER}}` — the scaffolder fills them from the per-client config object. CDS values
appear only as illustrative comments.

Pipeline:

```
brand-scrape.mjs   ──→  brand.json   ──┐
  (run once)                           ├─→ report-build.mjs ──→ {{deliverable}}.pdf ──→ email (Gmail python client) ──→ client inbox
{{slug}}-brief.mjs ──→ screenshots ────┘     (HTML→PDF via Playwright,
  (orchestrator, OUTPUT_MODE=json)              images inlined as data-URIs)
```

---

## The keystone: the `__RESULT__` stdout contract

Every Node script in this pattern communicates results as **exactly one sentinel-prefixed
compact-JSON line on stdout**. All human/diagnostic logging goes to **stderr**. The Python
caller (MCP server) greps the **last** sentinel line and `JSON.parse`s the remainder — never
brace-matching of pretty-printed multi-line JSON.

```js
// in scripts/lib/playwright-utils.mjs
export const RESULT_PREFIX = '__{{SLUG_UPPER}}_RESULT__';   // e.g. __CDS_RESULT__

export function emitResult(r) {
  process.stdout.write(RESULT_PREFIX + JSON.stringify(r) + '\n');
}

export function parseResult(stdout) {        // read the LAST sentinel line, not the first
  const lines = stdout.split('\n');
  for (let i = lines.length - 1; i >= 0; i--) {
    const idx = lines[i].indexOf(RESULT_PREFIX);
    if (idx !== -1) return JSON.parse(lines[i].slice(idx + RESULT_PREFIX.length));
  }
  throw new Error('no ' + RESULT_PREFIX + ' line in script output');
}
```

Invariants for everything below:

- **stdout = one sentinel JSON line. stderr = everything else.** Never `console.log` diagnostics.
- **Parse the LAST sentinel line** — earlier output (warnings, nested child stdout) is ignored.
- `report-build.mjs` calls the brief orchestrator with `OUTPUT_MODE=json` so it emits a single
  result line, then parses it. The report builder itself emits its own result line
  (`{ pdf, title, summary }`) for the MCP server / emailer to consume.

---

## Step 1 — Scrape the client's brand (run ONCE at scaffold time)

`brand-scrape.mjs` points Playwright at the client's site and harvests:

- **Logo candidates** — `<img>` whose `src`/`alt`/`class` contains `logo`, or any img inside
  `header`/`nav`, plus inline header/nav `<svg>`.
- **Colour palette** — tally computed colours across `header, nav, button, h1, h2, a`,
  weighting **backgrounds ×3, text ×1** by frequency. `palette[0]` is the brand primary.
- **Fonts** — computed `font-family` over `body, h1, h2, nav, button`.
- **Raster assets** — download logo / favicon / og-image into `assets/`.

Output: writes `brand.json` AND emits a compact JSON line on stdout. The scaffolder parses
it and uses `palette[0]` / `fonts[0]` / first downloaded logo to populate the brand config —
**branding is scraped, not hand-typed.** The agent then confirms / overrides with the human.

```js
// brand-scrape.mjs — reusable verbatim; only SITE + asset prefix change
import { chromium } from 'playwright';
import { writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const SITE = '{{CLIENT_SITE}}';                 // e.g. https://www.cdsnz.co.nz
const ASSETS = join(process.cwd(), 'assets');
mkdirSync(ASSETS, { recursive: true });
const abs = (u) => { try { return new URL(u, SITE).href; } catch { return null; } };

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 }, deviceScaleFactor: 2 });
  await page.goto(SITE, { waitUntil: 'networkidle' });

  // --- logo candidates ---
  const logos = await page.evaluate(() => {
    const out = new Set();
    document.querySelectorAll('img').forEach((i) => {
      const hay = `${i.src} ${i.alt} ${i.className}`.toLowerCase();
      if (hay.includes('logo') || i.closest('header,nav')) out.add(i.src);
    });
    document.querySelectorAll('header svg, nav svg').forEach(() => out.add('inline-svg'));
    return [...out];
  });

  // --- palette by weighted frequency (bg ×3, text ×1) ---
  const palette = await page.evaluate(() => {
    const tally = {};
    const bump = (c, w) => { if (c && !/rgba?\(0, 0, 0, 0\)|transparent/.test(c)) tally[c] = (tally[c] || 0) + w; };
    document.querySelectorAll('header, nav, button, h1, h2, a').forEach((el) => {
      const s = getComputedStyle(el);
      bump(s.backgroundColor, 3);
      bump(s.color, 1);
    });
    return Object.entries(tally).sort((a, b) => b[1] - a[1]).map(([c]) => c);
  });

  // --- fonts ---
  const fonts = await page.evaluate(() =>
    [...new Set([...document.querySelectorAll('body, h1, h2, nav, button')]
      .map((el) => getComputedStyle(el).fontFamily.split(',')[0].replace(/["']/g, '').trim()))]);

  // --- download raster assets ---
  const downloaded = [];
  for (const u of logos.filter((l) => l !== 'inline-svg').map(abs).filter(Boolean)) {
    try {
      const res = await page.context().request.get(u);
      const ext = (u.split('.').pop() || 'png').split('?')[0].slice(0, 4);
      const file = join(ASSETS, `{{SLUG}}-logo-${downloaded.length}.${ext}`);
      writeFileSync(file, await res.body());
      downloaded.push(file);
    } catch { /* non-fatal */ }
  }

  await page.screenshot({ path: join(ASSETS, '{{SLUG}}-site.png'), fullPage: true });
  await browser.close();

  const brand = { site: SITE, primary: palette[0], palette, fonts, logos, downloaded };
  writeFileSync(join(process.cwd(), 'brand.json'), JSON.stringify(brand, null, 2));
  process.stdout.write('__{{SLUG_UPPER}}_RESULT__' + JSON.stringify(brand) + '\n');
}
main().catch((e) => { console.error('brand-scrape:', e.message); process.exit(1); });
```

Resulting `brand.json` feeds the `brand` block of the per-client config:

```jsonc
"brand": {
  "primary": "#FF4000",      // palette[0] from scrape — confirm with human
  "ink":     "#1a1a1a",
  "muted":   "#767676",
  "font":    "Raleway",      // fonts[0]
  "logo":    "assets/{{slug}}-logo-0.png"  // downloaded[0]
}
```

---

## Step 2 — Render the branded HTML report to PDF (`report-build.mjs`)

Reusable mechanics:

1. Run the brief orchestrator via `execFileAsync` with `OUTPUT_MODE=json`; `parseResult` the
   sentinel line to get `{ summary, screenshots, ...sections }`.
2. **Base64-inline every image** (logo + each screenshot) as a `data:` URI so the PDF is fully
   self-contained — no external file refs, no broken-image boxes in the final PDF.
3. Build one HTML string with a brand CSS block (colours/font from `brand.json`).
4. `chromium → page.setContent(html, { waitUntil: 'networkidle' }) → page.pdf(...)` at A4,
   `printBackground: true`, zero margins.
5. `emitResult({ entity, pdf, title, summary })` for the emailer.

The `esc()` HTML-escaper and `dataUri()` helper are verbatim-reusable. The masthead/footer
CSS shell is verbatim; the report `<section>` body is a per-client TODO (this is where the
deliverable's actual layout lives — fill it after seeing the data shape).

```js
// report-build.mjs
import { chromium } from 'playwright';
import { execFile } from 'child_process';
import { promisify } from 'util';
import { readFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { parseResult, emitResult } from './lib/playwright-utils.mjs';

const execFileAsync = promisify(execFile);
const __dirname = dirname(fileURLToPath(import.meta.url));
const ASSETS = join(__dirname, 'assets');
const REPORT_DIR = join(__dirname, '..', 'reports');
mkdirSync(REPORT_DIR, { recursive: true });

const ENTITY = process.argv[2] || '{{DEFAULT_ENTITY}}';
const MODE = process.env.PLAYWRIGHT_MODE || 'mock';

// brand config (from brand.json, confirmed by human)
const C = { primary: '{{BRAND_PRIMARY}}', ink: '{{BRAND_INK}}',
            muted: '{{BRAND_MUTED}}', panel: '#f7f7f8', line: '#e6e6e8' };

// --- verbatim-reusable helpers ---
const dataUri = (p, mime) =>
  existsSync(p) ? `data:${mime};base64,${readFileSync(p).toString('base64')}` : '';
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// 1. run orchestrator, parse the sentinel
async function getBrief() {
  const { stdout } = await execFileAsync(
    'node', [join(__dirname, '{{slug}}-brief.mjs'), ENTITY],
    { env: { ...process.env, PLAYWRIGHT_MODE: MODE, OUTPUT_MODE: 'json' },
      encoding: 'utf-8', timeout: 60000, maxBuffer: 10 * 1024 * 1024 });
  return parseResult(stdout);
}

// 2 + 3. inline images, build HTML
function buildHtml(b) {
  const logo  = dataUri(join(ASSETS, '{{LOGO_FILE}}'), 'image/png');
  const shots = (b.screenshots || []).map((s) => dataUri(s, 'image/png')).filter(Boolean);

  const figures = shots.map((src, i) => `
    <figure class="fig">
      <img src="${src}" alt="data source ${i + 1}"/>
      <figcaption>Source ${i + 1} — captured live ${esc(b.generated || '')}</figcaption>
    </figure>`).join('');

  return `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    @import url('https://fonts.googleapis.com/css2?family={{BRAND_FONT}}:wght@400;600;800&display=swap');
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:'{{BRAND_FONT}}',-apple-system,Arial,sans-serif;color:${C.ink};
         -webkit-print-color-adjust:exact;print-color-adjust:exact;font-size:12px}
    .masthead{display:flex;align-items:center;justify-content:space-between;padding:24px 40px}
    .masthead img{height:40px}
    .rule{height:5px;background:${C.primary}}
    .kicker{color:${C.primary};font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:11px}
    .titleblock{padding:32px 40px 8px}
    .titleblock h1{font-size:26px;font-weight:800;margin-top:6px}
    .summary{margin:16px 40px;padding:16px 20px;background:${C.panel};border-left:4px solid ${C.primary}}
    .section{padding:16px 40px}
    .section h2{font-size:15px;border-bottom:1px solid ${C.line};padding-bottom:6px;margin-bottom:10px}
    .fig{margin:14px 40px;border:1px solid ${C.line};border-radius:6px;overflow:hidden}
    .fig img{width:100%;display:block}
    .fig figcaption{font-size:10px;color:${C.muted};padding:6px 10px;background:${C.panel}}
    .footer{margin-top:24px;padding:14px 40px;border-top:1px solid ${C.line};
            font-size:10px;color:${C.muted};display:flex;justify-content:space-between}
    .confidential{color:${C.primary};font-weight:600}
  </style></head><body>
    <div class="masthead">
      ${logo ? `<img src="${logo}" alt="{{CLIENT_NAME}}"/>` : '<b>{{CLIENT_NAME}}</b>'}
      <span class="kicker">{{DELIVERABLE_NOUN}}</span>
    </div>
    <div class="rule"></div>

    <div class="titleblock">
      <div class="kicker">{{DELIVERABLE_NOUN}}</div>
      <h1>${esc(b.title || ENTITY)}</h1>
    </div>

    <div class="summary">${esc(b.summary || '')}</div>

    <!-- ============================================================= -->
    <!-- PER-CLIENT TODO: the deliverable's section layout.            -->
    <!-- Fold b's structured fields into <div class="section"> blocks. -->
    <!-- e.g.  <div class="section"><h2>Findings</h2> ... </div>       -->
    <!-- ============================================================= -->

    <div class="section"><h2>Data sources</h2></div>
    ${figures}

    <div class="footer">
      <span><b>{{CLIENT_NAME}}</b> &middot; {{DELIVERABLE_NOUN}}</span>
      <span class="confidential">COMMERCIAL IN CONFIDENCE</span>
    </div>
  </body></html>`;
}

// 4 + 5. render to PDF, emit result
async function main() {
  const b = await getBrief();
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.setContent(buildHtml(b), { waitUntil: 'networkidle' });

  const slug = ENTITY.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
  const pdf = join(REPORT_DIR, `{{SLUG_UPPER}}-{{DELIVERABLE_NOUN_SLUG}}-${slug}.pdf`);
  await page.pdf({ path: pdf, format: 'A4', printBackground: true,
                   margin: { top: '0', bottom: '0', left: '0', right: '0' } });
  await browser.close();

  emitResult({ entity: ENTITY, pdf,
               title: `{{CLIENT_NAME}} {{DELIVERABLE_NOUN}} — ${ENTITY}`,
               summary: b.summary });
}
main().catch((e) => { console.error('report-build:', e.message); process.exit(1); });
```

**Templatize:** brand colours/font/logo file, client name, deliverable noun, the `<section>`
body. Keep `dataUri`/`esc`, the masthead/footer shell, and the `page.pdf` call verbatim.

Why inline images: a PDF that references `file://` or `http://` images will render blank boxes
on another machine or after the temp files are cleaned up. Base64 data-URIs make the PDF a
single portable file — exactly what you want to email and what survives being forwarded.

---

## Step 3 — Email the PDF as an attachment (THE GOTCHA)

The email tool builds the branded PDF (Step 2) and shells out to the Workspace helper to send
it as an attachment from a Workspace account, with a small branded covering note as the HTML
body.

```python
# in the MCP server (e.g. email_report tool)
import sys, subprocess, os

GAPI   = os.path.expanduser("~/.hermes/skills/productivity/google-workspace/scripts/google_api.py")
SENDER = "{{SENDER}}"                          # e.g. Joe Ward <joe@engineai.co.nz>
DEFAULT_RECIPIENTS = {{DEFAULT_RECIPIENTS}}    # SAFE default — internal only, never the client until told

def email_report(pdf: str, subject: str, data: dict, recipients=None):
    recipients = recipients or DEFAULT_RECIPIENTS
    cmd = [
        sys.executable, GAPI, "gmail", "send",
        "--to", ", ".join(recipients),
        "--subject", subject,
        "--from", SENDER,
        "--html",
        "--body", _email_body_html(data),     # tiny branded covering note
        "--attach", pdf,                       # <-- forces the python-client path internally
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
```

### THE GOTCHA — attachments must use the Gmail python client, NOT a gws-style argv path

The Workspace helper (`google_api.py gmail send`) has two internal send paths:

- **No attachment** → it may pass the raw MIME message as an **argv parameter** to a `gws`-style
  CLI. Fine for small text bodies.
- **With an attachment** → the raw MIME message now contains the **base64-encoded PDF**, which is
  far too large to pass on `argv`. The OS enforces a maximum total argument length
  (`ARG_MAX` / `E2BIG`); a PDF-sized payload blows straight past it and the send fails (or is
  silently truncated).

So the helper **branches on `has_attachments`**: it only takes the `gws` argv route when there are
no attachments. **Whenever there is an attachment it MUST fall back to the Gmail Python client**,
which POSTs the message body over HTTPS rather than smuggling it through `argv`:

```python
# inside google_api.py gmail_send — the branch you must rely on
def gmail_send(to, subject, sender, html, body, attach=None):
    msg = _build_mail(to=to, subject=subject, sender=sender, html=html, body=body, attach=attach)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    if not attach:
        # small payload — gws argv path is OK
        return _gws_send_via_argv(raw)

    # ATTACHMENT PRESENT: never argv (ARG_MAX). Use the Google python client — POSTs over HTTP.
    service = _gmail_service()                                  # authed googleapiclient
    return service.users().messages().send(
        userId="me", body={"raw": raw}
    ).execute()
```

Rule for any scaffolded demo that emails attachments: **pass `--attach` and let the helper take
the python-client branch. Never hand-build a `gws ... --attach` argv invocation** — it will hit
the arg-length limit on any real PDF.

### The covering-email body

Keep it tiny and on-brand — the PDF is the payload, the email is just the wrapper:

```python
def _email_body_html(data: dict) -> str:
    C = "{{BRAND_PRIMARY}}"
    return f"""<div style="font-family:Arial,sans-serif;color:#1a1a1a;max-width:560px">
      <div style="height:4px;background:{C}"></div>
      <p>Hi,</p>
      <p>{esc(data.get('summary',''))}</p>
      <p>Full {{DELIVERABLE_NOUN}} attached as a PDF.</p>
      <p style="color:#767676;font-size:12px;margin-top:24px">Delivered via Engine AI</p>
    </div>"""
```

### Recipient safety

`DEFAULT_RECIPIENTS` is **internal only** (e.g. the presenter's own address). The agent emails the
client's *real* inbox only when explicitly told to during the demo. This prevents an accidental
send of sample/synthetic data to the client before you mean to.

---

## Step 4 — Wiring into the MCP `email_report` tool

The tool description carries a **directive prompt** so the model reliably reaches for the tool
instead of free-composing an email:

```python
Tool(
    name="{{slug}}_email_report",
    description=(
        "Generate the branded {{DELIVERABLE_NOUN}} PDF for the given {{primary_entity_arg}} "
        "and email it as an attachment. ALWAYS use this when asked to email/send the report. "
        "Do NOT hand-compose an email. Do NOT ask for approval first — just call this."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "{{primary_entity_arg}}": {"type": "string"},
            "recipients": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["{{primary_entity_arg}}"],
    },
)
```

In `call_tool`, build the PDF then call `email_report(...)`, and return a `TextContent`
confirmation. Optionally also return base64 `ImageContent` for each screenshot so the captures
appear inline in the chat — but per the reliability playbook, the **PDF email is the bulletproof
"wow", not inline chat images** (weaker models drop/mangle inline media).

---

## End-to-end smoke test (run before any demo)

```bash
cd ~/.hermes/demos/{{slug}}/playwright-scripts

# 1. brand harvested once at scaffold time
node brand-scrape.mjs          # writes brand.json + assets/

# 2. orchestrator emits a single sentinel line
PLAYWRIGHT_MODE=mock OUTPUT_MODE=json node {{slug}}-brief.mjs "{{DEFAULT_ENTITY}}" \
  | grep '__{{SLUG_UPPER}}_RESULT__'

# 3. report builds a self-contained PDF, emits { pdf, title, summary }
PLAYWRIGHT_MODE=mock node report-build.mjs "{{DEFAULT_ENTITY}}"
ls -la ../reports/   # confirm the PDF exists and opens

# 4. email to the INTERNAL default recipient only (never the client in a test)
#    exercise the python-client attachment path end-to-end
python3 ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py gmail send \
  --to "{{INTERNAL_TEST_RECIPIENT}}" --from "{{SENDER}}" \
  --subject "TEST — {{DELIVERABLE_NOUN}}" --html --body "<p>attachment path test</p>" \
  --attach ../reports/{{SLUG_UPPER}}-{{DELIVERABLE_NOUN_SLUG}}-{{default-entity-slug}}.pdf
```

If step 4 succeeds with the PDF attached and intact, the attachment path is on the python client
and the OS arg-length gotcha is handled.

---

## Invariants checklist (preserve in every clone)

- [ ] stdout = one sentinel JSON line; stderr = all diagnostics.
- [ ] Consumers parse the **LAST** `__{{SLUG_UPPER}}_RESULT__` line.
- [ ] `report-build.mjs` runs the orchestrator with `OUTPUT_MODE=json` and parses its sentinel.
- [ ] All images (logo + screenshots) inlined as base64 data-URIs — PDF is self-contained.
- [ ] `page.pdf` is A4, `printBackground:true`, zero margins; CSS sets `print-color-adjust:exact`.
- [ ] Brand colours/font/logo come from `brand.json` (scraped), confirmed by the human.
- [ ] Attachments go via the **Gmail python client** (`service.users().messages().send`),
      **never** a `gws`-style `--attach` argv path (ARG_MAX / E2BIG).
- [ ] `DEFAULT_RECIPIENTS` is internal-only; client inbox used only when explicitly instructed.
- [ ] `email_report` tool description is directive ("ALWAYS use this… do NOT hand-compose").
