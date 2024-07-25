import streamlit as st
import sqlite3
import bcrypt

# Conexão com o banco de dados
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Criar tabela de usuários se não existir
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT)''')

# Função para hash da senha
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Função para verificar a senha
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

# Função para criar um novo usuário
def create_user(username, password):
    hashed_password = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# Função para verificar o login
def check_login(username, password):
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    if result:
        return check_password(password, result[0])
    return False

# Inicializar o estado da sessão
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ''

# Função para a página logada
def logged_in_page():
    st.title(f"Bem-vindo, {st.session_state.username}!")
    st.write("Esta é a sua página pessoal após o login.")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ''
        st.rerun()

# Interface principal
if st.session_state.logged_in:
    logged_in_page()
else:
    st.title("App de Login e Registro")

    tab1, tab2 = st.tabs(["Login", "Registro"])

    with tab1:
        st.header("Login")
        username = st.text_input("Usuário", key="login_user")
        password = st.text_input("Senha", type='password', key="login_pass")
        if st.button("Login"):
            if check_login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")

    with tab2:
        st.header("Criar nova conta")
        new_user = st.text_input("Usuário", key="reg_user")
        new_password = st.text_input("Senha", type='password', key="reg_pass")
        if st.button("Registrar"):
            if create_user(new_user, new_password):
                st.success("Conta criada com sucesso!")
            else:
                st.error("Usuário já existe")

# Fechar conexão com o banco de dados
conn.close()