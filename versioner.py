import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from downloader import download_file

BASE_DIR = os.path.join("data", ".minecraft")
VERSIONS_DIR = os.path.join(BASE_DIR, "versions")
LIBRARIES_DIR = os.path.join(BASE_DIR, "libraries")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

VERSION_MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

def is_version_installed(version_id):
    jar_path = os.path.join(VERSIONS_DIR, version_id, f"{version_id}.jar")
    json_path = os.path.join(VERSIONS_DIR, version_id, f"{version_id}.json")
    return os.path.exists(jar_path) and os.path.exists(json_path)

def get_available_versions(limit=10):
    response = requests.get(VERSION_MANIFEST_URL)
    response.raise_for_status()
    data = response.json()
    versions = [v["id"] for v in data["versions"] if v["type"] == "release"]
    return versions[:limit]

def download_many(files, max_threads=10):
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(download_file, url, path) for url, path in files]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"[!] Erro em download paralelo: {e}")

def download_version(version_id):
    manifest = requests.get(VERSION_MANIFEST_URL).json()
    version_data = next(v for v in manifest["versions"] if v["id"] == version_id)
    version_url = version_data["url"]

    version_json = requests.get(version_url).json()

    version_dir = os.path.join(VERSIONS_DIR, version_id)
    os.makedirs(version_dir, exist_ok=True)
    version_json_path = os.path.join(version_dir, f"{version_id}.json")
    with open(version_json_path, "w") as f:
        json.dump(version_json, f, indent=2)

    client_jar_url = version_json["downloads"]["client"]["url"]
    client_jar_path = os.path.join(version_dir, f"{version_id}.jar")
    download_file(client_jar_url, client_jar_path)

    lib_files = []
    for lib in version_json["libraries"]:
        if "downloads" not in lib or "artifact" not in lib["downloads"]:
            continue
        artifact = lib["downloads"]["artifact"]
        lib_path = os.path.join(LIBRARIES_DIR, artifact["path"])
        lib_files.append((artifact["url"], lib_path))
    download_many(lib_files)

    assets_index = version_json["assets"]
    asset_index_url = version_json["assetIndex"]["url"]
    asset_index_path = os.path.join(ASSETS_DIR, "indexes", f"{assets_index}.json")
    download_file(asset_index_url, asset_index_path)

    with open(asset_index_path, 'r') as f:
        index_data = json.load(f)
        asset_files = []
        for asset, data in index_data["objects"].items():
            hash_val = data["hash"]
            subdir = hash_val[:2]
            asset_url = f"https://resources.download.minecraft.net/{subdir}/{hash_val}"
            asset_path = os.path.join(ASSETS_DIR, "objects", subdir, hash_val)
            asset_files.append((asset_url, asset_path))
        download_many(asset_files)
