import os
import sys
import time
import subprocess

from zipfile import ZipFile

UPDATE_ZIP_URL = "<https://meu-servidor.com/app_update.zip>"
UPDATE_PATH = "update.zip"
EXTRACT_PATH = "./"

def download_update():
    try:
        response = subprocess.get(UPDATE_ZIP_URL)
        with open(UPDATE_PATH, 'wb') as file:
            file.write(response.content)
        print(f"Update baixado com sucesso em: {UPDATE_PATH}")
    except Exception as e:
        print("Erro ao baixar atualização:", e)

def extract_update():
    try:
        with ZipFile(UPDATE_PATH, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_PATH)
        print(f"Atualização extraída para: {EXTRACT_PATH}")
    except Exception as e:
        print("Erro ao extrair a atualização:", e)

def restart_app():
    print("Reiniciando a aplicação...")
    python = sys.executable
    subprocess.Popen([python, "app.py"])
    sys.exit()

if __name__ == "__main__":
    print("Esperando a aplicação principal fechar...")
    time.sleep(3)  # Dá tempo para a aplicação principal fechar completamente
    download_update()
    extract_update()
    restart_app()
