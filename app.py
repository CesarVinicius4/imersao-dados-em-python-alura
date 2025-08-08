import plotly.express as px
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon=":bar_chart:",
    layout="wide",
)

df = pd.read_csv(
    "https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv"
)

# Barra Lateral
st.sidebar.header("Filtros")

# Filtro de Ano
anos_disponiveis = sorted(df["ano"].unique())
anos_selecionados = st.sidebar.multiselect(
    "Selecione o(s) ano(s):", anos_disponiveis, default=anos_disponiveis
)

# Filtro de Senioridade
senioridades_disponiveis = sorted(df["senioridade"].unique())
senioridades_selecionadas = st.sidebar.multiselect(
    "Selecione a(s) senioridade(s):",
    senioridades_disponiveis,
    default=senioridades_disponiveis,
)

# Filtro por tipo de contrato
contratos_disponiveis = sorted(df["contrato"].unique())
contratos_selecionados = st.sidebar.multiselect(
    "Selecione o(s) tipo(s) de contrato:",
    contratos_disponiveis,
    default=contratos_disponiveis,
)

# Filtro por tamanho da empresa
tamanhos_disponiveis = sorted(df["tamanho_empresa"].unique())
tamanhos_selecionados = st.sidebar.multiselect(
    "Selecione o(s) tamanho(s) da empresa:",
    tamanhos_disponiveis,
    default=tamanhos_disponiveis,
)

df_filtrado = df[
    (df["ano"].isin(anos_selecionados))
    & (df["senioridade"].isin(senioridades_selecionadas))
    & (df["contrato"].isin(contratos_selecionados))
    & (df["tamanho_empresa"].isin(tamanhos_selecionados))
]

st.title("🎲 Dashboard de Salários na Área de Dados")
st.markdown(
    "Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros a esquerda para refinar sua análise."
)

# Métricas Principais
st.subheader("Métricas Gerais(Salário anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado["usd"].mean()
    salario_maximo = df_filtrado["usd"].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
else:
    (
        salario_medio,
        salario_maximo,
        total_registros,
        cargo_mais_frequente,
    ) = (0, 0, 0, "")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário Médio", f"${salario_medio:,.0f}")
col2.metric("Salário Máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de Registros", total_registros)
col4.metric("Cargo Mais Frequente", cargo_mais_frequente)

st.markdown("---")

st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = (
            df_filtrado.groupby("cargo")["usd"]
            .mean()
            .nlargest(10)
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        grafico_cargos = px.bar(
            top_cargos,
            x="usd",
            y="cargo",
            color="usd",
            color_continuous_scale=["#54e04a", "#006400"],
            orientation="h",
            title="Top 10 Cargos com Maior Salário Médio",
            labels={"usd": "Média Salarial anual(USD)", "cargo": ""},
        )
        grafico_cargos.update_layout(
            title_x=0.1, yaxis={"categoryorder": "total ascending"}, showlegend=False
        )
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x="usd",
            nbins=30,
            title="Distribuição de salários anuais",
            labels={"usd": "Faixa salarial (USD)", "count": ""}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado["remoto"].value_counts().reset_index()
        remoto_contagem.columns = ["tipo_trabalho", "quantidade"]
        grafico_remoto = px.pie(
            remoto_contagem,
            names="tipo_trabalho",
            values="quantidade",
            title="Proporção dos tipos de trabalho",
            hole=0.5,
        )
        grafico_remoto.update_traces(textinfo="percent+label")
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

with col_graf4:
    if not df_filtrado.empty:
        cargo_filtrado = "Data Analyst"
        df_ds = df_filtrado[df_filtrado["cargo"] == cargo_filtrado]
        media_ds_pais = df_ds.groupby("residencia_iso3")["usd"].mean().reset_index()
        grafico_paises = px.choropleth(
            media_ds_pais,
            locations="residencia_iso3",
            color="usd",
            color_continuous_scale="rdylgn",
            title=f"Salário médio de {cargo_filtrado} por país",
            labels={"usd": "Salário médio (USD)", "residencia_iso3": "País"}
        )
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")

col_graf5, col_graf6 = st.columns(2)

with col_graf5:
    if not df_filtrado.empty:
        grafico_senioridade = px.histogram(
            df_filtrado,
            x="senioridade",
            nbins=10,
            color_discrete_sequence=['indianred'],
            title="Distribuição de Senioridades",
            labels={"senioridade": "Nível de Senioridade", "count": ""}
        )
        grafico_senioridade.update_layout(title_x=0.1)
        st.plotly_chart(grafico_senioridade, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de senioridades.")

with col_graf6:
    if not df_filtrado.empty:
        tamanho_empresa_contagem = df_filtrado["tamanho_empresa"].value_counts().reset_index()
        tamanho_empresa_contagem.columns = ["tamanho_empresa", "quantidade"]
        grafico_tamanho_empresa = px.pie(
            tamanho_empresa_contagem,
            names="tamanho_empresa",
            values="quantidade",
            title="Distribuição de Tamanhos de Empresa",
            hole=0.5,
            color="tamanho_empresa",
            color_discrete_map={
                "Pequena": "#dbdf10",
                "Média": "#DA7C03",
                "Grande": "#05502a",
            }
        )
        grafico_tamanho_empresa.update_traces(textinfo="percent+label")
        grafico_tamanho_empresa.update_layout(title_x=0.1)
        st.plotly_chart(grafico_tamanho_empresa, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de tamanhos de empresa.")

st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)
