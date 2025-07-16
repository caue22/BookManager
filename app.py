import sqlite3

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
    print("\n=== Cadastrar Livro ===")
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    ano = input("Ano de Publicação: ").strip()
    genero = input("Gênero: ").strip()
    quantidade = input("Quantidade em Estoque: ").strip()

    if titulo and autor and ano.isdigit() and quantidade.isdigit():
        cursor.execute('''
        INSERT INTO livros (titulo, autor, ano_publicacao, genero, quantidade_estoque)
        VALUES (?, ?, ?, ?, ?)
        ''', (titulo, autor, int(ano), genero, int(quantidade)))
        conn.commit()
        print("✅ Livro cadastrado com sucesso!\n")
    else:
        print("⚠️ Preencha todos os campos corretamente.\n")

def listar_livros():
    print("\n=== Lista de Livros ===")
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()

    if livros:
        for livro in livros:
            print(f"ID: {livro[0]} | Título: {livro[1]} | Autor: {livro[2]} | "
                  f"Ano: {livro[3]} | Gênero: {livro[4]} | Estoque: {livro[5]}")
    else:
        print("📭 Nenhum livro cadastrado.")
    print()

def atualizar_livro():
    print("\n=== Atualizar Livro ===")
    try:
        id_livro = int(input("Digite o ID do livro a ser atualizado: "))
        cursor.execute('SELECT * FROM livros WHERE id = ?', (id_livro,))
        if cursor.fetchone() is None:
            print("⚠️ Livro não encontrado.\n")
            return

        print("Campos disponíveis: titulo, autor, ano_publicacao, genero, quantidade_estoque")
        campo = input("Qual campo deseja atualizar? ").strip()
        if campo not in ['titulo', 'autor', 'ano_publicacao', 'genero', 'quantidade_estoque']:
            print("⚠️ Campo inválido.\n")
            return

        novo_valor = input(f"Digite o novo valor para {campo}: ").strip()
        if campo in ['ano_publicacao', 'quantidade_estoque']:
            novo_valor = int(novo_valor)

        cursor.execute(f'UPDATE livros SET {campo} = ? WHERE id = ?', (novo_valor, id_livro))
        conn.commit()
        print("✅ Livro atualizado com sucesso!\n")
    except ValueError:
        print("⚠️ Entrada inválida. Digite números onde for necessário.\n")

def excluir_livro():
    print("\n=== Excluir Livro ===")
    try:
        id_livro = int(input("Digite o ID do livro a ser excluído: "))
        cursor.execute('SELECT * FROM livros WHERE id = ?', (id_livro,))
        if cursor.fetchone() is None:
            print("⚠️ Livro não encontrado.\n")
            return

        confirmacao = input("Tem certeza que deseja excluir? (s/n): ").strip().lower()
        if confirmacao == 's':
            cursor.execute('DELETE FROM livros WHERE id = ?', (id_livro,))
            conn.commit()
            print("🗑️ Livro excluído com sucesso!\n")
        else:
            print("❌ Exclusão cancelada.\n")
    except ValueError:
        print("⚠️ Entrada inválida. Digite números onde for necessário.\n")


conn.close()