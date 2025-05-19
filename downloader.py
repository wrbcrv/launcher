import os
import time
import requests
from tqdm import tqdm

def download_file(url, path, retries=3, delay=3):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if os.path.exists(path):
        print(f"[✓] Já existe: {os.path.basename(path)}")
        return

    for attempt in range(1, retries + 1):
        try:
            print(f"[→] Baixando: {os.path.basename(path)} (Tentativa {attempt}/{retries})")
            response = requests.get(url, stream=True, timeout=15)
            response.raise_for_status()

            total = int(response.headers.get('content-length', 0))
            with open(path, "wb") as file, tqdm(
                total=total, unit='B', unit_scale=True, desc=os.path.basename(path)
            ) as bar:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
                    bar.update(len(chunk))
            return

        except requests.exceptions.RequestException as e:
            print(f"[!] Erro: {e}")
            if attempt < retries:
                print(f"↻ Tentando novamente em {delay} segundos...")
                time.sleep(delay)
            else:
                print(f"[✗] Falha ao baixar {url} após {retries} tentativas.")
                raise
