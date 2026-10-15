
import streamlit as st

# Configuração da página em modo Wide para ocupar a tela inteira
st.set_page_config(
    page_title="Acesso ao Sistema", 
    page_icon="🔒", 
    layout="wide"
)

# --- CONFIGURAÇÃO DE CREDENCIAIS ---
USUARIO_CORRETO = "admin"
SENHA_CORRETA = "12345"
URL_DO_FORMULARIO_APPSHEET = "https://www.appsheet.com/start/0258d3f8-ef68-4825-94c3-d696dc4f14df"

# Inicializa o estado de login caso não exista
if "logado" not in st.session_state:
    st.session_state.logado = False

# --- ESTILIZAÇÃO CSS CUSTOMIZADA (ESTILO DA SUA IMAGEM) ---
design_login_customizado = """
<style>
/* Remove as margens padrão do Streamlit e adiciona o fundo com formas azuis */
.stApp {
    background-color: #ffffff;
    background-image: 
        radial-gradient(circle at 10% 20%, #007bff 15%, transparent 16%),
        radial-gradient(circle at 85% 40%, #0069d9 22%, transparent 23%),
        radial-gradient(circle at 25% 85%, #007bff 12%, transparent 13%);
    background-attachment: fixed;
}

/* Customização total do Card de Login */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #ffffff !important;
    border-radius: 16px !important;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.08) !important;
    padding: 30px !important;
    border: none !important;
}

/* Customização dos inputs para ficarem mais limpos */
div[data-baseweb="input"] {
    border-radius: 8px !important;
    background-color: #f8f9fa !important;
}

/* Estilização do botão ENTRAR em Azul Forte */
div.stButton > button:first-child {
    background-color: #007bff !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: bold !important;
    height: 45px !important;
    transition: all 0.3s ease;
}

div.stButton > button:first-child:hover {
    background-color: #0056b3 !important;
    box-shadow: 0px 5px 15px rgba(0, 123, 255, 0.4) !important;
    transform: translateY(-1px);
}
</style>
"""

# Aplica o estilo na tela
st.markdown(design_login_customizado, unsafe_allow_html=True)

# --- interface visual da tela de login ---
if not st.session_state.logado:
    
    # Criamos colunas largas para centralizar perfeitamente o card na tela
    left_space, main_card, right_space = st.columns([1.2, 1, 1.2])
    
    with main_card:
        st.write("") # Espaçadores verticais para descer o card
        st.write("")
        st.write("")
        
        # O container que vira o Card Branco através do nosso CSS
        with st.container(border=True):
            # Cabeçalho estilizado igual à imagem
            st.markdown("<h2 style='text-align: center; color: #1e293b; font-family: sans-serif; font-weight: 700; margin-bottom: 5px;'>Bem vindo ao <span style='color: #007bff;'>LOGIN</span></h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px; margin-bottom: 25px;'>Preencha os dados de login para acessar</p>", unsafe_allow_html=True)
            
            # Campos de entrada
            usuario = st.text_input("Usuário", placeholder="Ex: jhonasrodrigues", icon="👤")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha...", icon="🔑")
            
            st.write("")
            
            # Botão Entrar expandido
            if st.button("ENTRAR", use_container_width=True):
                if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
                    st.session_state.logado = True
                    st.toast("Acesso autorizado!", icon="✅")
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")

# --- TELA DE DIRECIONAMENTO (PÓS-LOGIN) ---
else:
    left_space, main_card, right_space = st.columns([1.2, 1, 1.2])
    with main_card:
        st.write("")
        st.write("")
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center; color: #10B981;'>✓ Login Confirmado</h2>", unsafe_allow_html=True)
            st.write("---")
            
            st.write("Seu acesso foi validado com sucesso. Clique abaixo para abrir o formulário de reserva em ambiente seguro:")
            
            st.link_button("🚀 Abrir Formulário no Tablet", URL_DO_FORMULARIO_APPSHEET, type="primary", use_container_width=True)
            
            st.write("")
            if st.button("Encerrar Sessão (Sair)", type="secondary", use_container_width=True):
                st.session_state.logado = False
                st.rerun()
