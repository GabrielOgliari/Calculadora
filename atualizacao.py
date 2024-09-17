import sys
import os
import time
import shutil
import subprocess
import requests
import zipfile
import tkinter as tk

def main():
    # if len(sys.argv) < 2: # Verifica se o caminho do aplicativo foi fornecido
    #     print("Caminho do aplicativo não fornecido.")
    #     sys.exit(1)

    sys.argv.append("Calculadora.py") #
    
    app_path = sys.argv[1]
    app_dir = os.path.dirname(app_path)
    temp_dir = "update_temp"

    try:
        # Aguarda a aplicação principal fechar
        time.sleep(2)

        # Remove os arquivos antigos
        for filename in os.listdir(app_dir):
            file_path = os.path.join(app_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Falha ao remover {file_path}. {e}")

        # Move os novos arquivos para o diretório da aplicação
        for filename in os.listdir(temp_dir):
            src_path = os.path.join(temp_dir, filename)
            dest_path = os.path.join(app_dir, filename)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
            else:
                shutil.move(src_path, dest_path)
        
        # Remove o arquivo zip e a pasta temporária
        shutil.rmtree(temp_dir)
        if os.path.exists("update.zip"):
            os.remove("update.zip")

        # Reinicia a aplicação
        subprocess.Popen([sys.executable, app_path], shell=True)
    except Exception as e:
        print(f"Erro durante a atualização: {e}")


def baixar_e_atualizar(download_url):
    try:
        # Baixa o arquivo zip
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        with open("update.zip", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Extrai o zip para uma pasta temporária
        with zipfile.ZipFile("update.zip", 'r') as zip_ref:
            zip_ref.extractall("update_temp")
        
        # Executa o script de atualização
        updater_path = os.path.join("update_temp", "updater.py")
        if not os.path.exists(updater_path):
            tk.messagebox.showerror("Erro", "Script de atualização não encontrado.")
            return
        
        # Passa o caminho do aplicativo atual para o updater
        current_script = os.path.abspath(sys.argv[0])
        subprocess.Popen([sys.executable, updater_path, current_script], shell=True)
        # root.destroy()  # Fecha a aplicação atual
    except Exception as e:
        tk.messagebox.showerror("Erro", f"Falha ao atualizar: {e}")

def checar_atualizacao():
    url = "https://api.github.com/repos/GabrielOgliari/Calculadora/releases/latest"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve algum erro na requisição
        release_info = response.json()
        latest_version = release_info["tag_name"]
        download_url = None
        # Encontra o asset para download (assumindo que é um zip)
        for asset in release_info.get("assets", []):
            if asset["name"].endswith(".zip"):
                download_url = asset["browser_download_url"]
                break
        return latest_version, download_url
    except requests.exceptions.RequestException as e:
        print(f"Erro ao checar atualização: {e}")
        return None, None

if __name__ == "__main__":
    checar_atualizacao()
    main()
