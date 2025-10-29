# FPSci IQP 2025 Harness CLI

A CLI for facilitating experiments in FPSci IQP 2025.

## Quick start

Make sure `input-injector.exe` is in the root of where you cloned this repo to.

[Install `uv`](https://docs.astral.sh/uv/getting-started/installation/)

Activate virtual environment:

```shell
uv venv
.venv\Scripts\activate
```

Start the harness CLI:

```shell
harness
```

## Settings

You can add a `.env` file at root to set how the CLI should be ran. This is the same
as setting flags manually on the command line. An example:

```bash
# .env
VERBOSE=True
RANDOMIZE_GAMES=False
RANDOMIZE_LATENCIES=False
GAME_DURATION=3
```

This will make `harness start` emits extra debug logs, doesn't randomize games and latencies
and each game round will last 3 seconds.

## Interesting folders to look at

C:\Users\shengmei\Desktop\OLD STUFF\User-Study-Game-Performance-Analysis-ISU-main
C:\Users\shengmei\Desktop\OLD STUFF\Flow
C:\Users\shengmei\Desktop\OLD STUFF\TestingHarness