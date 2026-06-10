# Demo Reliability Hardening

The demo doesn't fail because the build is wrong. It fails because the agent
*freelances* on stage — runs a terminal command, "helpfully" fixes something,
drops the photo it was meant to attach, or doesn't fire the tool at all because
the request was phrased loosely. Every item below comes from a real CDS demo
failure. Treat this as a pre-flight checklist, and read the WHY so you know which
corner you can't cut.

This applies to demos running on **either** runtime target (Leo / shared EngineAI
Hermes, or a personal Hermes like Gilfoyle). The model-switch verbs and fallback
model are gateway-level settings — confirm them on whichever gateway is driving
the demo.

---

## The checklist (run this every time)

```
[ ] Switched to the demo (Pro) model IN-CHAT, session-scoped
[ ] Behaviour guardrail pasted into the agent's standing instructions
[ ] Global fallback model is Flash (or equiv) — NOT a free/over-eager model
[ ] Every scripted question tested through the REAL chat path (message → tool)
[ ] All deps pre-warmed: browsers, OAuth tokens, caches
[ ] Hero artifact is an emailed branded PDF — not inline chat media
[ ] NO shell / restart / gateway commands will be pasted into the demo chat
```

---

## 1. Switch the model in-chat, session-scoped — never at the shell

**Do:** before the demo, switch to the stronger demo model from *inside the chat*:
`scripts/demo-model.sh pro` or the in-chat `/model <pro>` command. Afterwards,
restore the daily driver with `flash` / `/model <flash>`.

**Never:** paste shell, restart, or gateway-control commands into the demo chat —
`launchctl kickstart`, `hermes ...`, any "restart the gateway" instruction.

**WHY:** restarting the gateway from inside the chat reboots the very process
that is hosting the live session — it kills the demo mid-sentence, in front of
the client. The in-chat `/model` switch is session-scoped: it changes behaviour
without touching the process. The shell path and the chat path must stay
separate. The chat is a *client surface*, not a terminal.

---

## 2. Pin the behaviour guardrail verbatim in the agent's standing instructions

Add this wording, as-is, to the demo agent's standing instructions:

> For any demo request: call the matching tool, present ONLY its result cleanly,
> then STOP. No terminal commands, no file edits, no codebase searches, no
> software installs, no extra "helpful" engineering, no freelancing. This is a
> client-facing path.

**WHY:** the default failure mode of a capable model on stage is *being helpful*.
It sees a rough edge and reaches for the terminal, edits a file, or goes
exploring — all visible to the client, all off-script, all capable of breaking
the session. The guardrail draws a hard line: tool in, result out, stop. It is
the single most important sentence in the whole demo.

---

## 3. Point the global fallback model at something sane

Set the gateway's fallback model to **Flash** (or an equivalent instruction-following
model) — **never** a free or over-eager model. (Gemma was switched off the fallback
slot for exactly this reason.)

**WHY:** free models *ignore behaviour instructions*. Proven on real runs: they
mark mail as read despite an explicit "KEEP UNREAD" directive, and they mangle
MEDIA directives. If the primary model ever drops to the fallback mid-demo, you
need the fallback to still respect your guardrails — not to go rogue. A free
model on the fallback slot is a loaded gun pointed at the demo.

---

## 4. Test the REAL path, not the tool in isolation

Verify by **sending an actual chat message** and confirming the model fires the
correct tool. Example: type "give me the GeoTech brief" and confirm it routes to
`cds_geotech_brief`. Test the natural, slightly-vague phrasings a client would
actually use — and record the wording that fired reliably.

**WHY:** calling the MCP tool directly proves nothing. The failure mode lives in
the **message-to-tool routing**, not in the tool. The tool can be perfect and the
demo can still die because the model didn't recognise the intent from a loose
request and instead free-formed a reply. If you only ever tested the tool
directly, you never tested the thing that breaks.

> Belt-and-braces: the email tool's MCP description should carry a directive
> ("ALWAYS use this when asked to email/send… do NOT hand-compose, do NOT ask
> for approval first") so vague phrasing still lands on the tool. Keep a blunt
> fallback phrasing in your back pocket: `Run the {tool} for {input}`.

---

## 5. Pre-warm every dependency before going on stage

Get browsers launched, OAuth/auth tokens valid and refreshed, and caches warm
*ahead of time*. There should be nothing left for the model to "helpfully fix"
live — no logins, no installs, no setup steps.

**WHY:** every cold dependency is an invitation for the model to freelance (see
item 2). An expired token tempts it to re-auth; a missing browser tempts it to
install Playwright; a cold cache adds latency that reads as "frozen" on stage. A
warm system has no rough edges for the model to reach toward — it can only do the
one thing you scripted.

---

## 6. Put the visual "wow" in an emailed PDF, not inline chat media

Deliver the polished, branded artifact as an **emailed PDF** (e.g.
`cds_email_report`). Do not rely on inline images in the chat for the climax.

**WHY:** inline chat media is unreliable on weaker models — MEDIA directives get
dropped or mangled, and images silently fail to render. A silent failure at the
finale is the worst possible time. The emailed PDF is bulletproof: it's generated
server-side, self-contained (images base64-inlined), on-brand, and lands in a real
inbox the client keeps. The client *leaves with a tangible artifact* instead of
squinting at a chat bubble that may or may not have rendered.

> Attachment gotcha: send PDFs via the Python Google client, never the `gws` CLI
> with `--attach` — the raw MIME message is passed as an argv parameter and a
> PDF-sized payload blows the OS arg-length limit. The `email_report` tool path
> already forces the Python client; keep it that way.

---

## The one-line summary

The chat is a stage, not a terminal. Pin the guardrail, switch the model in-chat,
keep the fallback sane, warm every dependency, test the message→tool path the
client will actually use, and put the wow in an emailed PDF. Everything off that
path is freelancing — and freelancing is how demos die.
