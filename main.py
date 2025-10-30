import os, time, random, string, json
import websocket
from pyrogram import Client as Zdarova
from yandex_music import Client
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

from dotenv import load_dotenv
load_dotenv()

console = Console()

def getCurrentTrack(yaToken: str) -> dict:
    def getImgUri(cover_uri: str) -> str:
        return f"https://{cover_uri[:-2]}1000x1000" if cover_uri else ""
    def getTrackInfo(client: Client, trackId: int) -> dict:
        track = client.tracks([trackId])[0]
        duration = track.duration_ms // 1000
        return {
            "trackId": int(track.track_id.split(":")[0]) if track.track_id.split(":")[0].isdigit() else track.track_id,
            "title": track.title,
            "artist": ", ".join(track.artists_name()),
            "img": getImgUri(track.cover_uri),
            "duration": duration,
            "minutes": duration // 60,
            "seconds": duration % 60,
        }

    client = Client(yaToken).init()
    deviceId = "".join(random.choices(string.ascii_lowercase, k=16))
    wsProto = {"Ynison-Device-Id": deviceId, "Ynison-Device-Info": json.dumps({"app_name": "Chrome","type":1})}

    ws = websocket.WebSocket()
    ws.connect(
        "wss://ynison.music.yandex.ru/redirector.YnisonRedirectService/GetRedirectToYnison",
        header={
            "Sec-WebSocket-Protocol": f"Bearer, v2, {json.dumps(wsProto)}",
            "Origin": "http://music.yandex.ru",
            "Authorization": f"OAuth {yaToken}",
        },
    )
    data = json.loads(ws.recv())
    ws.close()

    wsProto["Ynison-Redirect-Ticket"] = data["redirect_ticket"]

    payload = {
        "update_full_state": {
            "player_state": {
                "player_queue": {
                    "current_playable_index": -1,
                    "entity_id": "",
                    "entity_type": "VARIOUS",
                    "playable_list": [],
                    "options": {"repeat_mode": "NONE"},
                    "entity_context": "BASED_ON_ENTITY_BY_DEFAULT",
                    "version": {"device_id": deviceId,"version":9021243204784341000,"timestamp_ms":0},
                    "from_optional": "",
                },
                "status": {
                    "duration_ms": 0,
                    "paused": True,
                    "playback_speed": 1,
                    "progress_ms": 0,
                    "version": {"device_id": deviceId,"version":8321822175199937000,"timestamp_ms":0},
                },
            },
            "device": {
                "capabilities": {"can_be_player": True,"can_be_remote_controller": False,"volume_granularity":16},
                "info": {"device_id": deviceId,"type":"WEB","title":"Chrome Browser","app_name":"Chrome"},
                "volume_info": {"volume":0},
                "is_shadow": True,
            },
            "is_currently_active": False,
        },
        "rid":"ac281c26-a047-4419-ad00-e4fbfda1cba3",
        "player_action_timestamp_ms":0,
        "activity_interception_type":"DO_NOT_INTERCEPT_BY_DEFAULT",
    }

    ws = websocket.WebSocket()
    ws.connect(
        f"wss://{data['host']}/ynison_state.YnisonStateService/PutYnisonState",
        header={
            "Sec-WebSocket-Protocol": f"Bearer, v2, {json.dumps(wsProto)}",
            "Origin": "http://music.yandex.ru",
            "Authorization": f"OAuth {yaToken}",
        },
    )
    ws.send(json.dumps(payload))
    ynison = json.loads(ws.recv())
    ws.close()

    track = ynison["player_state"]["player_queue"]["playable_list"][ynison["player_state"]["player_queue"]["current_playable_index"]]

    return {
        "paused": ynison["player_state"]["status"]["paused"],
        "progress_ms": ynison["player_state"]["status"]["progress_ms"],
        "track": getTrackInfo(client, track["playable_id"]),
    }

def initialization():
    account = Zdarova("account", api_id=os.getenv("aid"), api_hash=os.getenv("ahash"))
    token = os.getenv("ytoken")
    ym = Client(token).init()
    lastTrackId = None

    with open("logo.txt", "r", encoding="ascii") as fuck:
        header = fuck.read()

    console.print(header, style="bold green", justify="center")
    console.print('Managing the "Now Playing" module in Telegram', style="bold green", justify="center")
    console.print("Developer: @nedefined $ Thanks to: mipoh.ru\n", style="bold yellow", justify="center")

    while True:
        with account:
            console.print("* 1/5 - Obtaining redirect ticket", style="bold cyan")
            trackInfo = getCurrentTrack(token)
            console.print("* 2/5 - Getting the player's state", style="bold cyan")

            trackObj = trackInfo["track"]
            trackId = trackObj["trackId"]
            if trackId == lastTrackId:
                console.print(f"Track {trackId} is already set, skipping...", style="bold magenta")
                time.sleep(30)
                continue

            lastTrackId = trackId

            filename = f"{trackObj['title']} - {trackObj['artist']}.mp3"
            filename = "".join(c for c in filename if c not in '<>:"/\\|?*')

            console.print(f"* 3/5 - Track ID received: [bold magenta]{trackId}", style="bold cyan")
            console.print(f"* 4/5 - Downloading: [bold magenta]{filename}", style="bold cyan")

            track = ym.tracks([int(trackId)])[0]
            with Progress(
                TextColumn("[progress.description]{task.description}", style="bold green"),
                BarColumn(bar_width=None, style="green"),
                TextColumn("{task.percentage:>3.0f}%", style="bold yellow"),
                TimeRemainingColumn(),
                console=console
            ) as progress:
                task = progress.add_task("Downloading", total=100)
                track.download(filename=filename, codec="mp3", bitrate_in_kbps=192)
                progress.update(task, advance=100)

            console.print("* 5/5 - Telegram profile updating", style="bold cyan")
            try:
                account.remove_profile_audio(account.me.first_profile_audio.file_id)
            except:
                pass
            account.add_profile_audio(filename)
            console.print("Profile updated. Waiting 320 seconds...\n", style="bold green")
        time.sleep(320)

if __name__ == "__main__":
    initialization()
