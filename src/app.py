import streamlit as st
import requests
import json
import pandas as pd
from pathlib import Path

# ============ CONFIGURAÇÕES ============
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3.2"  # Verifique se o modelo llama3.2 está baixado no seu ollama (ollama run llama3.2)

# Caminhos baseados na localização deste script de modo que funcione independente de onde é chamado
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """Você é o EduFin, um educador financeiro especializado em alunos e jovens universitários (foco especial a partir de 17 anos).

OBJETIVO:
Ensinar conceitos de planejamento, poupança, investimento básico e uso consciente de crédito, usando os dados da conta e perfil do cliente como exemplos práticos.

REGRAS:
- NUNCA recomende investimentos específicos sem conhecer e considerar o perfil e a idade;
- NUNCA sugira cartão de crédito, empréstimo ou cheque especial para menores de 18 anos;
- Use os dados fornecidos no contexto (perfil, transações e histórico de atendimento);
- Linguagem simples, acessível e encorajadora (como se explicasse para um colega universitário);
- Se não tiver as informações, admita e tente ajudar com conceitos gerais;
- Responda em até 3 parágrafos curtos na medida do possível;
- Seja sempre simpático e utilize emojis apropriados para engajar o usuário.
"""

# ============ CARREGAR DADOS ============
@st.cache_data
def carregar_dados():
    try:
        with open(DATA_DIR / "perfil_investidor.json", encoding="utf-8") as f:
            perfil = json.load(f)
        
        with open(DATA_DIR / "produtos_financeiros.json", encoding="utf-8") as f:
            produtos = json.load(f)
        
        historico = pd.read_csv(DATA_DIR / "historico_atendimento.csv")
        transacoes = pd.read_csv(DATA_DIR / "transacoes.csv")
        
        return perfil, produtos, historico, transacoes
    except Exception as e:
        st.error(f"Erro ao carregar os dados. Verifique a pasta 'data': {e}")
        return None, None, None, None

# ============ MONTAR CONTEXTO ============
def montar_contexto(perfil, produtos, historico, transacoes):
    cliente_historico = historico[historico["nome"] == perfil["nome"]]
    cliente_transacoes = transacoes[transacoes["nome"] == perfil["nome"]]
    
    contexto = f"""\
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA de EMERGÊNCIA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{cliente_transacoes.tail(10).to_string(index=False) if not cliente_transacoes.empty else "Nenhuma transação encontrada"}

ATENDIMENTOS ANTERIORES:
{cliente_historico.tail(5).to_string(index=False) if not cliente_historico.empty else "Nenhum atendimento anterior"}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}

REGRAS POR IDADE:
- Menores de 18 anos: NÃO podem ter cartão de crédito, cheque especial ou empréstimo.
- A partir de 16 anos: Podem ter Poupança Jovem, Cartão Pré-Pago e Conta Universitária.
- A partir de 18 anos: Podem ter CDB Universitário e cartão de crédito com limite controlado.
"""
    return contexto

# ============ CHAMAR OLLAMA COM STREAMING ============
def perguntar_stream(msg, contexto, idade):
    prompt = f"""
{SYSTEM_PROMPT}

CONTEXTO DO CLIENTE:
{contexto}

PERGUNTA DO USUÁRIO: {msg}

REGRAS ADICIONAIS A REFORÇAR:
- Idade do Cliente: {idade} anos.
- Se o cliente for menor de 18, NÃO sugira cartão de crédito, empréstimo ou cheque especial!

RESPOSTA EDUFIN:
"""
    
    try:
        r = requests.post(
            OLLAMA_URL, 
            json={"model": MODELO, "prompt": prompt, "stream": True}, 
            stream=True
        )
        r.raise_for_status()
        
        for line in r.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                result = json.loads(decoded_line)
                yield result.get("response", "")
                
    except requests.exceptions.RequestException as e:
        yield f"⚠️ **Erro de conexão com o Ollama.**\nCertifique-se de que o software do Ollama está instalado, rodando localmente (na porta 11434) e com o modelo `{MODELO}` baixado (`ollama pull {MODELO}`). Detalhes: `{e}`"

# ============ INTERFACE STREAMLIT ============
def main():
    st.set_page_config(page_title="EduFin | Educação Financeira", page_icon="🎓", layout="wide")
    
    # carregar dados base
    perfis_tipos, produtos, historico, transacoes = carregar_dados()
    if perfis_tipos is None:
        return

    # Perfis de clientes simulados baseados no histórico
    clientes_mock = {
        "Ana Clara (Estagiária, 20 anos)": {
            "nome": "Ana Clara",
            "idade": 20,
            "perfil_investidor": "Renda Própria Parcial",
            "objetivo_principal": "Economizar para intercâmbio/formatura",
            "patrimonio_total": 450.00,
            "reserva_emergencia_atual": 150.00
        },
        "João Pedro (Estudante, 17 anos)": {
            "nome": "João Pedro",
            "idade": 17,
            "perfil_investidor": "Mesada Fixa",
            "objetivo_principal": "Comprar um notebook novo para estudos",
            "patrimonio_total": 50.00,
            "reserva_emergencia_atual": 0.00
        },
        "Marina Silva (Empreendedora, 19 anos)": {
            "nome": "Marina Silva",
            "idade": 19,
            "perfil_investidor": "Empreendedor/Startup",
            "objetivo_principal": "Crescer minha startup e ter liberdade financeira",
            "patrimonio_total": 5500.00,
            "reserva_emergencia_atual": 2500.00
        }
    }

    # --- SIDEBAR: SELEÇÃO E INFORMAÇÕES DO CLIENTE ---
    with st.sidebar:
        st.title("Simulação do Cliente")
        cliente_selecionado = st.selectbox("Quem está acessando o App?", list(clientes_mock.keys()))
        perfil = clientes_mock[cliente_selecionado]
        
        st.divider()
        st.title(f"Acesso: {perfil['nome']}")
        st.markdown(f"**Idade:** {perfil['idade']} anos")
        st.markdown(f"**Perfil:** {str(perfil['perfil_investidor']).capitalize()}")
        st.markdown(f"**Meu Objetivo Principal:** {perfil['objetivo_principal']}")
        st.divider()
        
        st.subheader("💰 Suas Finanças Atuais")
        st.metric(label="Patrimônio Total", value=f"R$ {perfil['patrimonio_total']:.2f}")
        st.metric(label="Reserva de Emergência", value=f"R$ {perfil['reserva_emergencia_atual']:.2f}")
        st.divider()
        
        st.info("💡 **O EduFin analisa constantemente seu perfil** e as opções do mercado para te recomendar os melhores caminhos na sua jornada financeira e educacional!")

    contexto = montar_contexto(perfil, produtos, historico, transacoes)
    
    # Gerenciamento de histórico de mensagens por usuário
    session_key = f"messages_{perfil['nome']}"
    
    # --- ÁREA PRINCIPAL: CHATBOT EDUFIN ---
    st.title("🎓 EduFin - Seu Assessor e Educador Financeiro Virtual")
    st.write("Olá! Sou o EduFin, o seu novo colega de faculdade especializado em finanças. Vou te ajudar a alcançar suas metas, poupar dinheiro de um jeito inteligente e entrar no mundo dos investimentos no seu próprio ritmo.")
    
    # Inicializar histórico de mensagens desse cliente
    if session_key not in st.session_state:
        st.session_state[session_key] = [
            {"role": "assistant", "content": f"Olá, {perfil['nome']}! Vi que seu grande objetivo é **{perfil['objetivo_principal']}**. O que podemos aprender hoje que nos deixe mais perto de alcançá-lo? 🚀"}
        ]
    
    # Exibir histórico na tela do chat
    for msg in st.session_state[session_key]:
        avatar = "🎓" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
    
    # Caixa de entrada para que o usuário faça a pergunta
    if pergunta := st.chat_input(f"Mensagem de {perfil['nome']} para o EduFin..."):
        
        # Guardar e renderizar a mensagem do usuário
        st.session_state[session_key].append({"role": "user", "content": pergunta})
        with st.chat_message("user", avatar="👤"):
            st.markdown(pergunta)
        
        # Renderizar fluxo (stream) do bot simulando estar digitando
        with st.chat_message("assistant", avatar="🎓"):
            resposta_stream = perguntar_stream(pergunta, contexto, perfil["idade"])
            resposta_completa = st.write_stream(resposta_stream)
            
        # Salvar resposta final no histórico
        st.session_state[session_key].append({"role": "assistant", "content": resposta_completa})

if __name__ == "__main__":
    main()
