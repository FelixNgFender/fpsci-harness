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

Conduct a experiment for a participant from a schedule:

```shell
harness conduct --participant [NUMBER 1-40]
```

In case the harness is bugged out during a specific game, exit and restart or
start the next game in a schedule with the
`--starting-game [dave_the_diver, half_life_2, fitts_law, feeding_frenzy, rocket_league]`
flag. For help on specific commands in the harness, add a '-h' flag to get help.

## Install ruff & ty code extensions

These extensions are needed for formatting and type checking before pushing
code. To install, follow these steps.

1. Go to VSCode Marketplace
1. Search for 'ruff'
1. Install the ruff extension that appears
1. Then, search for 'ty'
1. Install the ty extension that appears

## Settings

You can add a `.env` file at root to set how the CLI should be ran. This is the
same as setting flags manually on the command line. An example:

```bash
# .env
VERBOSE=True
```

This will make `harness start` emits extra debug logs.

## Formatting and Typecheck

Run these lines before pushing any code to make sure our code is formatted
properly and there are no bad type assignments.

`uv format && ty check`

## Rocket League Parsing

Rocket League parsing is done by
[`rrrocket`](https://github.com/nickbabcock/rrrocket). A Windows binary has to
be provided at root.
