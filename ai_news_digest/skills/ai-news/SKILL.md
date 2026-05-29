---
name: ai-news-digest
description: Gather and compile the top AI news from the most recent day into a structured, well-sourced digest. Use this skill whenever the user asks for AI news, an "AI news roundup," "what's happening in AI today," a daily or morning AI briefing, the latest in artificial intelligence, recent model or product releases, or any request to catch up on current developments in AI/ML — even if they never say the word "digest." Trigger it for phrasings like "what's new in AI," "catch me up on AI," "today's AI headlines," "AI news for a specific date," or "give me the AI rundown." Prefer this skill over a single ad-hoc search, because the value is in broad multi-category coverage plus careful sourcing.
---

# AI News Digest

Produce a digest of the most important AI developments for a given day. The goal is breadth (you didn't miss the big stories), trustworthiness (every item is sourced and primary where possible), and signal (you separated genuinely important news from churn).

## Workflow

Follow these steps in order. Don't shortcut to a single search — the whole point is comprehensive, deduplicated coverage.

### 1. Anchor the date and window

Establish today's date from context. The default window is **the last 24 hours**. If searches for the last day come back thin (a quiet news day), widen to the last 2–3 days and say so explicitly in the digest header (e.g. "Covering May 27–29"). Never silently mix a week of old news into a "today" digest.

When you build search queries, use the actual current year, and prefer the word "today" or the explicit date over stale phrasing.

### 2. Search across all categories

Run **separate** searches for each category below — a combined query returns shallow results for everything. Aim for roughly 6–12 searches total, more if the user wants depth. Skip a category only if repeated searches show genuinely nothing new.

- **Model & product releases** — new models, major version bumps, API/feature launches, benchmarks. Queries: "AI model release today", "new LLM announced", "<lab name> launch".
- **Research & papers** — notable papers, techniques, results. Queries: "AI research paper this week", "machine learning breakthrough".
- **Business & funding** — raises, acquisitions, partnerships, earnings, leadership moves. Queries: "AI startup funding today", "AI company acquisition".
- **Policy, regulation & safety** — legislation, lawsuits, government action, safety findings. Queries: "AI regulation news", "AI lawsuit", "AI safety".
- **Industry & discourse** — adoption, infrastructure (chips, data centers), and significant debates. Queries: "AI chip news", "AI industry today".

For each promising hit where the search snippet is too thin to summarize accurately, **fetch the source** to get the real detail. Don't write a summary off a headline alone.

### 3. Prioritize trustworthy, primary sources

Consult `references/sources.md` for a curated list of reliable AI news outlets and primary sources. Favor original sources — a lab's own announcement, the paper, the SEC filing, the official blog — over aggregators and rewrites. When two outlets conflict, note it rather than picking one silently. Be skeptical of single-source rumors, unconfirmed leaks, and obvious SEO/press-release spam; either confirm them against a second source or label them as unconfirmed.

### 4. Rank and deduplicate

Many outlets cover the same event — collapse those into one item with the best source. Rank by genuine importance, not recency alone: a major model release outranks a minor feature update even if the update is newer. Lead with the single biggest story of the day.

### 5. Assemble the digest

Use the output format below. Keep each item tight — a couple of sentences of substance, not a full article rehash.

## Output format

Default to delivering the digest **inline in the chat** (it's something the user reads now). If the user asks to save, keep, or send it, write it to a markdown file instead. Use this structure:

```
# AI News — <date or date range>

**Top story:** <one-line headline of the single most important development.>

## 🚀 Models & Products
- **<Headline>** — <1–2 sentence summary in your own words.> [source]

## 🔬 Research
- **<Headline>** — <summary> [source]

## 💰 Business & Funding
- **<Headline>** — <summary> [source]

## ⚖️ Policy & Safety
- **<Headline>** — <summary> [source]

## 🏭 Industry & Infrastructure
- **<Headline>** — <summary> [source]
```

Rules for the format:
- Omit any section that genuinely had no news rather than padding it.
- 3–6 items per active section is a good target; this is a digest, not an archive.
- Every item carries a working source link (the citation system handles attribution; still make the source identifiable).
- End with a one-line "What to watch" pointer only if there's a clear thread to follow (an expected release, a pending ruling). Don't force it.

## Copyright and accuracy (important)

This skill summarizes news, so be disciplined:
- **Write every summary in your own words.** Do not paste article text. Keep any unavoidable direct quote under 15 words, use at most one per source, and only when the exact wording matters.
- Don't reconstruct an article's structure or reproduce its specific phrasing — paraphrase fully.
- If you can't verify a claim, leave it out rather than guessing or inventing an attribution.
- Attribute concrete facts to where they came from; flag conflicts and unconfirmed reports honestly.

## Adapting to the user

- If the user names a focus ("just LLM releases," "AI policy only," "anything about <company>"), bias the searches and sections toward it.
- If they want it shorter, collapse to the top 5 items overall under a single list.
- If they ask for a recurring/daily format, keep the structure stable run-to-run so it reads like a real briefing.