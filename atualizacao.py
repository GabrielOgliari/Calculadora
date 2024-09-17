import os
import sys
import time
import urllib.request


import subprocess
from zipfile import ZipFile

class Atualizador:
    UPDATE_ZIP_URL = "https://meu-servidor.com/app_update.zip"
    UPDATE_PATH = "update.zip"
    EXTRACT_PATH = "./"

    def download_update(self):
        try:
            with urllib.request.urlopen(self.UPDATE_ZIP_URL) as response:
                with open(self.UPDATE_PATH, 'wb') as out_file:
                    out_file.write(response.read())
            print(f"Update baixado com sucesso em: {self.UPDATE_PATH}")
        except Exception as e:
            print("Erro ao baixar atualização:", e)

    def extract_update(self):
        try:
            with ZipFile(self.UPDATE_PATH, 'r') as zip_ref:
                zip_ref.extractall(self.EXTRACT_PATH)
            print(f"Atualização extraída para: {self.EXTRACT_PATH}")
        except Exception as e:
            print("Erro ao extrair a atualização:", e)
        finally:
            if os.path.exists(self.UPDATE_PATH):
                os.remove(self.UPDATE_PATH)
                print(f"Arquivo {self.UPDATE_PATH} removido após extração.")

    def restart_app(self):
        print("Reiniciando a aplicação...")
        python = sys.executable
        subprocess.Popen([python, "app.py"])
        sys.exit()

    def run(self):
        print("Esperando a aplicação principal fechar...")
        time.sleep(3)  # Dá tempo para a aplicação principal fechar completamente
        self.download_update()
        self.extract_update()
        self.restart_app()

if __name__ == "__main__":
    atualizador = Atualizador()
    atualizador.run()
