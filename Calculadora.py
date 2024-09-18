import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

import requests

# Função para adicionar o número ou operador na tela
def click_button(event):
    current_text = entry.get()
    new_text = current_text + str(event.widget["text"])
    entry.delete(0, tk.END)
    entry.insert(tk.END, new_text)

# Função para avaliar a expressão e mostrar o resultado
def evaluate_expression():
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
root.title("Calculadora")   

# Criando a entrada de texto onde os números e resultados aparecerão
entry = tk.Entry(root, width=16, font=("Arial", 24), borderwidth=2, relief="solid")
entry.grid(row=0, column=0, columnspan=4)

# Lista de botões da calculadora
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    'C', '0', '=', '+'
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
    url = "https://api.github.com/repos/GabrielOgliari/Calculadora/tags"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve algum erro na requisição
        tags = response.json()
        if tags:
            return tags[0]["name"]  # Pega a tag mais recente
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao checar atualização: {e}")
        return None
    


if __name__ == "__main__":
    version = "v1.0"
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
            subprocess.Popen([sys.executable, path_atualizacao], shell=True)
            # root.destroy()
            sys.exit(0)

        # print(f"Última versão disponível: {latest_version}")
        
    else:
        print("Não foi possível checar a atualização.")
    root.mainloop()
