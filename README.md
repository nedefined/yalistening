# yalistening
**An open-source Yandex Music module for the Telegram messenger.** Built with Kurigram, Yandex Music API, WebSocket, Rich, and managed via UV.

## Installation

I recommend using the [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager. Pull and install all dependencies from pyproject.toml:
```bash
uv sync
```
## Launch
You can set variables directly in the line
```bash
aid=<TG_API_ID> ahash="<TG_API_HASH>" ytoken="<YANDEX_OAUTH_TOKEN>" uv run python main.py
```
Or export them before a clean run
```bash
export aid=<TG_API_ID>
export ahash=<TG_API_HASH>
export ytoken=<YANDEX_OAUTH_TOKEN>
```