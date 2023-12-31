import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards 

@st.cache_data
def carregar_dados():
    # carregar as bases de dados
    df_vendas = pd.read_excel("Vendas.xlsx")
    df_produtos = pd.read_excel("Produtos.xlsx")

    df = pd.merge(df_vendas, df_produtos, how='left', on='ID Produto')

    # Criando colunas
    df["Custo"] = df["Custo Unitário"] * df["Quantidade"]
    df["Lucro"] = df["Valor Venda"] - df["Custo"]
    df["mes_ano"] = df["Data Venda"].dt.to_period("M").astype(str)
    df["Ano"] = df["Data Venda"].dt.year

    return df


def main():

    df = carregar_dados() 
    st.title("Dasboard de Vendas 📊")
    ano_filtrado = st.sidebar.selectbox("Filtrar por Ano:", [None, *df['Ano'].unique()])

    if ano_filtrado is not None:
        df_filtrado = df[df['Ano'] == ano_filtrado]
    else:
        df_filtrado = df.copy()  
    total_custo = (df_filtrado["Custo"].sum()).astype(str)
    total_custo = total_custo.replace(".",",")
    total_custo = "R$" + total_custo[:2] + "." + total_custo[2:5] + "." + total_custo[5:]    
    total_lucro = (df_filtrado["Lucro"].sum()).astype(str)
    total_lucro = total_lucro.replace(".",",")
    total_lucro = "R$" + total_lucro[:2] +"." + total_lucro[2:5] + "." + total_lucro[5:]
    total_clientes = df_filtrado["ID Cliente"].nunique()

    produtos_vendidos_marca = df_filtrado.groupby("Marca")["Quantidade"].sum().sort_values(ascending=True).reset_index()
    lucro_categoria = df_filtrado.groupby("Categoria")["Lucro"].sum().reset_index()
    lucro_mes_categoria = df_filtrado.groupby(["mes_ano", "Categoria"])["Lucro"].sum().reset_index()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Custo", total_custo)
        style_metric_cards(border_left_color="#3e4095")
    with col2:
        st.metric("Total Lucro", total_lucro)
    with col3:
        st.metric("Total Clientes", total_clientes)
    st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 18px;
        color: rgba(0,0,0,0,)
    }
    </style>
    """,
    unsafe_allow_html=True,
    )
    st.markdown(
    """
    <style>
    [data-testid="stMetricLabel"] {
        font-size: 40px;
        color: rgba(0,0,0,0,)
    }
    </style>
    """,
    unsafe_allow_html=True,
    )
    st.sidebar.markdown(
    """
    <style>
        .sidebar .sidebar-content {
            width: 200px;
        }
    </style>
    """,
    unsafe_allow_html=True
)
    col1, col2 = st.columns(2)
    fig = px.bar(produtos_vendidos_marca, x="Quantidade", y="Marca", orientation="h",
                 text="Quantidade", title="Total produtos vendidos por Marca",
                 width=400, height=350, color_discrete_sequence=["#3e4095"])
    fig.update_yaxes(automargin=True)
    fig.update_layout(title_x=0.5)
    col1.plotly_chart(fig, theme=None)

    fig1 = px.pie(lucro_categoria, values="Lucro", names="Categoria",
                  title="Lucro por Categoria", width=400, height=350,
                  color_discrete_sequence=["#3e4095", "#EC610C"])
    fig1.update_layout(title_x=0.5)
    col2.plotly_chart(fig1)

    fig2 = px.line(lucro_mes_categoria, x="mes_ano", y="Lucro", color="Categoria",
                   title="Lucro x Mês x Categoria", markers=True,
                   width=700,height=450, color_discrete_sequence=["#3e4095", "#EC610C", "#8860FF"])
    fig2.update_layout(title_x=0.3)
    st.plotly_chart(fig2)
if __name__ == "__main__":
    main()