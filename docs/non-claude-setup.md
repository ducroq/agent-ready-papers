# Using agent-ready-papers With Agents Other Than Claude Code

The framework's prose is agent-agnostic (since v2.1.0): the `agents/` directory holds portable role prompts, the Hard Constraint about in-repo `memory/` is generalised across agent vendors, and the README's worked examples cite Haiku, GPT-4o-mini, and Gemini-Flash as equivalent choices. This doc walks through the practical *how* of using the framework with a non-Claude-Code agent.

**Scope:** focused on the three surfaces a non-Claude agent needs to touch — `CLAUDE.md`, `agents/<role>.md`, and the in-repo `memory/` directory. Not a full setup walkthrough for any specific tool; tool installs and authentication are out of scope (consult each tool's own current docs). Vendor-specific syntax in this doc was correct as of writing — verify against each tool's current docs before relying on a specific flag.

## The framework's agent-facing surface

| Surface | Role | What any agent needs to do with it |
|---------|------|-------------------------------------|
| `CLAUDE.md` (root, `templates/`, paper projects) | Repo orientation — Before You Start tables, Hard Constraints, architecture overview | Read at session start so the agent knows what's where. Despite the file name, this is just markdown — any agent that can read project files can use it. |
| `agents/<role>.md` (`equation-checker.md`, `review-prompt.md`) | Portable role-prompt system prompts | Copy the file's contents into the agent's system-prompt slot (or paste at session start). Pair with the artefact to be processed. |
| `memory/` (in-repo, gitignored) | Project state across sessions (versions, narratives, gotchas, priorities) | Read at session start; write at session end. The principle: this-repo state stays here, not in the agent's user-level auto-memory. See the Hard Constraint in the root `CLAUDE.md`. |

## Universal pattern

For most workflows the pattern is the same regardless of agent:

1. **Orient the agent.** Point it at the relevant `CLAUDE.md` (`./CLAUDE.md` for framework-level work; `templates/CLAUDE.md` as the adopter template; `papers/<name>/CLAUDE.md` for paper-specific work).
2. **Load the role prompt.** For verification work, paste `agents/equation-checker.md` or `agents/review-prompt.md` as the agent's system prompt (or include in the first message).
3. **Provide the artefact.** The manuscript section, the registry, the equations — whatever the role prompt operates on.
4. **Persist state.** When the session ends, update `memory/` (in-repo) with what was decided / discovered. Don't rely on the agent's own session memory.

Step 2 is what `agents/` exists for. Step 4 is what the Hard Constraint enforces.

## Tool-specific notes

The notes below are entry points, not full setup guides. Each tool's CLI flags, file-discovery conventions, and authentication change frequently — verify against the tool's current docs before relying on a specific command.

### GitHub Copilot CLI

- **Install / auth:** see <https://docs.github.com/copilot/how-tos/copilot-cli> for the current install command and licensing requirements. The [`agent-ready-assessment`](https://github.com/ducroq/agent-ready-assessment) repo's `docs/copilot-cli-setup.md` has a worked HAN-institutional setup if you need a template; adapt the institutional pieces (GitHub Education licensing, org policy workarounds) to your own context.
- **`CLAUDE.md`:** Copilot CLI does not auto-read `CLAUDE.md` at session start. Point it at the file as the first instruction (e.g. `copilot -p "Read CLAUDE.md, then …"`) or maintain a `.github/copilot-instructions.md` that mirrors the Hard Constraints — Copilot reads that file automatically.
- **`agents/` role prompts:** invoke as `copilot -p "Read 'agents/review-prompt.md' as your system prompt. Then review this manuscript: …"`, or paste the prompt contents directly in interactive mode.
- **Limitations:** no native `.docx` / `.pdf` reading; convert manuscripts to markdown first. No session-persistent memory across runs — the in-repo `memory/` discipline carries the state.

### Cursor

- **Project rules:** Cursor reads `.cursorrules` (older convention) and `.cursor/rules/*.mdc` (newer convention) for project-level system instructions. Cross-tool conventions like `AGENTS.md` are also being adopted across vendors — check Cursor's current docs for which your version reads. The pragmatic move: keep `CLAUDE.md` as the canonical orientation file and add a `.cursorrules` (or symlink / duplicate) that points Cursor at `CLAUDE.md` and the relevant Hard Constraints.
- **`agents/` role prompts:** paste `agents/review-prompt.md` or `agents/equation-checker.md` contents into Cursor's Composer or Chat's system-instructions slot before processing the artefact.

### Continue, Aider, and other CLI agents

- **Continue:** project-level system prompts go in `.continue/config.json` or via project-level `.md` references. Add a `systemMessage` that includes the framework's Hard Constraints, or reference `CLAUDE.md` from the config.
- **Aider:** use `--read CLAUDE.md` (or the current equivalent flag) to include the repo's orientation file in every session.
- **General pattern:** every CLI agent has *some* way to include a markdown file as orientation. The framework's surface is just markdown, so the integration is always *"how does this tool include a markdown file as system context?"*

### Web chat (ChatGPT, Gemini, Claude.ai, Mistral Le Chat)

- **Orientation:** paste the relevant `CLAUDE.md` contents at the start of the conversation, or attach the file if the web UI supports file uploads. ChatGPT's Projects feature, Gemini's Gems, and Claude.ai's Projects all let you pin orientation files at the conversation-room level.
- **`agents/` role prompts:** paste the role prompt contents as the first message of the conversation, followed by the artefact as the second message. For Pass 3 of the multi-pass review (DR-011), this is the typical workflow — cross-vendor review via web chat, with the style/voice filter built into the role prompt itself.
- **Limitations:** no persistent session state across browser tabs / conversations. The `memory/` discipline (write state to in-repo files at session end) becomes *more* important here than in always-on CLI tools, not less.

## Things to verify per tool

The following are tool-specific behaviours the framework cannot assume. Check each one for the agent you use:

- **Does the tool read `CLAUDE.md` automatically at session start?** Claude Code does; most others do not. If not, you need a separate orientation step.
- **Does the tool have a session-persistent system-prompt slot?** Or does the role prompt have to be re-pasted each session?
- **Does the tool support reading `.docx` / `.pdf` / `.bib` natively?** Most don't — convert artefacts to markdown first. Pandoc handles `.docx` → markdown well; `.bib` is already plain text.
- **Does the tool have a per-project rules file convention?** (`.cursorrules`, `.cursor/rules/*.mdc`, `.github/copilot-instructions.md`, `.continue/config.json`, etc.) If yes, mirror the relevant Hard Constraints there so they apply to every session.
- **How does the tool's auto-memory interact with the framework's `memory/` constraint?** If the tool has user-level memory across projects (Claude Code, ChatGPT memory, Gemini memory), treat it like Claude Code's `~/.claude/` — cross-project knowledge only; this-repo state stays in the in-repo `memory/`.

## What you do *not* need to do

- **You do not need to rename `CLAUDE.md` to `AGENTS.md`** to use this framework with a non-Claude agent. The filename is a convention from Claude Code's auto-discovery behaviour; the file contents are plain markdown that any agent can read. Renaming would break Claude Code's auto-discovery without buying anything for other agents (which usually need to be pointed at orientation files explicitly anyway). If you want both Claude Code auto-discovery *and* `AGENTS.md`-aware-tool support: symlink or duplicate, don't pick.
- **You do not need to maintain parallel copies of `agents/` prompts** for different agents. The prompts in `agents/` are written in vendor-neutral form (`"You are an X agent. Your task is to Y."` — see `agents/README.md`) and work across vendors as-is.
- **You do not need a separate per-agent Hard Constraint set** in your paper project. The Hard Constraints in `templates/CLAUDE.md` are agent-agnostic since v2.1.0 — they speak of *"any agent's user-level auto-memory"* rather than naming a specific tool.

## See also

- [README](../README.md#agent-role-prompts) — Agent-Role Prompts section: the index of what's in `agents/`
- [`agents/README.md`](../agents/README.md) — the line between agent-role prompts and fill-in templates, vendor-neutrality convention
- Root [`CLAUDE.md`](../CLAUDE.md) Hard Constraint about in-repo `memory/` — the generalised principle
- [`agent-ready-assessment`](https://github.com/ducroq/agent-ready-assessment) — convention source for the `agents/` directory pattern; the `docs/copilot-cli-setup.md` there has a worked HAN-institutional Copilot CLI example
- [`agent-ready-projects`](https://github.com/ducroq/agent-ready-projects) — companion guide for AI-assisted coding; layered documentation model applies to non-Claude agents the same way
