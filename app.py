import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog


conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    ano_publicacao INTEGER,
    genero TEXT,
    quantidade_estoque INTEGER
)
''')
conn.commit()


def cadastrar_livro():
    def salvar():
        titulo = titulo_entry.get().strip()
        autor = autor_entry.get().strip()
        ano = ano_entry.get().strip()
        genero = genero_entry.get().strip()
        quantidade = quantidade_entry.get().strip()

        if titulo and autor and ano.isdigit() and quantidade.isdigit():
            cursor.execute('''
            INSERT INTO livros (titulo, autor, ano_publicacao, genero, quantidade_estoque)
            VALUES (?, ?, ?, ?, ?)
            ''', (titulo, autor, int(ano), genero, int(quantidade)))
            conn.commit()
            messagebox.showinfo("Sucesso", "✅ Livro cadastrado com sucesso!")
            janela_cadastro.destroy()
        else:
            messagebox.showerror("Erro", "⚠️ Preencha todos os campos corretamente.")

    janela_cadastro = tk.Toplevel(root)
    janela_cadastro.title("Cadastrar Livro")

    tk.Label(janela_cadastro, text="Título:").grid(row=0, column=0, sticky="e")
    titulo_entry = tk.Entry(janela_cadastro)
    titulo_entry.grid(row=0, column=1)

    tk.Label(janela_cadastro, text="Autor:").grid(row=1, column=0, sticky="e")
    autor_entry = tk.Entry(janela_cadastro)
    autor_entry.grid(row=1, column=1)

    tk.Label(janela_cadastro, text="Ano de Publicação:").grid(row=2, column=0, sticky="e")
    ano_entry = tk.Entry(janela_cadastro)
    ano_entry.grid(row=2, column=1)

    tk.Label(janela_cadastro, text="Gênero:").grid(row=3, column=0, sticky="e")
    genero_entry = tk.Entry(janela_cadastro)
    genero_entry.grid(row=3, column=1)

    tk.Label(janela_cadastro, text="Quantidade em Estoque:").grid(row=4, column=0, sticky="e")
    quantidade_entry = tk.Entry(janela_cadastro)
    quantidade_entry.grid(row=4, column=1)

    tk.Button(janela_cadastro, text="Salvar", command=salvar).grid(row=5, column=0, columnspan=2, pady=10)


def listar_livros():
    janela_listagem = tk.Toplevel(root)
    janela_listagem.title("Lista de Livros")

    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()

    if livros:
        for i, livro in enumerate(livros):
            texto = (f"ID: {livro[0]} | Título: {livro[1]} | Autor: {livro[2]} | "
                     f"Ano: {livro[3]} | Gênero: {livro[4]} | Estoque: {livro[5]}")
            tk.Label(janela_listagem, text=texto, anchor='w', justify='left').grid(row=i, column=0, sticky="w")
    else:
        tk.Label(janela_listagem, text="📭 Nenhum livro cadastrado.").pack()


def atualizar_livro():
    id_livro = simpledialog.askinteger("Atualizar Livro", "Digite o ID do livro a ser atualizado:", parent=root)
    if id_livro:
        cursor.execute('SELECT * FROM livros WHERE id = ?', (id_livro,))
        if cursor.fetchone() is None:
            messagebox.showerror("Erro", "⚠️ Livro não encontrado.")
            return

        campo = simpledialog.askstring("Campo", "Qual campo deseja atualizar?\n"
                                         "(titulo, autor, ano_publicacao, genero, quantidade_estoque)", parent=root)
        if campo not in ['titulo', 'autor', 'ano_publicacao', 'genero', 'quantidade_estoque']:
            messagebox.showerror("Erro", "⚠️ Campo inválido.")
            return

        novo_valor = simpledialog.askstring("Novo Valor", f"Digite o novo valor para {campo}:", parent=root)
        if novo_valor is None:
            return

        try:
            if campo in ['ano_publicacao', 'quantidade_estoque']:
                novo_valor = int(novo_valor)
            cursor.execute(f'UPDATE livros SET {campo} = ? WHERE id = ?', (novo_valor, id_livro))
            conn.commit()
            messagebox.showinfo("Sucesso", "✅ Livro atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"⚠️ Erro ao atualizar: {e}")


def excluir_livro():
    id_livro = simpledialog.askinteger("Excluir Livro", "Digite o ID do livro a ser excluído:", parent=root)
    if id_livro:
        cursor.execute('SELECT * FROM livros WHERE id = ?', (id_livro,))
        if cursor.fetchone() is None:
            messagebox.showerror("Erro", "⚠️ Livro não encontrado.")
            return

        confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este livro?")
        if confirmacao:
            cursor.execute('DELETE FROM livros WHERE id = ?', (id_livro,))
            conn.commit()
            messagebox.showinfo("Sucesso", "🗑️ Livro excluído com sucesso!")



root = tk.Tk()
root.title("📚 Sistema de Cadastro de Livros (CRUD)")
root.geometry("400x300")

tk.Label(root, text="📚 Sistema de Cadastro de Livros", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="Cadastrar Livro", width=25, command=cadastrar_livro).pack(pady=5)
tk.Button(root, text="Listar Livros", width=25, command=listar_livros).pack(pady=5)
tk.Button(root, text="Atualizar Livro", width=25, command=atualizar_livro).pack(pady=5)
tk.Button(root, text="Excluir Livro", width=25, command=excluir_livro).pack(pady=5)
tk.Button(root, text="Sair", width=25, command=root.quit).pack(pady=20)

root.mainloop()

conn.close()