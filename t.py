import requests
pbp = requests.get("https://statsapi.mlb.com/api/v1/game/40404/playByPlay").json()
for play in pbp['allPlays']:
    print(play)