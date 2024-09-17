import tkinter as tk
from atualizacao import Atualizacao


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

# Executando a janela principal
def is_update_available(APP_VERSION):
    latest_version = Atualizacao.get_latest_release_version()
    if latest_version and latest_version > APP_VERSION:
        print(f"Nova versão disponível: {latest_version}")
        return True
    else:
        print("Nenhuma atualização disponível.")
        return False


if __name__ == "__main__":
    APP_VERSION = 1.0
    if is_update_available(APP_VERSION):
        Atualizacao.download_update()
        Atualizacao.extract_update()
    root.mainloop()
