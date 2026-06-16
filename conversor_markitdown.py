"""
Conversor de arquivos para Markdown usando a biblioteca MarkItDown.
Interface gráfica feita com tkinter.

Instalação da dependência:
    pip install 'markitdown[all]'
"""
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from markitdown import MarkItDown


class ConversorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor MarkItDown")
        self.root.geometry("600x320")
        self.root.resizable(False, False)

        self.arquivo_entrada = tk.StringVar()
        self.pasta_saida = tk.StringVar()

        self._montar_interface()

    def _montar_interface(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Conversor de arquivos para Markdown",
            font=("Segoe UI", 14, "bold"),
        ).grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w")

        ttk.Label(frame, text="Arquivo:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(frame, textvariable=self.arquivo_entrada, width=50).grid(
            row=1, column=1, padx=5, pady=5
        )
        ttk.Button(frame, text="Selecionar...", command=self.selecionar_arquivo).grid(
            row=1, column=2, pady=5
        )

        ttk.Label(frame, text="Salvar em:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(frame, textvariable=self.pasta_saida, width=50).grid(
            row=2, column=1, padx=5, pady=5
        )
        ttk.Button(frame, text="Selecionar...", command=self.selecionar_pasta).grid(
            row=2, column=2, pady=5
        )

        self.btn_converter = ttk.Button(
            frame, text="Converter", command=self.iniciar_conversao
        )
        self.btn_converter.grid(row=3, column=0, columnspan=3, pady=20)

        self.status = ttk.Label(frame, text="", foreground="gray")
        self.status.grid(row=4, column=0, columnspan=3, sticky="w")

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo para converter",
            filetypes=[
                ("Todos suportados", "*.pdf *.docx *.pptx *.xlsx *.html *.csv *.json *.xml *.txt *.jpg *.png *.mp3 *.wav"),
                ("Todos os arquivos", "*.*"),
            ],
        )
        if caminho:
            self.arquivo_entrada.set(caminho)
            if not self.pasta_saida.get():
                self.pasta_saida.set(os.path.dirname(caminho))

    def selecionar_pasta(self):
        caminho = filedialog.askdirectory(title="Selecione a pasta para salvar")
        if caminho:
            self.pasta_saida.set(caminho)

    def iniciar_conversao(self):
        arquivo = self.arquivo_entrada.get().strip()
        pasta = self.pasta_saida.get().strip()

        if not arquivo:
            messagebox.showwarning("Atenção", "Selecione um arquivo para converter.")
            return
        if not os.path.isfile(arquivo):
            messagebox.showerror("Erro", "O arquivo selecionado não existe.")
            return
        if not pasta:
            messagebox.showwarning("Atenção", "Selecione a pasta de destino.")
            return
        if not os.path.isdir(pasta):
            messagebox.showerror("Erro", "A pasta de destino não existe.")
            return

        self.btn_converter.config(state="disabled")
        self.status.config(text="Convertendo...", foreground="blue")
        threading.Thread(
            target=self._converter, args=(arquivo, pasta), daemon=True
        ).start()

    def _converter(self, arquivo, pasta):
        try:
            md = MarkItDown()
            resultado = md.convert(arquivo)

            nome_base = os.path.splitext(os.path.basename(arquivo))[0]
            caminho_saida = os.path.join(pasta, f"{nome_base}.md")

            with open(caminho_saida, "w", encoding="utf-8") as f:
                f.write(resultado.text_content)

            self.root.after(0, self._sucesso, caminho_saida)
        except Exception as e:
            self.root.after(0, self._erro, str(e))

    def _sucesso(self, caminho_saida):
        self.status.config(text=f"Salvo em: {caminho_saida}", foreground="green")
        self.btn_converter.config(state="normal")
        messagebox.showinfo("Concluído", f"Arquivo convertido com sucesso!\n\n{caminho_saida}")

    def _erro(self, mensagem):
        self.status.config(text="Erro na conversão.", foreground="red")
        self.btn_converter.config(state="normal")
        messagebox.showerror("Erro", f"Falha ao converter o arquivo:\n\n{mensagem}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ConversorApp(root)
    root.mainloop()
