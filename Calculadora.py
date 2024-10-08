import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import json

import http.client

# import requests

# Função para adicionar o número ou operador na tela
def click_button(event):
    current_text = entry.get()
    new_text = current_text + str(event.widget["text"])
    entry.delete(0, tk.END)
    entry.insert(tk.END, new_text)

# Função para avaliar a expressão e mostrar o resultado
def evaluate_expression(event):
    expression = entry.get()
    try:
        result = str(eval(expression))
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Erro")

# Função para limpar a tela
def clear_entry(event):
    entry.delete(0, tk.END)

# Criando a janela principal
root = tk.Tk()
root.title("MORETTO LINDOOOOOO")

# Criando a entrada de texto onde os números e resultados aparecerão
entry = tk.Entry(root, width=16, font=("Arial", 24), borderwidth=2, relief="solid")
entry.grid(row=0, column=0, columnspan=4)

# Lista de botões da calculadora
buttons = [
    'M', 'O', 'R', 'E',
    'T', 'T', 'O', ' ',
    'L', 'I', 'N', 'D',
    'O', 'O', 'O', 'O'
]

# Adicionando os botões na interface
row = 1
col = 0
for button_text in buttons:
    button = tk.Button(root, text=button_text, font=("Arial", 18), width=4, height=2)
    button.grid(row=row, column=col, padx=5, pady=5)

    if button_text == "=":
        button.bind("<Button-1>", evaluate_expression)
    elif button_text == "C":
        button.bind("<Button-1>", clear_entry)
    else:
        button.bind("<Button-1>", click_button)

    col += 1
    if col > 3:
        col = 0
        row += 1

# Função para checar atualização usando a API do GitHub
def checar_atualizacao(version):
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
        tags = json.loads(data)
        
        if "tag_name" in tags:
            return tags["tag_name"]  # Pega a tag mais recente
        
        return None
    except Exception as e:
        print(f"Erro ao checar atualização: {e}")
        return None
    


if __name__ == "__main__":
    version = "v1.1"
    latest_version = checar_atualizacao(version)
    # latest_version.strip()
    print(f"Versão : {latest_version}")
    if latest_version != version:
        # pedir se quer atualizar
        resposta = messagebox.askyesno("Atualização Disponível", "Uma nova versão está disponível. Deseja atualizar agora?")
        if resposta:
            print("Atualizando...")
            path_atualizacao = os.path.abspath("atualizacao.exe")
            print(path_atualizacao)
            # path_atualizacao = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
            # subprocess.Popen([sys.executable, path_atualizacao], shell=True)
            subprocess.Popen([path_atualizacao], shell=True)
            # root.destroy()
            sys.exit(0)

        # print(f"Última versão disponível: {latest_version}")
        
    root.mainloop()
