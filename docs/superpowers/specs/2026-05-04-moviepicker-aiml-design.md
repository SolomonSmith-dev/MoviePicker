# MoviePicker v3.0: AI/ML Pivot Design

**Status:** Approved design, consolidating brainstorm Sections 1-5.
**Designed:** 2026-05-04 (Sections 1-4 approved). **Section 5 approved:** 2026-07-09.
**Target:** Ship v3.0 ASAP, starting 2026-07-09. Effort estimate: ~1 weekend.
**Next step after review:** `superpowers:writing-plans` for the v3.0 implementation plan.

---

## 1. Context and goals

MoviePicker pivots from a rule-based recommendation tool to an ML portfolio piece for AI/ML internship applications (graduation December 2026). The project must demonstrate, in a reviewable weekend-sized diff: a real data pipeline from a live system (Jellyfin, 851 movies), classical and embedding-based content recommenders behind a clean seam, and an honest offline evaluation harness.

**Path decision (locked):** Path B, staged release.
- v3.0 = content-based recommender on the Jellyfin catalog (this design).
- v3.1 = MovieLens 25M collaborative filtering + hybrid serving (separate brainstorm later).
- Path A (replace everything with MovieLens-trained CF now) was rejected: 2-3 weekends of schedule risk during internship season for a result that still needs the content-based layer anyway.

**Success criteria:**
1. `moviepicker recommend --strategy all` prints side-by-side top-10 lists from all three recommenders against the real catalog.
2. `EVAL.md` is auto-generated with P@10, HR@10, NDCG@10, MRR (mean ± std over 5 seeds) and an honest-limitations section.
3. Existing rule-based engine and its tests are untouched and still pass.
4. README reframes the project as an ML portfolio piece.

## 2. Scope

**Ships in v3.0:**
1. Jellyfin export script: one-shot dump of the 851-movie catalog plus per-movie watch signal to normalized JSON.
2. Three recommenders behind a shared protocol, selectable at call time:
   - Rule-based engine (existing `RecommendationEngine`, kept byte-identical, wrapped as **Baseline 0**)
   - TF-IDF recommender (**Baseline 1**, scikit-learn)
   - Sentence-transformer recommender (**Production**, `all-MiniLM-L6-v2`)
3. Eval harness: P@10, HR@10, NDCG@10, MRR; 5 random seeds; mean ± std.
4. CLI integration: new non-interactive subcommands (`recommend --strategy {rule,tfidf,embed,all}`, `ingest`, `build-embeddings`, `eval`); no-arg invocation keeps the interactive menu.
5. FastAPI integration: `/recommendations` endpoint gains an optional `strategy` query param (default `embed`), so the existing frontend silently gets better recommendations.
6. README rewrite plus auto-generated `EVAL.md`.

**Explicitly deferred (see roadmap):** live Jellyfin sync, Plex adapter, Letterboxd CSV import, React frontend changes, LLM/RAG layer, multi-user support.

## 3. Architecture

### 3.1 The seam: `RecommenderProtocol`

```python
class RecommenderProtocol(Protocol):
    name: str  # "rule" | "tfidf" | "embed"

    def fit(self, db: Session) -> None: ...

    def recommend(
        self,
        user_id: int,
        k: int = 10,
        exclude_watched: bool = True,
    ) -> list[Recommendation]: ...

@dataclass
class Recommendation:
    movie_id: int
    score: float       # normalized to [0, 1] for cross-recommender comparability
    reason: str
```

Score normalization is min-max within a single `recommend()` call, so scores are comparable across strategies in side-by-side output but are not calibrated probabilities. `reason` is a human-readable one-liner (e.g. "high cosine similarity to 12 Angry Men (0.83)").

### 3.2 Package layout

New sibling package; the existing `src/core/recommendation.py` module is not moved or edited (imports elsewhere stay valid, "Baseline 0 unchanged" stays literally true):

```
src/core/recommenders/
    __init__.py          # get_recommender(name) factory + registry
    protocol.py          # RecommenderProtocol, Recommendation
    rule.py              # adapter wrapping src/core/recommendation.RecommendationEngine
    tfidf.py             # TF-IDF over title+overview+genres+director+cast text
    embed.py             # all-MiniLM-L6-v2 over the same text
    preference.py        # implicit-feedback user preference vector (shared by tfidf/embed)
    embeddings/
        build.py         # builds both TF-IDF and semantic artifacts (~60 LOC)
src/core/ingest.py       # catalog JSON -> SQLAlchemy upsert (~120 LOC)
src/eval/
    metrics.py           # hand-implemented P@k, HR@k, NDCG@k, MRR
    harness.py           # split/seed loop, EVAL.md generation
scripts/export_jellyfin.py  # one-shot Jellyfin dump (~80 LOC)
```

Note (drift from the May pause notes): the notes placed the build script at `src/core/recommendation/embeddings/build.py`, which would require converting the flat `recommendation.py` module into a package and churning its imports. The sibling `recommenders/` package avoids that.

### 3.3 Integration points

**CLI.** The `moviepicker` console script (`src/ui/cli_interface.py:main`) currently launches an interactive menu and has no subcommands; the design's `recommend` command does not exist yet (drift discovered 2026-07-09). v3.0 adds argparse-based dispatch in `main()`:
- `moviepicker` with no arguments: interactive menu, exactly as today.
- `moviepicker recommend [--strategy {rule,tfidf,embed,all}] [--k 10] [--user-id 1]`: non-interactive, prints ranked list(s), exits. `--strategy all` prints the three lists side by side.
- `moviepicker ingest <path>`: runs `src/core/ingest.py` on an export file and prints the `IngestReport`.
- `moviepicker build-embeddings`: runs `embeddings/build.py`.
- `moviepicker eval`: runs the harness and regenerates `EVAL.md`.

**API.** `web/routers/recommendations.py` gains an optional `strategy` query param, default `embed`, falling back to `rule` with a logged warning if embedding artifacts are missing. Response schema unchanged. The React frontend is not touched.

## 4. Data pipeline (3 stages)

**Stage 1: export.** `scripts/export_jellyfin.py` paginates Jellyfin `/Items` and writes `data/catalog/jellyfin-{YYYY-MM-DD}.json` plus a `latest.json` symlink. Credentials are read from `~/.config/moviepicker/.env` (gitignored, outside the repo). Writes to a temp file and renames on success, so a partial export never overwrites `latest.json`.

**Stage 2: ingest.** `src/core/ingest.py` upserts the JSON into SQLAlchemy (`Movie`, `WatchHistory`, favorite/play-count signal). Idempotent: running twice on the same file yields the same DB state. Returns an `IngestReport` (added / updated / skipped counts plus per-record warnings).

**Stage 3: artifacts.** `src/core/recommenders/embeddings/build.py` generates, into gitignored `data/embeddings/`:
- `tfidf_matrix.npz` + `vectorizer.pkl`
- `semantic_embeddings.npy` (851 × 384, ≈1.3 MB)
- `embedding_index.json` (row position → `movie_id`, shared by both artifact sets)

### 4.1 Export schema (confirmed against a real Jellyfin response, 2026-05-04)

```json
{
  "source": "jellyfin",
  "exported_at": "2026-05-04T20:00:00Z",
  "movies": [
    {
      "title": "...",
      "year": 1957,
      "tmdb_id": 389,
      "imdb_id": "tt0050083",
      "overview": "...",
      "genres": ["Drama"],
      "director": "Sidney Lumet",
      "cast": ["Henry Fonda", "Lee J. Cobb", "..."],
      "runtime_min": 96,
      "tmdb_rating": 8.5,
      "language": "en",
      "user_data": {
        "watched": true,
        "play_count": 1,
        "is_favorite": false,
        "last_played_at": "2025-10-23T08:06:16Z",
        "user_rating": null
      }
    }
  ]
}
```

Field derivations from the raw Jellyfin response:
- `tmdb_id` ← `ProviderIds.Tmdb`
- `runtime_min` ← `RunTimeTicks // 600_000_000` (Jellyfin uses 100 ns ticks)
- `director` ← join of `People[Type=="Director"]`
- `cast` ← top 10 `People[Type=="Actor"]` in billing order
- `tmdb_rating` ← `CommunityRating`
- `user_data.user_rating` is always null: Jellyfin does not expose numeric per-user ratings. Favorites and play counts are the only preference signal.

## 5. Preference vector weighting

Both content recommenders build the user profile as a weighted mean of liked-movie vectors:

```python
weight = log(1 + play_count + (1.0 if is_favorite else 0.0)) * exp(-days_since_last_watched / 365)
```

Implicit-feedback confidence (Hu, Koren, Volinsky 2008) times exponential recency decay. README framing (verbatim intent): "production-correct, but at single-user scale weighting differences are within eval noise floor; chosen because it is what production systems do, not because we measured a lift over equal weighting."

## 6. Evaluation

**Four metrics, all implemented by hand** (no sklearn for NDCG):
- **Precision@10**: headline number, position-blind
- **Hit Rate@10**: at least one held-out item in the top 10
- **NDCG@10**: position-aware (Järvelin & Kekäläinen 2002)
- **MRR**: reciprocal rank of the first relevant item

**Method:**
- Held-out set: 20% of liked movies (favorites + watched), re-sampled per seed.
- Seeds 42-46 (5 runs); report mean ± std. No statistical-significance claims at this N.
- Binary relevance only (no numeric rating signal exists in the data).
- Qualitative side-by-side via `moviepicker recommend --strategy all`.

**`EVAL.md`** is auto-generated by `moviepicker eval` with an `Honest limitations` section that names the small-N, single-user, binary-relevance problems before a reviewer can.

## 7. Error handling

- **Export:** unreachable server or invalid API key exits non-zero with a clear message; pagination failure aborts without writing (temp-file-and-rename). No retries in v3.0.
- **Ingest:** a movie missing `tmdb_id` is still ingested, keyed on (title, year); malformed records are skipped and counted in `IngestReport.skipped` with warnings, not silently dropped.
- **Recommenders:** missing artifacts raise `EmbeddingArtifactsMissingError` naming the fix (`moviepicker build-embeddings`); the API route catches it and falls back to `rule` with a logged warning. A user with zero watch signal gets the rule engine's existing cold-start behavior for `rule`, and an explicit "no preference signal" error for `tfidf`/`embed` in v3.0 (cold-start handling is deferred to v3.6+).
- **Eval:** if the liked-movie pool is too small to hold out 20% (fewer than 5 liked movies), the harness exits with an explanatory error instead of producing meaningless numbers.
- **Stale artifacts:** `build.py` stamps artifact files with the catalog export date; recommenders log a warning when the DB contains movies absent from `embedding_index.json`.

## 8. Testing

TDD throughout (per superpowers:test-driven-development). New tests live in `tests/`, alongside the existing suite, which must keep passing unmodified.

- **Protocol conformance:** one parametrized test suite run against all three recommenders on a ~12-movie synthetic fixture catalog (scores in [0,1], watched exclusion, k respected, deterministic given a seed).
- **Metrics:** hand-computed toy examples for each metric, including the worked NDCG example from the Järvelin & Kekäläinen framing.
- **Ingest:** idempotency (run twice, identical DB state and counts), missing-tmdb_id path, malformed-record path.
- **Export:** mocked Jellyfin HTTP responses (pagination, auth failure, partial-write abort). No live network in tests.
- **CLI:** `recommend` subcommand smoke test; no-arg invocation still reaches the interactive menu.
- **Dependency split:** scikit-learn + numpy join core requirements; `sentence-transformers` (which pulls torch) goes in a `requirements-ml.txt` / `[ml]` extra. Embed tests use `pytest.importorskip` so CI stays fast; `embed` strategy raises a clear install hint when the extra is missing.

## 9. Roadmap (Section 5, approved 2026-07-09 as-is)

| Release | Scope | Effort |
|---|---|---|
| v3.0 | Content-based recommender + eval (this design) | 1 weekend |
| v3.0.5 | Diversity reranking, basic filters | half-weekend |
| v3.1 | MovieLens 25M CF + hybrid serving | 2-3 weekends |
| v3.2 | Letterboxd CSV import | 1 weekend |
| v3.3 | LLM/RAG mood query layer | 1 weekend |
| v3.4 | Plex client (multi-source adapter) | half-weekend |
| v3.5 | Live Jellyfin sync | 1 weekend |
| v3.6+ | Frontend, multi-user, cold-start, hyperparameter tuning | open-ended |

Each release is independently shippable. No release retroactively breaks the v3.0 eval.

## 10. Security and credentials

- The Jellyfin API key exposed in chat during May reconnaissance (`6f9a…27cd`) was **revoked** (confirmed 2026-07-09). No outstanding credential exposure.
- The export script reads `JELLYFIN_URL` / `JELLYFIN_API_KEY` from `~/.config/moviepicker/.env`, outside the repo and gitignored by location. Keys are never written to exports, logs, or `EVAL.md`.

## 11. Decisions made while writing this doc (2026-07-09, flagged for review)

1. **CLI reality:** no `recommend` command existed; v3.0 adds argparse dispatch to `main()` with the no-arg interactive menu preserved (Section 3.3).
2. **Package placement:** `src/core/recommenders/` as a sibling package instead of converting `recommendation.py` into a package (Section 3.2).
3. **Dependency split:** heavy ML deps behind an extra so CI and default installs stay light (Section 8).
4. **API default:** `/recommendations` defaults to `embed` with `rule` fallback (Section 3.3), implementing the approved "frontend silently gets better recs" intent.
