import sys
import os
import time
import shutil
import subprocess
import zipfile
import http.client
import json
from urllib.parse import urlparse

def main(app_path):
    app_dir = os.path.dirname(app_path)
    temp_dir = "update_temp"

    try:
        # Aguarda a aplicação principal fechar
        time.sleep(2)

        # Verifica se o diretório da aplicação existe
        if not os.path.exists(app_dir):
            print(f"Diretório da aplicação não encontrado: {app_dir}")
            return

        # Remove os arquivos antigos, exceto o script atual
        for filename in os.listdir(app_dir):
            file_path = os.path.join(app_dir, filename)
            if filename != os.path.basename(__file__):  # Não remover o próprio script
                if filename == "update.zip" or filename == ".venv" or filename == ".gitignore" or filename == "update_temp" or filename == "atualizacao.exe":
                    continue
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Falha ao remover {file_path}. {e}")

        # Move os novos arquivos para o diretório da aplicação
        # for filename in os.listdir(temp_dir):
        # for filename in os.listdir(temp_dir):
        #     src_path = os.path.join(temp_dir, filename)
        #     dest_path = os.path.join(app_dir, filename)
        #     if os.path.isdir(src_path):
        #         shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        #     else:
        #         shutil.move(src_path, dest_path)
        mover_arquivos_para_app_dir(temp_dir, app_dir)
        
        # Remove o arquivo zip e a pasta temporária
        shutil.rmtree(temp_dir)
        if os.path.exists("update.zip"):
            os.remove("update.zip")

        # Reinicia a aplicação
        subprocess.Popen([app_path], shell=True)
        sys.exit(0)
    except Exception as e:
        print(f"Erro durante a atualização: {e}")

def mover_arquivos_para_app_dir(temp_dir, app_dir):
    try:
        # Procura pela subpasta dentro de update_temp
        subpasta = os.listdir(temp_dir)[0]  # Supondo que há uma única subpasta dentro de update_temp
        subpasta_path = os.path.join(temp_dir, subpasta)

        # Verifica se a subpasta é um diretório válido
        if not os.path.isdir(subpasta_path):
            print(f"Erro: {subpasta_path} não é um diretório.")
            return

        # Move os arquivos da subpasta para o diretório da aplicação
        for filename in os.listdir(subpasta_path):
            src_path = os.path.join(subpasta_path, filename)
            dest_path = os.path.join(app_dir, filename)

            # Ignora o script atual e a pasta temporária
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
            else:
                shutil.move(src_path, dest_path)

        print("Arquivos movidos com sucesso.")
    except Exception as e:
        print(f"Erro ao mover arquivos: {e}")

# def baixar_e_atualizar(download_url):
#     try:
#         # Baixa o arquivo zip
#         response = requests.get(download_url, stream=True)
#         response.raise_for_status()
#         with open("update.zip", "wb") as f:
#             for chunk in response.iter_content(chunk_size=8192):
#                 f.write(chunk)
        
#         # Extrai o zip para uma pasta temporária
#         with zipfile.ZipFile("update.zip", 'r') as zip_ref:
#             zip_ref.extractall("update_temp")
        
#         print("Download e extração concluídos. Pronto para atualizar.")
#     except Exception as e:
#         print(f"Falha ao baixar e atualizar: {e}")
#         return False
#     return True

def baixar_e_atualizar(download_url):
    try:
        # Realiza o parse da URL inicial
        parsed_url = urlparse(download_url)
        host = parsed_url.netloc
        path = parsed_url.path

        # Faz a conexão e requisição do arquivo com cabeçalho User-Agent
        conn = http.client.HTTPSConnection(host)
        headers = {
            "User-Agent": "Mozilla/5.0"  # Cabeçalho para evitar bloqueio
        }
        conn.request("GET", path, headers=headers)
        response = conn.getresponse()
        
        # Se houver redirecionamento (302), faz nova requisição
        if response.status == 302:
            location = response.getheader('Location')
            if not location.startswith('http'):
                # Se a nova URL for relativa, concatena o host original
                location = f"https://{host}{location}"
            print(f"Redirecionado para {location}")
            return baixar_e_atualizar(location)  # Chama a função recursivamente para baixar o novo arquivo
        
        if response.status != 200:
            print(f"Erro ao baixar o arquivo: {response.status} {response.reason}")
            return False

        # Salva o conteúdo em um arquivo temporário
        with open("update.zip", "wb") as f:
            shutil.copyfileobj(response, f)

        # Extrai o zip para uma pasta temporária
        with zipfile.ZipFile("update.zip", 'r') as zip_ref:
            zip_ref.extractall("update_temp")
        
        print("Download e extração concluídos. Pronto para atualizar.")
    except Exception as e:
        print(f"Falha ao baixar e atualizar: {e}")
        return False
    return True

def checar_atualizacao():
    url = "/repos/GabrielOgliari/Calculadora/releases/latest"
    try:
        conn = http.client.HTTPSConnection("api.github.com")
        headers = {
            "User-Agent": "Mozilla/5.0"  # Cabeçalho necessário para acessar a API do GitHub
        }
        conn.request("GET", url, headers=headers)
        response = conn.getresponse()
        
        if response.status != 200:
            print(f"Erro ao checar atualização: {response.status} {response.reason}")
            return None
        
        data = response.read()
        release_info = json.loads(data)
        print(f"Resposta da API: {release_info}")  # Imprimir toda a resposta da API para análise

        latest_version = release_info["tag_name"]
        print(f"Versão mais recente: {latest_version}")

        # Usa o campo zipball_url para baixar o código-fonte como um zip
        download_url = release_info.get("zipball_url")
        print(f"URL para download: {download_url}")

        return latest_version, download_url
    except Exception as e:
        print(f"Erro ao checar atualização: {e}")
        return None, None

if __name__ == "__main__":
    # Checa por atualizações
    latest_version, download_url = checar_atualizacao()
    
    if latest_version and download_url:
        # Baixa e prepara a atualização
        sucesso = baixar_e_atualizar(download_url)
        
        if sucesso:
            app_path = os.path.abspath("Calculadora.exe")  # O caminho do script da aplicação
            main(app_path)  # Inicia o processo de atualização
        else:
            print("Falha ao baixar ou extrair a atualização.")
    else:
        print("Nenhuma atualização disponível ou erro ao checar atualizações.")
