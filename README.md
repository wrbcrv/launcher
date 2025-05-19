# Minecraft CLI Launcher

Este projeto é uma launcher de Minecraft em modo linha de comando (CLI), com foco em simplicidade, privacidade e liberdade do usuário.

## Funcionalidades
- Instala e gerencia versões oficiais do Minecraft usando a API da Mojang.
- Executa o jogo em modo offline, sem necessidade de login.
- Permite configurar o nome de usuário e escolher a versão a ser executada.
- Faz download de arquivos com verificação, múltiplas tentativas e barra de progresso.
- Código aberto, sem rastreamento, anúncios ou componentes ocultos.

## Por que usar esta launcher
Diferente da maioria das launchers disponíveis na internet, este projeto não coleta dados, não exibe propagandas e não inclui spyware. Tudo pode ser auditado diretamente no código.

## Estrutura do projeto
- `main.py`: interface principal com menu de opções.
- `versioner.py`: gerencia versões e realiza os downloads.
- `launcher.py`: monta os parâmetros e executa o jogo.
- `downloader.py`: responsável por baixar arquivos com segurança.

Este projeto é distribuído para fins educacionais e uso pessoal.

---

# Minecraft CLI Launcher (English)

This project is a command-line interface (CLI) Minecraft launcher focused on simplicity, privacy, and user freedom.

## Features
- Installs and manages official Minecraft versions using Mojang's API.
- Launches the game in offline mode with no login required.
- Allows setting the username and choosing the version to run.
- Downloads files with verification, retries, and progress bars.
- Open source code with no tracking, ads, or hidden components.

## Why use this launcher
Unlike most launchers available online, this one does not collect data, show ads, or include spyware. Everything can be verified in the source code.

## Project structure
- `main.py`: main interface with menu options.
- `versioner.py`: manages versions and handles downloads.
- `launcher.py`: builds parameters and launches the game.
- `downloader.py`: handles secure and reliable file downloads.

This project is distributed for educational and personal use.
