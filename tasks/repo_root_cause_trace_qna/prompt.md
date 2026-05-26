# Task: `repo_root_cause_trace_qna`

You are debugging a repository behavior issue.

## User Question

Users sometimes click a "continue onboarding" link from an email and land back on the welcome step instead of the step they were on earlier. This happens more often when they have been idle for a while, even though they did not explicitly abandon onboarding.

Explain the root cause.

## Required Artifact

Write your answer to `answer.md`.

Use these exact top-level headings:

- `# Root Cause`
- `# Evidence`
- `# Fix Outline`

## What A Strong Answer Should Include

- the cleanup path involved
- the specific timestamp field mismatch
- the fallback path that sends users back to welcome
- a concrete, minimal fix direction

No code changes are required for this task.
