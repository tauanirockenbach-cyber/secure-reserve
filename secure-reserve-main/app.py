import time
import streamlit as st

# ------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Acesso ao Sistema",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------------
# CREDENCIAIS E LINKS
# ------------------------------------------------------------------
USUARIO_CORRETO = "admin"
SENHA_CORRETA = "12345"
URL_DO_FORMULARIO_APPSHEET = (
    "https://www.appsheet.com/start/0258d3f8-ef68-4825-94c3-d696dc4f14df"
)

# Inicialização dos estados da sessão
if "logado" not in st.session_state:
    st.session_state.logado = False

if "tentativas" not in st.session_state:
    st.session_state.tentativas = 0

if "bloqueado_ate" not in st.session_state:
    st.session_state.bloqueado_ate = 0

# ------------------------------------------------------------------
# ESTILO CSS
# ------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
}

/* Esconde elementos padrão do Streamlit */
#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden;
    height: 0;
}
.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
}

/* ---------- FUNDO ---------- */
.stApp {
    background: linear-gradient(135deg, #7cc4ff 0%, #4da3ff 50%, #2f8cf5 100%);
    background-attachment: fixed;
}
/* Formas desfocadas flutuando ao fundo */
.stApp::before, .stApp::after {
    content: "";
    position: fixed;
    border-radius: 50%;
    filter: blur(90px);
    opacity: 0.55;
    z-index: 0;
    pointer-events: none;
    animation: flutuar 14s ease-in-out infinite alternate;
}
.stApp::before {
    width: 520px; height: 520px;
    background: #e0f2fe;
    top: -140px; left: -120px;
}
.stApp::after {
    width: 460px; height: 460px;
    background: #a5d8ff;
    bottom: -140px; right: -100px;
    animation-delay: -6s;
}
@keyframes flutuar {
    from { transform: translate(0, 0) scale(1); }
    to   { transform: translate(40px, 30px) scale(1.12); }
}

/* ---------- CARD ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.96) !important;
    border-radius: 24px !important;
    border: 1px solid rgba(255, 255, 255, 0.6) !important;
    box-shadow: 0 25px 60px rgba(15, 60, 140, 0.30) !important;
    padding: 36px 32px !important;
    position: relative;
    z-index: 2;
    animation: entrada 0.6s cubic-bezier(.2,.8,.2,1);
}
@keyframes entrada {
    from { opacity: 0; transform: translateY(24px) scale(.98); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* ---------- ELEMENTOS DO CARD ---------- */
.logo-circulo {
    width: 72px; height: 72px;
    margin: 0 auto 18px auto;
    border-radius: 22px;
    background: linear-gradient(135deg, #1273ea, #0a3d91);
    display: flex; align-items: center; justify-content: center;
    font-size: 32px;
    box-shadow: 0 12px 28px rgba(18, 115, 234, 0.45);
}
.logo-sucesso {
    background: linear-gradient(135deg, #22c55e, #15803d);
    box-shadow: 0 12px 28px rgba(34, 197, 94, 0.45);
    color: #fff;
    font-weight: 800;
}
.titulo {
    text-align: center;
    color: #0f172a;
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0 0 6px 0;
}
.titulo span { color: #1273ea; }
.subtitulo {
    text-align: center;
    color: #1e293b;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 26px;
    line-height: 1.5;
}
.divisor {
    height: 1px;
    background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
    margin: 18px 0 20px 0;
}
.rodape {
    text-align: center;
    color: #334155;
    font-size: 12px;
    font-weight: 500;
    margin-top: 18px;
}

/* ---------- INPUTS ---------- */
label, [data-testid="stWidgetLabel"] p {
    color: #0f172a !important;
    font-weight: 700 !important;
    font-size: 13px !important;
}
div[data-baseweb="input"] {
    background-color: #eaf2fb !important;
    border: 1.5px solid #cbd9ec !important;
    border-radius: 12px !important;
    transition: all .2s ease;
}
div[data-baseweb="input"]:focus-within {
    background-color: #ffffff !important;
    border-color: #1273ea !important;
    box-shadow: 0 0 0 4px rgba(18, 115, 234, 0.15) !important;
}
div[data-baseweb="input"] input {
    color: #0f172a !important;
    font-size: 15px !important;
    padding: 12px 8px !important;
}
div[data-baseweb="input"] input::placeholder {
    color: #475569 !important;
}

/* ---------- BOTÕES ---------- */
div.stButton > button,
div[data-testid="stLinkButton"] a {
    height: 50px !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: .4px;
    border: none !important;
    transition: all .25s ease !important;
}
/* Botão primário (ENTRAR / abrir formulário) */
div.stButton > button[kind="secondary"]:not(.sair),
div[data-testid="stLinkButton"] a {
    background: linear-gradient(135deg, #1273ea, #0a58c9) !important;
    color: #ffffff !important;
    box-shadow: 0 8px 20px rgba(18, 115, 234, 0.35) !important;
}
div.stButton > button:hover,
div[data-testid="stLinkButton"] a:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 26px rgba(18, 115, 234, 0.5) !important;
    filter: brightness(1.06);
}
div.stButton > button:active {
    transform: translateY(0);
}
div.stButton > button p,
div[data-testid="stLinkButton"] a p {
    color: #ffffff !important;
}

/* Alertas */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------
# TELA DE LOGIN
# ------------------------------------------------------------------
if not st.session_state.logado:
    _, centro, _ = st.columns([3, 4, 3])

    with centro:
        st.write("")
        st.write("")
        st.write("")

        with st.container(border=True):
            st.markdown(
                """
                <div class="logo-circulo">🔒</div>
                <h2 class="titulo">Bem-vindo ao <span>LOGIN</span></h2>
                <p class="subtitulo">Preencha seus dados para acessar o sistema</p>
                """,
                unsafe_allow_html=True,
            )

            # Cálculo do tempo restante de bloqueio
            agora = time.time()
            tempo_restante = int(st.session_state.bloqueado_ate - agora)
            esta_bloqueado = tempo_restante > 0

            # Alerta visual de bloqueio
            if esta_bloqueado:
                st.error(
                    f"🔒 Excesso de tentativas falhas. Aguarde **{tempo_restante}s** para tentar novamente."
                )

            usuario = st.text_input(
                "Usuário",
                placeholder="Digite seu usuário",
                icon="👤",
                disabled=esta_bloqueado,
            )
            senha = st.text_input(
                "Senha",
                type="password",
                placeholder="Digite sua senha",
                icon="🔑",
                disabled=esta_bloqueado,
            )

            st.write("")

            if st.button("ENTRAR", use_container_width=True, disabled=esta_bloqueado):
                if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
                    st.session_state.logado = True
                    st.session_state.tentativas = 0
                    st.session_state.bloqueado_ate = 0
                    st.toast("Acesso autorizado!", icon="✅")
                    st.rerun()
                else:
                    st.session_state.tentativas += 1
                    restantes = 5 - st.session_state.tentativas

                    if st.session_state.tentativas >= 5:
                        st.session_state.bloqueado_ate = time.time() + 30
                        st.session_state.tentativas = 0
                        st.rerun()
                    else:
                        st.error(
                            f"Usuário ou senha incorretos. Você tem mais {restantes} tentativa(s)."
                        )

            st.markdown(
                '<div class="rodape">Ambiente seguro e monitorado</div>',
                unsafe_allow_html=True,
            )

            # Atualização em tempo real sem bloquear a aplicação
            if esta_bloqueado:
                time.sleep(1)
                st.rerun()
            elif st.session_state.bloqueado_ate > 0:
                st.session_state.bloqueado_ate = 0
                st.session_state.tentativas = 0
                st.rerun()

# ------------------------------------------------------------------
# TELA PÓS-LOGIN
# ------------------------------------------------------------------
else:
    _, centro, _ = st.columns([3, 4, 3])

    with centro:
        st.write("")
        st.write("")
        st.write("")

        with st.container(border=True):
            st.markdown(
                """
                <div class="logo-circulo logo-sucesso">✓</div>
                <h2 class="titulo">Login <span style="color:#16a34a;">confirmado!</span></h2>
                <p class="subtitulo">
                    Seu acesso foi validado com sucesso.<br>
                    Abra o formulário de reserva em ambiente seguro.
                </p>
                <div class="divisor"></div>
                """,
                unsafe_allow_html=True,
            )

            st.link_button(
                "📋  Abrir Formulário no Tablet",
                URL_DO_FORMULARIO_APPSHEET,
                use_container_width=True,
            )

            st.write("")

            if st.button("Encerrar Sessão (Sair)", use_container_width=True):
                st.session_state.logado = False
                st.rerun()

            st.markdown(
                '<div class="rodape">Sessão ativa · lembre-se de sair ao terminar</div>',
                unsafe_allow_html=True,
            )