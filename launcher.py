import os
import subprocess
import json
import platform
import requests

BASE_DIR = os.path.join(".minecraft")
VERSIONS_DIR = os.path.join(BASE_DIR, "versions")
LIBRARIES_DIR = os.path.join(BASE_DIR, "libraries")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def build_classpath(version_json):
    cp = []
    for lib in version_json["libraries"]:
        if "downloads" in lib and "artifact" in lib["downloads"]:
            path = lib["downloads"]["artifact"]["path"]
            cp.append(os.path.join(LIBRARIES_DIR, path))
    cp.append(os.path.join(VERSIONS_DIR, version_json["id"], f"{version_json['id']}.jar"))
    sep = ";" if platform.system() == "Windows" else ":"
    return sep.join(cp)

def launch_game(username, version_id):
    version_path = os.path.join(VERSIONS_DIR, version_id, f"{version_id}.json")

    if not os.path.exists(version_path):
        print("Versão não encontrada. Certifique-se de ter baixado primeiro.")
        return

    with open(version_path, "r") as f:
        version_json = json.load(f)

    classpath = build_classpath(version_json)
    main_class = version_json["mainClass"]
    asset_index = version_json["assets"]
    assets_root = ASSETS_DIR
    assets_index_path = os.path.join(ASSETS_DIR, "indexes", f"{asset_index}.json")

    command = [
        "java",
        "-Xmx2G",
        f"-Djava.library.path={BASE_DIR}/natives",
        "-cp", classpath,
        main_class,
        "--username", username,
        "--version", version_id,
        "--gameDir", BASE_DIR,
        "--assetsDir", assets_root,
        "--assetIndex", asset_index,
        "--versionType", "release",
        "--accessToken", "offline",  
        "--userType", "legacy",    
        "--uuid", "00000000-0000-0000-0000-000000000000" 
    ]

    print("Executando o Minecraft...")
    subprocess.run(command)

def get_version_metadata_url(version_id):
    manifest = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
    version_data = next(v for v in manifest["versions"] if v["id"] == version_id)
    return version_data["url"]
