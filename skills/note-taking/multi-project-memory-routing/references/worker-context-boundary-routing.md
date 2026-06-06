> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Worker Context Boundary Routing

Use this pattern when a project uses Hermes as the coordinator and external workers such as Claude Code, Codex, Cowork, or other CLI agents for implementation/review.

## Core lesson

Do not assume external workers inherit Hermes main-agent memory, the current chat, or the full Obsidian vault. Treat worker context as an explicit prompt/input contract.

Typical wrapper shape:

```text
worker prompt = project context file (.hermes.md / AGENTS.md / equivalent)
              + bounded task file
              + optional safety footer / tool limits
```

Workers may have filesystem tools and can read repo notes, handoff files, and Obsidian-exported Markdown if the task tells them where to look. But "can read" is not the same as "already read".

## Procedure

1. Identify the worker boundary.
   - Main Hermes agent: durable memory, user profile, current conversation, tools, project context.
   - External worker: only whatever the wrapper prompt includes, plus files it is instructed or chooses to read.

2. Inspect or state the wrapper contract before claiming what the worker knows.
   - Which project context file is prepended?
   - Which task file is appended?
   - Are safety footers/tool limits included?
   - Are Obsidian/project notes merely referenced or actually embedded?

3. For long-term goal / current phase / strategy questions, keep project truth in local authority layers:
   - compact current navigation file;
   - active strategy queue;
   - accepted changes / handoff logs;
   - project Obsidian index or project note.

4. For future worker tasks, include a short "Required context reads" block instead of dumping the whole vault:

```text
Before editing or reviewing, read:
- handoff/current_navigation.md
- handoff/active_strategy_queue.md
- notes/obsidian_projects/<Project>.md or project Obsidian index
- relevant accepted_changes / named handoff artifact for this slice
```

5. Keep the worker task bounded.
   - Put durable strategy and rationale in repo/Obsidian.
   - Put only the slice-specific instruction in the task file.
   - Preserve activation/safety gates in both project context and task footer when relevant.

6. When answering the user, distinguish:
   - "guaranteed included in the worker prompt";
   - "available on disk if the worker reads it";
   - "not automatically inherited from Hermes memory/chat".

## Pitfalls

- Saying Claude Code/Codex "knows" Obsidian content because it has file access. It only knows what the prompt embeds or what it reads during the run.
- Copying an entire vault into every worker prompt. Prefer small stable entry points and required reads.
- Updating global Hermes memory with detailed project state just to make workers aware of it. Use project-local context/handoff/Obsidian files and task templates instead.
- Treating worker partial context as project truth. Verify against project authority files before answering status questions.

## Verification

- The wrapper/task explicitly names the context files a worker must read.
- The answer labels prompt-included vs available-on-disk vs not inherited.
- Project-specific details remain in repo handoff or Obsidian, not global memory or this skill.
