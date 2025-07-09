import time
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

MODS_FILE = "monitored_mods.json"
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
CHECK_INTERVAL = 10  # seconds

if not DISCORD_WEBHOOK:
    raise ValueError("DISCORD_WEBHOOK is not set in .env file")

alerted_versions = set()

def check_mod_version(mod_id, mc_version):
    url = f"https://api.modrinth.com/v2/project/{mod_id}/version"
    try:
        response = requests.get(url)
        response.raise_for_status()
        for version in response.json():
            game_versions = version.get("game_versions", [])
            loaders = version.get("loaders", [])

            # Check for desired Minecraft version and 'fabric' loader
            if mc_version in game_versions and "fabric" in loaders:
                return version["version_number"], game_versions
    except requests.RequestException as e:
        print(f"Error fetching from Modrinth for {mod_id}: {e}")
    return None, None

def notify_discord(mod_id, version, game_versions):
    content = (
        f"✅ `{mod_id}`-`{version}` is available for Minecraft "
        f"`{', '.join(game_versions)}` on Modrinth (Fabric)!"
    )
    try:
        response = requests.post(DISCORD_WEBHOOK, json={"content": content})
        response.raise_for_status()
        print(f"Notified: {content}")
    except requests.RequestException as e:
        print(f"Error sending Discord message: {e}")

def monitor_loop():
    while True:
        if not os.path.exists(MODS_FILE):
            print("No mods file found.")
            time.sleep(CHECK_INTERVAL)
            continue

        try:
            with open(MODS_FILE) as f:
                mods = json.load(f)
        except json.JSONDecodeError:
            print("Invalid JSON format in monitored_mods.json")
            time.sleep(CHECK_INTERVAL)
            continue

        for mod in mods:
            mod_id = mod.get("mod_id")
            mc_version = mod.get("minecraft_version")
            if not mod_id or not mc_version:
                continue

            key = f"{mod_id}:{mc_version}"
            if key in alerted_versions:
                continue

            version_number, game_versions = check_mod_version(mod_id, mc_version)
            if version_number:
                notify_discord(mod_id, version_number, game_versions)
                alerted_versions.add(key)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_loop()
