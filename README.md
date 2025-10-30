# yalistening
**An open-source Yandex Music module for the Telegram messenger.** Built with Kurigram, Yandex Music API, WebSocket, Rich, and managed via UV.

## Installation

```
git clone https://github.com/nedefined/yalistening
cd yalistening
```

I recommend using the [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager. Pull and install all dependencies from pyproject.toml:
```bash
uv sync
```

## Configuring
Three environment variables are required for the script to work

### Telegram API: https://my.telegram.org/apps

1. Go to [my.telegram.org](https://my.telegram.org) and log in to your account.

2. Open the "API development tools" section.

3. Create a new application

4. On the page that opens, you will see and copy the app_api_id **(this is the `aid`)** and app_api_hash **(this is the `ahash`)**

### Yandex Music API: https://yandex-music.readthedocs.io/en/main/token.html

1. (Optional) Open DevTools in your browser and enable throttling in the Network tab.

2. Follow the link https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d

3. Authorise if necessary and grant access

4. The browser will redirect you to an address like `https://music.yandex.ru/#access_token=y0_...`, just copy it

## Launch
You can set variables directly in the line
```bash
aid=<TG_API_ID> ahash=<TG_API_HASH> ytoken=<YANDEX_OAUTH_TOKEN> uv run python main.py
```
Or export them before a clean run
```bash
export aid=<TG_API_ID>
export ahash=<TG_API_HASH>
export ytoken=<YANDEX_OAUTH_TOKEN>
```
Or create a .env file:
```
aid=<TG_API_ID>
ahash=<TG_API_HASH>
ytoken=<YANDEX_OAUTH_TOKEN>
```