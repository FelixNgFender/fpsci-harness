# FPSci IQP 2025 Harness CLI

A CLI for facilitating experiments in FPSci IQP 2025.

## Quick start

Make sure `input-injector.exe` is in the root of where you cloned this repo to.

[Install `uv`](https://docs.astral.sh/uv/getting-started/installation/)

Activate virtual environment:

```shell
uv sync
.venv\Scripts\activate
```

Start the harness CLI:

```shell
harness
```

## Install ruff & ty code extensions
These extensions are needed for formatting and type checking before pushing code. To install, follow these steps.

1. Go to VSCode Marketplace
2. Search for 'ruff'
3. Install the ruff extension that appears
4. Then, search for 'ty'
5. Install the ty extension that appears. You will need to install the pre-release version if VSCode asks to do so.

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

## Formatting and Typecheck
#### Run these lines before pushing any code to make sure our code is formatted properly and there are no bad type assignments.
`uv format && ty check`

## Interesting folders to look at

C:\Users\shengmei\Desktop\OLD STUFF\User-Study-Game-Performance-Analysis-ISU-main
C:\Users\shengmei\Desktop\OLD STUFF\Flow
C:\Users\shengmei\Desktop\OLD STUFF\TestingHarness
