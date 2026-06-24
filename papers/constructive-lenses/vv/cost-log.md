# Operation Cost Log

<!-- Token-cost tracking for major framework operations.

     Log discrete, named, repeatable operations whose cost is worth
     comparing across sessions or reporting in a decision-record
     evidence base. Don't log incidental tool calls or general
     drafting — only operations whose cost-vs-value tradeoff you
     might want to argue about later.

     The point is to make framework overhead legible: cost-per-pass,
     cost-per-paper, and over time, the cost side of cost-vs-value
     claims in decision records (e.g., DR-011's "Pass 2 every major
     revision" prescription becomes empirically priceable).

     Convention introduced in v1.6.0. See DR-011 Evidence Base for
     the canonical use case. -->

**Paper:** [paper title]
**Started logging:** [date]

## How to use this log

1. Before a named operation, note input + output + cache tokens from `/status`. (For an Agent / subagent call, note `total_tokens` from the tool result — Agent tool results report a total only, not the input / output / cache breakdown.)
2. Run the operation.
3. Note tokens from `/status` again. The deltas are this operation's cost.
4. Add a row below with the deltas and a one-line note about findings or value delivered.

Operations worth logging:

- DR-011 review passes (Pass 1 Haiku / Pass 2 Opus / Pass 3 cross-vendor)
- `/curate` and `/audit-context` skill invocations
- Batch citation verification (`python -m tools.check_dois <registry>`)
- Coverage gates (`python -m tools.coverage <registry> --strict`)
- Full Gate sweeps before a phase transition
- One-shot heavy operations (e.g., manuscript-wide consistency check)

Operations not worth logging individually:

- Incidental file reads, edits, single-claim verifications
- General drafting time
- Anything you wouldn't compare across sessions or report empirically

## Log

| Date | Operation | Total tokens | Input Δ | Output Δ | Cache read | Wall clock | Notes |
|------|-----------|--------------|---------|----------|------------|------------|-------|
| [YYYY-MM-DD] | [e.g., DR-011 Pass 1 (Haiku) on §4 revision] | [N] | [N] | [N] | [N] | [Ns or Nm] | [findings, value notes] |

If a column has no data (e.g., subagent total only), leave it blank. Total is the load-bearing number; the others sharpen accounting when available.

## Aggregation (after ~10 entries)

Summarize by operation type for use in decision-record evidence bases:

| Operation type | N | Mean total tokens | Load-bearing findings (or value delivered) | Notes |
|----------------|---|-------------------|--------------------------------------------|-------|
| [e.g., DR-011 Pass 1 Haiku] | [N] | [mean] | [e.g., "0 / N rounds — Pass 2 catches what Pass 1 misses at this scope"] | |
| [e.g., DR-011 Pass 2 Opus] | [N] | [mean] | [e.g., "M load-bearing design findings across N rounds"] | |

When the aggregation table has enough N to be load-bearing, the data point belongs in a DR's Evidence Base (with a back-pointer to this log file as the primary source).
