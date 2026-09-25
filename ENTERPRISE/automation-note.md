# Maintainer automation note (not a buyer task)

Enterprise inquiries do **not** require the buyer to push code, copy files,
or run the hourly dual-agent cycle. That work is maintainer-side.

## What is automated from the public repo side
The hourly dual-agent upgrade (Code Structure & Prototype Upgrader +
Enterprise & Business Ventures Agent) is intended to:

1. Read `STATUS.md` and `GOAL.md`
2. Apply 1–3 honesty-preserving improvements
3. Push those files to `trigger6980/doctorate-natural-electric-ai-2036` via the GitHub connector
4. Record what landed in `STATUS.md`

If the connector is unavailable in a given hour, `STATUS.md` must say
**No structural change this hour — monitoring only**. It must not invent a push.

## What a buyer still does
- Open an `enterprise-inquiry` issue (or email) using the public templates
- Mark the scope-assumptions table
- Sign a written contract before private artifacts move

Buyers are not asked to operate Git, CI, or the agent cycle.

## What this page is not
Not an SLA. Not a ticket bot. Not a published price. Not a claim that every
hourly run lands code — some hours correctly monitor only.
