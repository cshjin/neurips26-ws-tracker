# NeurIPS 2026 Workshop Tracker

A community-maintained tracker for all **102 accepted NeurIPS 2026 workshops** (Sydney, Paris, Atlanta): submission deadlines, page limits, and which CFPs have a **low-effort submission track** — position papers, tiny papers, extended abstracts, or a CFP that explicitly welcomes negative / preliminary / work-in-progress results.

Live site: https://cshjin.github.io/neurips26-ws-tracker/

Repo: https://github.com/cshjin/neurips26-ws-tracker

Source list: [NeurIPS 2026 workshop announcement](https://blog.neurips.cc/2026/08/10/announcing-the-neurips-2026-workshops/) (2026-08-10).

## What's here

- `index.html` — the tracker page. Static, no build step, no dependencies beyond one Google Fonts link. Reads `data.json` at load time.
- `data.json` — the actual dataset: one entry per workshop (name, URL, city, deadline, page limits, low-effort-track verdict, one-line scope, status).
- `.github/workflows/deploy-pages.yml` — deploys `index.html` + `data.json` to GitHub Pages on every push to `main`.
- `.github/workflows/validate-data.yml` + `.github/scripts/validate_data.py` — runs on every push/PR that touches `data.json`, checks it's valid JSON, has all required fields, and rejects malformed entries (bad city name, malformed date, duplicate rows, etc.) before it can merge.

## Deploying with GitHub Pages

Pages is configured to deploy via the `deploy-pages.yml` workflow (build type "GitHub Actions", not the legacy branch-based source), so pushing to `main` is enough — no manual steps needed. If you fork this repo, enable Pages once under **Settings → Pages → Build and deployment → Source: GitHub Actions**, and the workflow handles the rest.

To preview locally before pushing, `fetch()` needs an actual HTTP origin (opening the file directly via `file://` will fail due to CORS), so run a tiny local server from this folder:

```bash
python3 -m http.server 8000
# then open http://localhost:8000/
```

## Data model (`data.json`)

Each workshop object:

| Field | Meaning |
|---|---|
| `name` | Workshop title |
| `url` | Workshop's own site |
| `city` | `Sydney` \| `Paris` \| `Atlanta` (NeurIPS 2026 runs across three locations) |
| `deadline` | Submission deadline, `YYYY-MM-DD`, or `null` if not yet posted. Assume **AoE** unless the workshop's own CFP says otherwise. |
| `pages` | Free-text summary of tracks/page limits, e.g. `"9pp full / 4pp short"` |
| `lowEffort` | `true` = CFP confirmed to have a position/tiny/extended-abstract/demo track or explicitly welcomes negative/WIP results. `false` = checked, only full experimental papers accepted. `null` = not yet confirmed (page didn't load, or CFP wasn't live yet at last check). |
| `lowEffortNote` | One-line description of which track qualifies |
| `scope` | One-line topic summary |
| `status` | Lifecycle status. Currently always `"CFP open"` — intended to be updated to things like `"Reviewing"`, `"Notifications out"`, `"Accepted"`, `"Program posted"` as each workshop's cycle progresses (see Roadmap). |

`meta.lastChecked` is the date the dataset was last verified against the live CFP pages.

## Contributing

This is meant to be tracked and corrected by more than one person:

- **Deadline changed / extended?** Update the `deadline` field for that workshop and open a PR.
- **We got a low-effort-track call wrong** (missed a track, or a workshop added one after our last check)? Fix `lowEffort` / `lowEffortNote` and open a PR.
- **A workshop's CFP wasn't live when we checked** (`deadline: null`, `lowEffort: null`)? Once it's posted, fill in the real values.
- **New workshop info** (a typo in the official list, a workshop that got cancelled, a merged/renamed workshop)? Same process — edit `data.json` directly, the page picks it up automatically.

No build step, so a PR against `data.json` is the entire contribution. Please keep entries evidence-based (i.e., quote or link what the workshop's own CFP says) rather than guessing. Before opening a PR, run the same check CI runs:

```bash
python3 .github/scripts/validate_data.py
```

## Roadmap (not yet built)

- Track per-workshop **notification / acceptance timelines** as they're announced (add fields like `notificationDate`, `programUrl`, `status: "Accepted" / "Rejected" / "Notified"` once workshops start sending decisions, roughly September 2026 onward for most of these).
- Possibly split `status` into workshop-level lifecycle (open → reviewing → notified → program posted) vs. any personal per-submission tracking, so the two don't get tangled in one shared file.

## Caveats

- CFPs get extended or edited without notice. This tracker reflects a **snapshot**, not a live feed — always confirm on the workshop's own page before submitting.
- A handful of workshop sites had no CFP text live yet, or returned nothing on fetch, at last check. Those show up as `TBD` / "Unconfirmed" in the UI rather than being guessed at.
- "Low-effort track" describes what the CFP *allows*, not what will get accepted — reviewers still judge submissions on merit.

## License

MIT — see `LICENSE`. Attribution to the workshops' own CFPs belongs to their organizers; this repo only aggregates publicly posted information.
