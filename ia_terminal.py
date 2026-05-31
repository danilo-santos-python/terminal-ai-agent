# Carrega variáveis do arquivo .env
from dotenv import load_dotenv

# Permite acessar variáveis de ambiente
import os

# Modelo Gemini
from langchain_google_genai import ChatGoogleGenerativeAI

# Estruturas de mensagens usadas pelo modelo
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# --------------------------------------------------
# CONFIGURAÇÃO INICIAL
# --------------------------------------------------

# Lê o arquivo .env
load_dotenv()

# Obtém a chave da API Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Impede a execução sem chave válida
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY não encontrada no arquivo .env"
    )

# --------------------------------------------------
# INICIALIZAÇÃO DO MODELO
# --------------------------------------------------

# Cria a conexão com o modelo Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.3
)

# --------------------------------------------------
# MEMÓRIA DA CONVERSA
# --------------------------------------------------

# A primeira mensagem define o comportamento da IA
history = [
    SystemMessage(
        content=(
            "You are a helpful AI assistant. "
            "Provide clear, concise and accurate answers."
        )
    )
]

# Quantidade máxima de mensagens armazenadas
# Evita crescimento infinito do contexto
MAX_HISTORY = 20

# --------------------------------------------------
# INTERFACE DE TERMINAL
# --------------------------------------------------

print("\nIA Terminal iniciada.")
print("Digite 'exit' para encerrar.\n")

# Mantém a aplicação em execução
while True:

    # Lê a mensagem digitada pelo usuário
    user_input = input("You: ").strip()

    # Ignora entradas vazias
    if not user_input:
        continue

    # Comando para encerrar o programa
    if user_input.lower() in ("exit", "quit", "sair"):
        print("Encerrando...")
        break

    # Adiciona a mensagem do usuário ao histórico
    history.append(
        HumanMessage(content=user_input)
    )

    try:

        # Envia todo o histórico para o Gemini
        response = llm.invoke(history)

        # Extrai o texto retornado pelo modelo
        answer = response.content

        # Exibe a resposta no terminal
        print(f"\nAI: {answer}\n")

        # Salva a resposta no histórico
        history.append(
            AIMessage(content=answer)
        )

        # Mantém apenas as mensagens mais recentes
        # para reduzir consumo de tokens
        if len(history) > MAX_HISTORY:
            history = [history[0]] + history[-MAX_HISTORY:]

    except Exception as error:

        # Captura erros de conexão, API ou modelo
        print(
            f"\nErro ao consultar o modelo:\n{error}\n"
        )