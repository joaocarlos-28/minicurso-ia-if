import streamlit as st

st.set_page_config(page_title="Portal do Aluno", page_icon=" ")
st.sidebar.title(" Desenvolvedor")
st.sidebar.write("Minicurso IA para Devs")

st.title(" Simulador de Desempenho")

c1, c2 = st.columns(2)
with c1: n1 = st.text_input("Nota 1", value="0")
with c2: n2 = st.text_input("Nota 2", value="0")
with c3: n3 = st.text_input("Nota 3", value="0")
  
if st.button("Analisar Notas", use_container_width=True):
  try:
    resultado = (float(n1) + float(n2)) / 2
    if resultado >= 6.0:
      st.success(f"Média: {resultado:.1f} - APROVADO! ")
    else:
      st.error(f"Média: {resultado:.1f} - RECUPERAÇÃO ")
  except ValueError:
    st.warning(" Erro: Introduza apenas números (use ponto para decimais).")
