from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
MODS_FILE = "monitored_mods.json"

if not os.path.exists(MODS_FILE):
    with open(MODS_FILE, "w") as f:
        json.dump([], f)

@app.route('/add', methods=['POST'])
def add_mod():
    data = request.json
    mod_id = data.get("mod_id")
    mc_version = data.get("minecraft_version")

    with open(MODS_FILE, "r+") as f:
        mods = json.load(f)
        mods.append({"mod_id": mod_id, "minecraft_version": mc_version})
        f.seek(0)
        json.dump(mods, f, indent=2)

    return jsonify({"message": "Mod added to monitoring list"}), 201

@app.route('/remove', methods=['POST'])
def remove_mod():
    data = request.json
    mod_id = data.get("mod_id")
    mc_version = data.get("minecraft_version")

    try:
        with open(MODS_FILE, "r") as f:
            mods = json.load(f)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format in mods file"}), 500

    # Filter out the matching entry
    mods = [
        mod for mod in mods
        if not (mod.get("mod_id") == mod_id and mod.get("minecraft_version") == mc_version)
    ]

    with open(MODS_FILE, "w") as f:
        json.dump(mods, f, indent=2)

    return jsonify({"message": f"Removed {mod_id}-{mc_version} from watch list."}), 200

@app.route('/list', methods=['GET'])
def list_mods():
    allowed_keys = {"minecraft_version"}
    provided_keys = set(request.args.keys())

    # If any disallowed query parameter is passed
    if not provided_keys.issubset(allowed_keys):
        return jsonify({"error": "Only 'minecraft_version' filtering is allowed."}), 403

    version_filter = request.args.get("minecraft_version")

    try:
        with open(MODS_FILE, "r") as f:
            mods = json.load(f)
    except Exception as e:
        return jsonify({"error": f"Could not read mod list: {str(e)}"}), 500

    if version_filter:
        filtered_mods = [m for m in mods if m.get("minecraft_version") == version_filter]
        if not filtered_mods:
            return jsonify({"message": f"No mods found for version {version_filter}"}), 404
        return jsonify({"watch_list": filtered_mods}), 200

    # No filter: return full list
    return jsonify({"watch_list": mods}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
