import streamlit as st

def redenrizar_footer():
    footer =     """
    <style>
        .meu-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 50px;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        background-color: #0e1117;
        color: white;
        text-align: center;
        padding: 8px 0;
        font-size: 16px;
        gap:5px;
        z-index: 999;
        }

        [data-testid="stSidebar"][aria-expanded="true"] ~ .st-emotion-cache-6px8kg .meu-footer {
        left: 300px;
        width: calc(100% - 300px);
        }

        .meu-link {
        all: unset;
        display: block;
        cursor: pointer;
        text-style: none;
        color: white;
        }
    </style>

    <footer class="meu-footer">
        Desenvolvido por  <a target="_blank" class="meu-link" href="https://arturrochel.vercel.app/"> Artur Rochel</a>
    </footer>
    """
    
    st.html(footer)

