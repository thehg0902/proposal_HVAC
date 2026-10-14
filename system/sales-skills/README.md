# Parked skills — agency sales

These three skills are PARKED: they live outside `.claude/skills/`, so Claude
Code does not discover them, `lint-skills.py` does not check them, and they do
not appear in `system/docs/REGISTRY.md` or cost description tokens in a build
session.

| skill | what it holds |
|---|---|
| `cold-outreach` | WOSS frame control, cold email/DM structure, call scripts, gatekeeper handling, follow-up cadence |
| `sales-calls-and-pricing` | pre-call prep, SPIN bank, call flow, qualification, project-math pricing, recap email, KCS, upsells |
| `objections-and-closes` | three aikido moves, objection bank, CTA laddering, the boost stack, close library |

Parked at v1.12.0 because they run the agency's client-acquisition work, not a
website build — no pipeline phase invokes them. Nothing was edited; the folders
are byte-identical to what was in `.claude/skills/`.

## Restore one

```bash
git mv system/sales-skills/<name> .claude/skills/<name>
```

Then re-run `python3 system/scripts/generate-skill-registry.py` and restore the
skill's name in the "Not for …" routing clause of any related skill's
description.

## Note on `objections-and-closes`

This is the borderline one. It owns CTA laddering, the objection bank, and the
boost stack, and both `copywriting` and `site-architecture` treat "objection
order" and "objection block" as build inputs — that content is currently
supplied by the RESEARCH BRIEF's build directives instead. If website CTAs or
objection sections start reading thin, restore this one first.
