import tkinter as tk
from tkinter import filedialog, messagebox
from parser import parse_pubmed
import traceback


def selecionar_arquivo():
    caminho = filedialog.askopenfilename(
        filetypes=[("Arquivos XML", "*.xml"), ("Arquivos GZ", "*.gz")]
    )
    if caminho:
        caminho_var.set(caminho)


def processar():
    caminho = caminho_var.get()
    if not caminho:
        messagebox.showwarning("Aviso", "Por favor, selecione um arquivo para processar.")
        return

    # Perguntar onde salvar o CSV
    output_caminho = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Arquivo CSV", "*.csv")],
        title="Salvar arquivo CSV como"
    )

    if not output_caminho:
        messagebox.showwarning("Aviso", "Seleção de local de salvamento cancelada.")
        return

    try:
        parse_pubmed(caminho, output_caminho)
        messagebox.showinfo("Sucesso", f"Processamento concluído!\nArquivo salvo em:\n{output_caminho}")
        print(f"CSV salvo em: {output_caminho}")
    except Exception as e:
        print("Erro durante o processamento:")
        traceback.print_exc()  # <-- Mostra o erro completo no terminal
        messagebox.showerror("Erro", f"Ocorreu um erro durante o processamento:\n{str(e)}")


# ---------- Interface Tkinter ----------

janela = tk.Tk()
janela.title("Parser de Artigos PubMed")
janela.geometry("600x200")
janela.resizable(False, False)

# Label
label = tk.Label(janela, text="Selecione um arquivo XML ou GZ:")
label.pack(pady=10)

# Entrada de texto para o caminho do arquivo
caminho_var = tk.StringVar()
entrada = tk.Entry(janela, textvariable=caminho_var, width=70)
entrada.pack(padx=10)

# Botões
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

btn_selecionar = tk.Button(frame_botoes, text="Selecionar Arquivo", command=selecionar_arquivo)
btn_selecionar.pack(side=tk.LEFT, padx=10)

btn_processar = tk.Button(frame_botoes, text="Processar", command=processar)
btn_processar.pack(side=tk.LEFT, padx=10)

# Inicia a janela
janela.mainloop()
