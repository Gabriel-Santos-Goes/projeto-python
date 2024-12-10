import sqlite3

# Nome do banco de dados
NOME_BANCO = "tarefas.db"

# Função para conectar ao banco e criar a tabela se ela não existir
def conectar_banco():
    conexao = sqlite3.connect(NOME_BANCO)
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            concluida BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    conexao.commit()
    return conexao

# Função para adicionar uma nova tarefa
def adicionar_tarefa(conexao):
    titulo = input("\nDigite o título da tarefa: ").strip()
    if not titulo:
        print("⚠️ O título não pode estar vazio. Tente novamente.")
        return
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO tarefas (titulo) VALUES (?)", (titulo,))
    conexao.commit()
    print(f"✅ Tarefa '{titulo}' adicionada com sucesso!")

# Função para listar todas as tarefas
def listar_tarefas(conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT id, titulo, concluida FROM tarefas")
    tarefas = cursor.fetchall()
    print("\n📋 Suas tarefas:")
    if not tarefas:
        print("Você ainda não tem nenhuma tarefa. Que tal adicionar uma?")
    else:
        for id_tarefa, titulo, concluida in tarefas:
            status = "✅" if concluida else "❌"
            print(f"{id_tarefa}. {titulo} - {status}")

# Função para marcar uma tarefa como concluída
def concluir_tarefa(conexao):
    listar_tarefas(conexao)
    try:
        id_tarefa = int(input("\nDigite o ID da tarefa que você concluiu: "))
        cursor = conexao.cursor()
        cursor.execute("UPDATE tarefas SET concluida = 1 WHERE id = ?", (id_tarefa,))
        if cursor.rowcount == 0:
            print("⚠️ Nenhuma tarefa encontrada com esse ID. Tente novamente.")
        else:
            conexao.commit()
            print(f"🎉 Parabéns! A tarefa {id_tarefa} foi marcada como concluída.")
    except ValueError:
        print("⚠️ Por favor, digite um número válido.")

# Função principal (menu)
def menu():
    conexao = conectar_banco()
    print("👋 Olá! Bem-vindo ao seu Gerenciador de Tarefas.")
    while True:
        print("\n=== O que você gostaria de fazer? ===")
        print("1. Adicionar uma nova tarefa")
        print("2. Ver suas tarefas")
        print("3. Marcar uma tarefa como concluída")
        print("4. Sair")
        opcao = input("Digite o número da opção escolhida: ").strip()

        if opcao == "1":
            adicionar_tarefa(conexao)
        elif opcao == "2":
            listar_tarefas(conexao)
        elif opcao == "3":
            concluir_tarefa(conexao)
        elif opcao == "4":
            print("👋 Até logo! Espero que suas tarefas sejam um sucesso!")
            conexao.close()
            break
        else:
            print("⚠️ Opa, parece que você digitou uma opção inválida. Tente novamente.")

# Executa o menu
if __name__ == "__main__":
    menu()
