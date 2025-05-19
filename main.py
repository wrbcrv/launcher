import os
import json
from versioner import get_available_versions, download_version
from launcher import launch_game

VERSIONS_DIR = os.path.join(".minecraft", "versions")
CONFIG_PATH = os.path.join("config.json")

os.makedirs(os.path.join(".minecraft", "versions"), exist_ok=True)
os.makedirs(os.path.join(".minecraft", "libraries"), exist_ok=True)
os.makedirs(os.path.join(".minecraft", "assets", "indexes"), exist_ok=True)
os.makedirs(os.path.join(".minecraft", "assets", "objects"), exist_ok=True)

def get_installed_versions():
    if not os.path.exists(VERSIONS_DIR):
        return []
    versions = []
    for version in os.listdir(VERSIONS_DIR):
        jar = os.path.join(VERSIONS_DIR, version, f"{version}.jar")
        json_file = os.path.join(VERSIONS_DIR, version, f"{version}.json")
        if os.path.isfile(jar) and os.path.isfile(json_file):
            versions.append(version)
    return versions

def load_username():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            data = json.load(f)
            if 'username' in data:
                return data['username']
    return None

def save_username(username):
    data = {'username': username}
    with open(CONFIG_PATH, 'w') as f:
        json.dump(data, f)

def prompt_for_username():
    username = input("Digite o nome de usuário: ")
    save_username(username)
    return username

def main():
    print("=== Minecraft Launcher (by Werbton) v1.0 ===")

    username = load_username()
    if not username:
        username = prompt_for_username()

    while True:
        installed_versions = get_installed_versions()
        available_versions = get_available_versions()

        print(f"\nUsuário atual: {username}")
        print("\nOpções:")
        print("1. Listar versões instaladas")
        print("2. Baixar nova versão")
        print("3. Iniciar jogo com versão instalada")
        print("4. Alterar nome de usuário")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("Versões instaladas:")
            for v in installed_versions:
                print(" -", v)

        elif opcao == "2":
            print("Versões disponíveis:")
            for idx, v in enumerate(available_versions):
                print(f"{idx+1}. {v}")
            print("0. Voltar")
            escolha = input("Digite o número da versão para baixar ou 0 para voltar: ")
            if escolha == "0":
                continue
            try:
                idx = int(escolha) - 1
                if 0 <= idx < len(available_versions):
                    download_version(available_versions[idx])
                    print(f"Versão {available_versions[idx]} baixada com sucesso!")
                else:
                    print("Índice inválido.")
            except Exception as e:
                print("Erro ao baixar versão:", e)

        elif opcao == "3":
            print("Versões instaladas:")
            for idx, v in enumerate(installed_versions):
                print(f"{idx+1}. {v}")
            print("0. Voltar")
            escolha = input("Digite o número da versão para iniciar ou 0 para voltar: ")
            if escolha == "0":
                continue
            try:
                idx = int(escolha) - 1
                if 0 <= idx < len(installed_versions):
                    launch_game(username, installed_versions[idx])
                else:
                    print("Índice inválido.")
            except Exception as e:
                print("Erro ao iniciar o jogo:", e)

        elif opcao == "4":
            username = prompt_for_username()
            print("Nome de usuário atualizado.")

        elif opcao == "5":
            print("Saindo do launcher.")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
