# Task: `svc_boot_healthcheck`

Repair the tiny service stack in this repository.

The repository contains:

- `stack.web` - a localhost HTTP server
- `stack.worker` - a worker that writes a heartbeat file
- `stack.mailer` - a worker that writes a ready marker and a heartbeat file
- `scripts/boot_stack.py` - starts the stack
- `scripts/stop_stack.py` - stops the stack
- `tools/healthcheck.py` - prints JSON health information

## Requirements

After your fix:

- `python3 scripts/boot_stack.py` must start the stack.
- `python3 tools/healthcheck.py` must print JSON to stdout.
- The JSON must reflect the actual configured runtime values.
- The stack must work both with defaults and with overridden:
  - `STACK_PORT`
  - `STACK_STATE_DIR`
  - `STACK_HEARTBEAT_TTL`
- The healthcheck must fail when the worker heartbeat becomes stale.
- `python3 scripts/stop_stack.py` must stop started processes cleanly.

## Visible Check

Run:

```bash
python3 visible_check.py
```
