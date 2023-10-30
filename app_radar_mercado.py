import streamlit as st
import plotly.express as px
import pandas as pd
#import numpy as np
import gc
#import warnings
#warnings.filterwarnings('ignore')

gc.enable()

st.set_page_config(page_title="Radar de mercado RN"
                   , page_icon=":dart:"
                   , layout="wide")

with st.container():
    st.title(" :dart: Radar de mercado do Rio Grande do Norte")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    st.write("Desenvolvido por [Kevyn Nogueira](https://www.linkedin.com/in/kevynnogueira/)")
    st.write("-------------------------------------------------------------------------------")

with st.expander("INFORMAÇÕES BÁSICAS"):

    titulos_infos = ['Dicionário de dados', 'Referências']
    tab1, tab2 = st.tabs(titulos_infos)

    with tab1:
        dados = ['CNPJ BASICO',
            'CNPJ ORDEM',
            'CNPJ DV',
            'IDENTIFICADOR MATRIZ/FILIAL',
            'NOME FANTASIA',
            'CNAE FISCAL PRINCIPAL',
            'TIPO DE LOGRADOURO',
            'LOGRADOURO',
            'NUMERO',
            'COMPLEMENTO',
            'BAIRRO',
            'CEP',
            'UF ou Unidade Federativa',
            'MUNICIPIO',
            'DDD 1',
            'TELEFONE 1',
            'CORREIO ELETRONICO',
            'CATEGORIA CNAE PRINCIPAL',
            'DESCRICAO MUNICIPIO',
            'CAPITAL SOCIAL ou Capital',
            'PORTE DA EMPRESA',
            'DESCRICAO CNAE'
        ]

        descricoes = ['NÚMERO BASE DE INSCRIÇÃO NO CNPJ (OITO PRIMEIROS DÍGITOS DO CNPJ).',
        'NÚMERO DO ESTABELECIMENTO DE INSCRIÇÃO NO CNPJ (DO NONO ATÉ O DÉCIMO SEGUNDO DÍGITO DO CNPJ).',
        'DÍGITO VERIFICADOR DO NÚMERO DE INSCRIÇÃO NO CNPJ (DOIS ÚLTIMOS DÍGITOS DO CNPJ).',
        'CÓDIGO DO IDENTIFICADOR MATRIZ/FILIAL',
        'CORRESPONDE AO NOME FANTASIA',
        'CÓDIGO DA ATIVIDADE ECONÔMICA PRINCIPAL DO ESTABELECIMENTO',
        'DESCRIÇÃO DO TIPO DE LOGRADOURO',
        'NOME DO LOGRADOURO ONDE SE LOCALIZA O ESTABELECIMENTO.',
        'NÚMERO ONDE SE LOCALIZA O ESTABELECIMENTO. QUANDO NÃO HOUVER PREENCHIMENTO DO NÚMERO HAVERÁ ‘S/N’.',
        'COMPLEMENTO PARA O ENDEREÇO DE LOCALIZAÇÃO DO ESTABELECIMENTO',
        'BAIRRO ONDE SE LOCALIZA O ESTABELECIMENTO.',
        'CÓDIGO DE ENDEREÇAMENTO POSTAL REFERENTE AO LOGRADOURO NO QUAL O ESTABELECIMENTO ESTA LOCALIZADO',
        'UNIDADE DA FEDERAÇÃO EM QUE SE ENCONTRA O ESTABELECIMENTO',
        'CÓDIGO DO MUNICÍPIO DE JURISDIÇÃO ONDE SE ENCONTRA O ESTABELECIMENTO',
        'CONTÉM O DDD 1',
        'CONTÉM O NÚMERO DO TELEFONE 1',
        'CONTÉM O E-MAIL DO CONTRIBUINTE',
        'Contém o tipo de atividade da empresa. Sumariza os CNAE (Nçao é uma classificação oficial do governo)',
        'MUNICÍPIO DE JURISDIÇÃO ONDE SE ENCONTRA O ESTABELECIMENTO',
        'CAPITAL SOCIAL DA EMPRESA. Todo valor bruto disponibilizado para abrir uma empresa e mantê-la funcionando até que gere lucros',
        'Se refere ao tamanhoda empresa, podendo ser: NÃO INFORMADO; MICRO EMPRESA;  EMPRESA DE PEQUENO PORTE; DEMAIS',
        'Descricão do CNAE fiscal principal do estabelecimento'
        ]

        tab1_dict = {'DADO': dados, 'DESCRIÇÃO': descricoes}
        tab1_df = pd.DataFrame(data=tab1_dict)
        st.dataframe(tab1_df)

    with tab2:
        st.write("Dados foram obtidos através de:")
        st.write('[Dados abertos do governo](https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj)')
        #st.write('[Dados de geolocalização do Open Adresses](https://openaddresses.io/)')

#@st.cache_data
def carregar_dados():
    df = pd.read_parquet("df_estabelecimentos_completo.parquet")
    df_socios = pd.read_parquet("df_socios.parquet")
    return df,df_socios

df,df_socios = carregar_dados()

st.sidebar.header("FILTROS:")

# Create for DESCRICAO MUNICIPIO
municipio=st.sidebar.multiselect("Município:", df["DESCRICAO MUNICIPIO"].sort_values().unique())
if not municipio:
    df2=df.copy()
else:
    df2=df[df["DESCRICAO MUNICIPIO"].isin(municipio)]

# Create for BAIRRO
bairro=st.sidebar.multiselect("Bairro:", df2["BAIRRO"].sort_values().unique())
if not bairro:
    df3=df2.copy()
else:
    df3=df2[df2["BAIRRO"].isin(bairro)]

# Create for PORTE DA EMPRESA
porte_empresa=st.sidebar.multiselect("Porte da empresa:", df3["PORTE DA EMPRESA"].sort_values().unique())

if not porte_empresa:
    df4 = df3.copy()
else:
    df4 = df3[df3["PORTE DA EMPRESA"].isin(porte_empresa)]

# Create for CATEGORIA CNAE PRINCIPAL
categoria = st.sidebar.multiselect("Categoria:", df4["CATEGORIA CNAE PRINCIPAL"].sort_values().unique())

if not categoria:
    df5 = df4.copy()
else:
    df5 = df4[df4["CATEGORIA CNAE PRINCIPAL"].isin(categoria)]


# Create for Simples
simples = st.sidebar.multiselect("Opção pelo Simples:", df5["OPCAO PELO SIMPLES"].sort_values().unique())

if not simples:
    df6 = df5.copy()
else:
    df6 = df5[df5["OPCAO PELO SIMPLES"].isin(simples)]

# Create for Mei
mei = st.sidebar.multiselect("Opção pelo MEI:", df5["OPCAO PELO MEI"].sort_values().unique())

if not mei:
    df7 = df6.copy()
else:
    df7 = df6[df6["OPCAO PELO MEI"].isin(mei)]

# Filtering the data

if municipio and bairro and porte_empresa and categoria and simples and mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['BAIRRO'].isin(bairro) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO SIMPLES'].isin(simples) & df7['OPCAO PELO MEI'].isin(mei)]
elif municipio and bairro and porte_empresa and categoria and simples and not mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['BAIRRO'].isin(bairro) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO SIMPLES'].isin(simples)]
elif municipio and bairro and porte_empresa and categoria and not simples and mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['BAIRRO'].isin(bairro) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO MEI'].isin(mei)]
elif municipio and bairro and porte_empresa and categoria and not simples and not mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['BAIRRO'].isin(bairro) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['CATEGORIA'].isin(categoria)]
elif municipio and bairro and porte_empresa and not categoria and simples and mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['BAIRRO'].isin(bairro) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['OPCAO PELO SIMPLES'].isin(simples) & df7['OPCAO PELO MEI'].isin(mei)]
elif municipio and bairro and porte_empresa and not categoria and simples and not mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['BAIRRO'].isin(bairro) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['OPCAO PELO SIMPLES'].isin(simples)]
elif municipio and bairro and porte_empresa and not categoria and not simples and mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['BAIRRO'].isin(bairro) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['OPCAO PELO MEI'].isin(mei)]
elif municipio and bairro and porte_empresa and not categoria and not simples and not mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['BAIRRO'].isin(bairro) & df7['PORTE DA EMPRESA'].isin(porte_empresa)]
elif municipio and bairro and not porte_empresa and categoria and simples and mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['BAIRRO'].isin(bairro) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO SIMPLES'].isin(simples) & df7['OPCAO PELO MEI'].isin(mei)]
elif municipio and bairro and not porte_empresa and categoria and simples and not mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['BAIRRO'].isin(bairro) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO SIMPLES'].isin(simples)]
elif municipio and bairro and not porte_empresa and categoria and not simples and mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['BAIRRO'].isin(bairro) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO MEI'].isin(mei)]
elif municipio and bairro and not porte_empresa and categoria and not simples and not mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['BAIRRO'].isin(bairro) & df7['CATEGORIA'].isin(categoria)]
elif municipio and bairro and not porte_empresa and not categoria and simples and mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['BAIRRO'].isin(bairro) & df7['OPCAO PELO SIMPLES'].isin(simples) & df7['OPCAO PELO MEI'].isin(mei)]
elif municipio and bairro and not porte_empresa and not categoria and simples and not mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['BAIRRO'].isin(bairro) & df7['OPCAO PELO SIMPLES'].isin(simples)]
elif municipio and bairro and not porte_empresa and not categoria and not simples and mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['BAIRRO'].isin(bairro) & df7['OPCAO PELO MEI'].isin(mei)]
elif municipio and bairro and not porte_empresa and not categoria and not simples and not mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['BAIRRO'].isin(bairro)]
elif municipio and not bairro and porte_empresa and categoria and simples and mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO SIMPLES'].isin(simples) & df7['OPCAO PELO MEI'].isin(mei)]
elif municipio and not bairro and porte_empresa and categoria and simples and not mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO SIMPLES'].isin(simples)]
elif municipio and not bairro and porte_empresa and categoria and not simples and mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO MEI'].isin(mei)]
elif municipio and not bairro and porte_empresa and categoria and not simples and not mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['CATEGORIA'].isin(categoria)]
elif municipio and not bairro and porte_empresa and not categoria and simples and mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['OPCAO PELO SIMPLES'].isin(simples) & df7['OPCAO PELO MEI'].isin(mei)]
elif municipio and not bairro and porte_empresa and not categoria and simples and not mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['OPCAO PELO SIMPLES'].isin(simples)]
elif municipio and not bairro and porte_empresa and not categoria and not simples and mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['OPCAO PELO MEI'].isin(mei)]
elif municipio and not bairro and porte_empresa and not categoria and not simples and not mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['PORTE DA EMPRESA'].isin(porte_empresa)]
elif municipio and not bairro and not porte_empresa and categoria and simples and mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO SIMPLES'].isin(simples) & df7['OPCAO PELO MEI'].isin(mei)]
elif municipio and not bairro and not porte_empresa and categoria and simples and not mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO SIMPLES'].isin(simples)]
elif municipio and not bairro and not porte_empresa and categoria and not simples and mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO MEI'].isin(mei)]
elif municipio and not bairro and not porte_empresa and categoria and not simples and not mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['CATEGORIA'].isin(categoria)]
elif municipio and not bairro and not porte_empresa and not categoria and simples and mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['OPCAO PELO SIMPLES'].isin(simples) & df7['OPCAO PELO MEI'].isin(mei)]
elif municipio and not bairro and not porte_empresa and not categoria and simples and not mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['OPCAO PELO SIMPLES'].isin(simples)]
elif municipio and not bairro and not porte_empresa and not categoria and not simples and mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio) & df7['OPCAO PELO MEI'].isin(mei)]
elif municipio and not bairro and not porte_empresa and not categoria and not simples and not mei: filtered_df = df7[df7['DESCRICAO MUNICIPIO'].isin(municipio)]
elif not municipio and bairro and porte_empresa and categoria and simples and mei: filtered_df = df7[df7['BAIRRO'].isin(bairro) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO SIMPLES'].isin(simples) & df7['OPCAO PELO MEI'].isin(mei)]
elif not municipio and bairro and porte_empresa and categoria and simples and not mei: filtered_df = df7[df7['BAIRRO'].isin(bairro) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO SIMPLES'].isin(simples)]
elif not municipio and bairro and porte_empresa and categoria and not simples and mei: filtered_df = df7[df7['BAIRRO'].isin(bairro) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO MEI'].isin(mei)]
elif not municipio and bairro and porte_empresa and categoria and not simples and not mei: filtered_df = df7[df7['BAIRRO'].isin(bairro) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['CATEGORIA'].isin(categoria)]
elif not municipio and bairro and porte_empresa and not categoria and simples and mei: filtered_df = df7[df7['BAIRRO'].isin(bairro) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['OPCAO PELO SIMPLES'].isin(simples) & df7['OPCAO PELO MEI'].isin(mei)]
elif not municipio and bairro and porte_empresa and not categoria and simples and not mei: filtered_df = df7[df7['BAIRRO'].isin(bairro) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['OPCAO PELO SIMPLES'].isin(simples)]
elif not municipio and bairro and porte_empresa and not categoria and not simples and mei: filtered_df = df7[df7['BAIRRO'].isin(bairro) & df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['OPCAO PELO MEI'].isin(mei)]
elif not municipio and bairro and porte_empresa and not categoria and not simples and not mei: filtered_df = df7[df7['BAIRRO'].isin(bairro) & df7['PORTE DA EMPRESA'].isin(porte_empresa)]
elif not municipio and bairro and not porte_empresa and categoria and simples and mei: filtered_df = df7[df7['BAIRRO'].isin(bairro) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO SIMPLES'].isin(simples) & df7['OPCAO PELO MEI'].isin(mei)]
elif not municipio and bairro and not porte_empresa and categoria and simples and not mei: filtered_df = df7[df7['BAIRRO'].isin(bairro) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO SIMPLES'].isin(simples)]
elif not municipio and bairro and not porte_empresa and categoria and not simples and mei: filtered_df = df7[df7['BAIRRO'].isin(bairro) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO MEI'].isin(mei)]
elif not municipio and bairro and not porte_empresa and categoria and not simples and not mei: filtered_df = df7[df7['BAIRRO'].isin(bairro) & df7['CATEGORIA'].isin(categoria)]
elif not municipio and bairro and not porte_empresa and not categoria and simples and mei: filtered_df = df7[df7['BAIRRO'].isin(bairro) & df7['OPCAO PELO SIMPLES'].isin(simples) & df7['OPCAO PELO MEI'].isin(mei)]
elif not municipio and bairro and not porte_empresa and not categoria and simples and not mei: filtered_df = df7[df7['BAIRRO'].isin(bairro) & df7['OPCAO PELO SIMPLES'].isin(simples)]
elif not municipio and bairro and not porte_empresa and not categoria and not simples and mei: filtered_df = df7[df7['BAIRRO'].isin(bairro) & df7['OPCAO PELO MEI'].isin(mei)]
elif not municipio and bairro and not porte_empresa and not categoria and not simples and not mei: filtered_df = df7[df7['BAIRRO'].isin(bairro)]
elif not municipio and not bairro and porte_empresa and categoria and simples and mei: filtered_df = df7[df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO SIMPLES'].isin(simples) & df7['OPCAO PELO MEI'].isin(mei)]
elif not municipio and not bairro and porte_empresa and categoria and simples and not mei: filtered_df = df7[df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO SIMPLES'].isin(simples)]
elif not municipio and not bairro and porte_empresa and categoria and not simples and mei: filtered_df = df7[df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO MEI'].isin(mei)]
elif not municipio and not bairro and porte_empresa and categoria and not simples and not mei: filtered_df = df7[df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['CATEGORIA'].isin(categoria)]
elif not municipio and not bairro and porte_empresa and not categoria and simples and mei: filtered_df = df7[df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['OPCAO PELO SIMPLES'].isin(simples) & df7['OPCAO PELO MEI'].isin(mei)]
elif not municipio and not bairro and porte_empresa and not categoria and simples and not mei: filtered_df = df7[df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['OPCAO PELO SIMPLES'].isin(simples)]
elif not municipio and not bairro and porte_empresa and not categoria and not simples and mei: filtered_df = df7[df7['PORTE DA EMPRESA'].isin(porte_empresa) & df7['OPCAO PELO MEI'].isin(mei)]
elif not municipio and not bairro and porte_empresa and not categoria and not simples and not mei: filtered_df = df7[df7['PORTE DA EMPRESA'].isin(porte_empresa)]
elif not municipio and not bairro and not porte_empresa and categoria and simples and mei: filtered_df = df7[df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO SIMPLES'].isin(simples) & df7['OPCAO PELO MEI'].isin(mei)]
elif not municipio and not bairro and not porte_empresa and categoria and simples and not mei: filtered_df = df7[df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO SIMPLES'].isin(simples)]
elif not municipio and not bairro and not porte_empresa and categoria and not simples and mei: filtered_df = df7[df7['CATEGORIA'].isin(categoria) & df7['OPCAO PELO MEI'].isin(mei)]
elif not municipio and not bairro and not porte_empresa and categoria and not simples and not mei: filtered_df = df7[df7['CATEGORIA'].isin(categoria)]
elif not municipio and not bairro and not porte_empresa and not categoria and simples and mei: filtered_df = df7[df7['OPCAO PELO SIMPLES'].isin(simples) & df7['OPCAO PELO MEI'].isin(mei)]
elif not municipio and not bairro and not porte_empresa and not categoria and simples and not mei: filtered_df = df7[df7['OPCAO PELO SIMPLES'].isin(simples)]
elif not municipio and not bairro and not porte_empresa and not categoria and not simples and mei: filtered_df = df7[df7['OPCAO PELO MEI'].isin(mei)]
elif not municipio and not bairro and not porte_empresa and not categoria and not simples and not mei: filtered_df = df7.copy()


if  filtered_df['CAPITAL SOCIAL'].min() != filtered_df['CAPITAL SOCIAL'].max():
    range_capital = st.sidebar.slider("Selecione o range de capital social", filtered_df['CAPITAL SOCIAL'].min(), filtered_df['CAPITAL SOCIAL'].max(), (filtered_df['CAPITAL SOCIAL'].min(), filtered_df['CAPITAL SOCIAL'].max()))
    filtered_df = filtered_df[filtered_df['CAPITAL SOCIAL'].between(range_capital[0], range_capital[1])]
else: st.sidebar.write("Capital social (em R$) de cada empresa é:", filtered_df['CAPITAL SOCIAL'].min())


filtered_df['CAPITAL SOCIAL'] = filtered_df['CAPITAL SOCIAL'].astype('float')
capital_df=filtered_df[['CNPJ BASICO', 'CAPITAL SOCIAL']].drop_duplicates()
#-----------------------------------------------------------------------------------------------
# create columns
kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric("Quantidade total de empresas ativas",filtered_df["CNPJ BASICO"].nunique())

kpi2.metric("Quantidade total de estabelecimentos ativos",filtered_df["CNPJ BASICO"].count())


capital = f"R${capital_df['CAPITAL SOCIAL'].astype('float').sum():_.2f}".replace('.', ',').replace('_', '.')
kpi3.metric("Capital social total", capital)

#-----------------------------------------------------------------------------------------------
titulos_guias = ['Quantidade de estabelecimentos', 'Capital social das empresas (R$)']

#------------------------
st.subheader("Dados por categoria")

guia1, guia2 = st.tabs(titulos_guias)

with guia1:
    tipo_cnae_df = filtered_df.groupby(by=["CATEGORIA CNAE PRINCIPAL"], as_index=False)["CNPJ BASICO"].count().sort_values(
        by=["CNPJ BASICO"])
    csv = tipo_cnae_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download dos dados de quantidade', data=csv,
                       file_name="Quantidade_de_estabelecimentos_por_atividade.csv", mime='text/csv')

    fig = px.bar(tipo_cnae_df, x="CATEGORIA CNAE PRINCIPAL", y="CNPJ BASICO", text_auto=True,
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

with guia2:
    capital_tipo_df = filtered_df[['CNPJ BASICO', "CATEGORIA CNAE PRINCIPAL", 'CAPITAL SOCIAL']].drop_duplicates()
    capital_tipo_df = capital_tipo_df.groupby(by=["CATEGORIA CNAE PRINCIPAL"], as_index=False)["CAPITAL SOCIAL"].sum().sort_values(by =["CAPITAL SOCIAL"])

    csv = capital_tipo_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download dos dados de capital', data=csv,
                       file_name="Capital_de_empresas_por_atividade.csv", mime='text/csv')

    fig = px.bar(capital_tipo_df, x="CATEGORIA CNAE PRINCIPAL", y="CAPITAL SOCIAL", text_auto=True,
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

#------------------------
st.subheader("Dados por porte")

guia3, guia4 = st.tabs(titulos_guias)

# Adicionar conteúdo a cada guia
with guia3:
    porte_df = filtered_df.groupby(by=["PORTE DA EMPRESA"], as_index=False)["CNPJ BASICO"].count().sort_values(
        by=["CNPJ BASICO"])
    csv = porte_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download dos dados de quantidade', data=csv,
                       file_name="Quantidade_de_estabelecimentos_por_porte_da_empresa.csv", mime='text/csv')

    fig = px.bar(porte_df, x="PORTE DA EMPRESA", y="CNPJ BASICO", text_auto=True,
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

with guia4:
    capital_porte_df = filtered_df[['CNPJ BASICO', "PORTE DA EMPRESA", 'CAPITAL SOCIAL']].drop_duplicates()
    capital_porte_df = capital_porte_df.groupby(by=["PORTE DA EMPRESA"], as_index=False)["CAPITAL SOCIAL"].sum().sort_values(by =["CAPITAL SOCIAL"])

    csv = capital_porte_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download dos dados de capital', data=csv,
                       file_name="Capital_de_empresas_por_porte.csv", mime='text/csv')

    fig = px.bar(capital_porte_df, x="PORTE DA EMPRESA", y="CAPITAL SOCIAL", text_auto=True,
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)


#------------------------
st.subheader("Dados por CNAE")
guia5, guia6 = st.tabs(titulos_guias)

with guia5:
    cnae_df=filtered_df.groupby(by=["DESCRICAO CNAE"], as_index=False)["CNPJ BASICO"].count().sort_values(by =["CNPJ BASICO"])
    csv = cnae_df.to_csv(index = False).encode('utf-8')
    st.download_button('Download dos dados de quantidade', data=csv, file_name="Quantidade_de_estabelecimentos_por_CNAE.csv", mime='text/csv')

    fig=px.bar(cnae_df, y="DESCRICAO CNAE", x="CNPJ BASICO", text_auto=True,
                 template="seaborn")
    st.plotly_chart(fig,use_container_width=True, height=200)

with guia6:
    capital_cnae_df = filtered_df[['CNPJ BASICO', "DESCRICAO CNAE", 'CAPITAL SOCIAL']].drop_duplicates()
    capital_cnae_df = capital_cnae_df.groupby(by=["DESCRICAO CNAE"], as_index=False)["CAPITAL SOCIAL"].sum().sort_values(by =["CAPITAL SOCIAL"])

    csv = capital_cnae_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download dos dados de capital', data=csv,
                       file_name="Capital_de_empresas_por_CNAE.csv", mime='text/csv')

    fig = px.bar(capital_cnae_df, y="DESCRICAO CNAE", x="CAPITAL SOCIAL", text_auto=True,
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)



# --------------------------------------
st.subheader("Dados por opção Simples")
guia7, guia8 = st.tabs(titulos_guias)

with guia7:
    cnae_df=filtered_df.groupby(by=["OPCAO PELO SIMPLES"], as_index=False)["CNPJ BASICO"].count().sort_values(by =["CNPJ BASICO"])
    csv = cnae_df.to_csv(index = False).encode('utf-8')
    st.download_button('Download dos dados de quantidade', data=csv, file_name="Quantidade_de_estabelecimentos_por_opcao_simples.csv", mime='text/csv')

    fig=px.bar(cnae_df, y="OPCAO PELO SIMPLES", x="CNPJ BASICO", text_auto=True,
                 template="seaborn")
    st.plotly_chart(fig,use_container_width=True, height=200)

with guia8:
    capital_cnae_df = filtered_df[['CNPJ BASICO', "OPCAO PELO SIMPLES", 'CAPITAL SOCIAL']].drop_duplicates()
    capital_cnae_df = capital_cnae_df.groupby(by=["OPCAO PELO SIMPLES"], as_index=False)["CAPITAL SOCIAL"].sum().sort_values(by =["CAPITAL SOCIAL"])

    csv = capital_cnae_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download dos dados de capital', data=csv,
                       file_name="Capital_de_empresas_por_opcao_simples.csv", mime='text/csv')

    fig = px.bar(capital_cnae_df, y="OPCAO PELO SIMPLES", x="CAPITAL SOCIAL", text_auto=True,
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)





# --------------------------------------
st.subheader("Dados por opção MEI")
guia9, guia10 = st.tabs(titulos_guias)

with guia9:
    cnae_df=filtered_df.groupby(by=["OPCAO PELO MEI"], as_index=False)["CNPJ BASICO"].count().sort_values(by =["CNPJ BASICO"])
    csv = cnae_df.to_csv(index = False).encode('utf-8')
    st.download_button('Download dos dados de quantidade', data=csv, file_name="Quantidade_de_estabelecimentos_por_opcao_mei.csv", mime='text/csv')

    fig=px.bar(cnae_df, y="OPCAO PELO MEI", x="CNPJ BASICO", text_auto=True,
                 template="seaborn")
    st.plotly_chart(fig,use_container_width=True, height=200)

with guia10:
    capital_cnae_df = filtered_df[['CNPJ BASICO', "OPCAO PELO MEI", 'CAPITAL SOCIAL']].drop_duplicates()
    capital_cnae_df = capital_cnae_df.groupby(by=["OPCAO PELO MEI"], as_index=False)["CAPITAL SOCIAL"].sum().sort_values(by =["CAPITAL SOCIAL"])

    csv = capital_cnae_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download dos dados de capital', data=csv,
                       file_name="Capital_de_empresas_por_opcao_mei.csv", mime='text/csv')

    fig = px.bar(capital_cnae_df, y="OPCAO PELO MEI", x="CAPITAL SOCIAL", text_auto=True,
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)


# --------------------------------------

with st.expander("ANÁLISE REGIONAL"):
    if not municipio and not bairro:
        st.write("Selecione alguma localização nos filtros para visualizar")
    else:
        st.subheader("Dados por municipío")
        guia11, guia12 = st.tabs(titulos_guias)

        with guia11:
            municipio_cnpj_df=filtered_df[['DESCRICAO MUNICIPIO','CNPJ BASICO']].groupby(['DESCRICAO MUNICIPIO']).count().reset_index().sort_values(by = 'CNPJ BASICO',ascending=False).reset_index(drop  = True)
            csv = municipio_cnpj_df.to_csv(index=False).encode('utf-8')
            st.download_button('Download dos dados de quantidade', data=csv, file_name="Quantidade_de_estabelecimentos_por_municipio.csv", mime='text/csv')

            fig=px.bar(municipio_cnpj_df, x="DESCRICAO MUNICIPIO", y="CNPJ BASICO", text_auto=True, template="seaborn").update_layout(
                xaxis={
                    "range": [municipio_cnpj_df["CNPJ BASICO"].quantile(1), df["CNPJ BASICO"].max()],
                    "rangeslider": {"visible": True},
                    "autorange": True
                }
            )
            st.plotly_chart(fig,use_container_width=True, height=200)

        with guia12:
            capital_municipio_df = filtered_df[['CNPJ BASICO', "DESCRICAO MUNICIPIO", 'CAPITAL SOCIAL']].drop_duplicates()
            capital_municipio_df = capital_municipio_df.groupby(by=["DESCRICAO MUNICIPIO"], as_index=False)[
                "CAPITAL SOCIAL"].sum().sort_values(by=["CAPITAL SOCIAL"])

            csv = capital_municipio_df.to_csv(index=False).encode('utf-8')
            st.download_button('Download dos dados de capital', data=csv,
                               file_name="Capital_de_empresas_por_municipio.csv", mime='text/csv')

            fig = px.bar(capital_municipio_df, x="DESCRICAO MUNICIPIO", y="CAPITAL SOCIAL", text_auto=True, template="seaborn").update_layout(
                xaxis={
                    "range": [capital_municipio_df["CAPITAL SOCIAL"].quantile(1), df["CAPITAL SOCIAL"].max()],
                    "rangeslider": {"visible": True},
                    "autorange": True
                }
            )
            st.plotly_chart(fig,use_container_width=True, height=200)

        st.subheader("Dados por bairro")
        guia13, guia14 = st.tabs(titulos_guias)

        with guia13:
            bairro_cnpj_df=filtered_df[['BAIRRO','CNPJ BASICO']].groupby(['BAIRRO']).count().reset_index().sort_values(by = 'CNPJ BASICO',ascending=False).reset_index(drop  = True)
            csv = bairro_cnpj_df.to_csv(index=False).encode('utf-8')
            st.download_button('Download dos dados', data=csv, file_name="Quantidade_de_estabelecimentos_por_bairro.csv", mime='text/csv')


            fig=px.bar(bairro_cnpj_df, x="BAIRRO", y="CNPJ BASICO", text_auto=True, template="seaborn").update_layout(
                xaxis={
                    "range": [bairro_cnpj_df["CNPJ BASICO"].quantile(1), df["CNPJ BASICO"].max()],
                    "rangeslider": {"visible": True},
                    "autorange": True
                }
            )
            st.plotly_chart(fig,use_container_width=True, height=200)

        with guia14:
            capital_bairro_df = filtered_df[['CNPJ BASICO', "BAIRRO", 'CAPITAL SOCIAL']].drop_duplicates()
            capital_bairro_df = capital_bairro_df.groupby(by=["BAIRRO"], as_index=False)[
                "CAPITAL SOCIAL"].sum().sort_values(by=["CAPITAL SOCIAL"])

            csv = capital_bairro_df.to_csv(index=False).encode('utf-8')
            st.download_button('Download dos dados de capital', data=csv,
                               file_name="Capital_de_empresas_por_bairro.csv", mime='text/csv')

            fig = px.bar(capital_bairro_df, x="BAIRRO", y="CAPITAL SOCIAL", text_auto=True,
                         template="seaborn").update_layout(
                xaxis={
                    "range": [capital_bairro_df["CAPITAL SOCIAL"].quantile(1), df["CAPITAL SOCIAL"].max()],
                    "rangeslider": {"visible": True},
                    "autorange": True
                }
            )
            st.plotly_chart(fig, use_container_width=True, height=200)

st.subheader("Dados de CNPJ")

titulos_guias_tabelas = ['Estabelecimentos', 'Empresas', 'Sócios']
guia15, guia16, guia17 = st.tabs(titulos_guias_tabelas)

with guia15:
    filtered_table_estab = filtered_df.drop(['RAZAO SOCIAL', 'CAPITAL SOCIAL','PORTE DA EMPRESA'], axis=1).fillna(
        "-").astype(str).reset_index(drop=True)
    csv = filtered_table_estab.to_csv(index=False).encode('utf-8')
    st.download_button('Download dos dados de estabelecimentos', data=csv, file_name="dados_cnpj_estabelecimentos.csv", mime='text/csv')
    st.dataframe(filtered_table_estab)

with guia16:
    filtered_table_emp = filtered_df[['CNPJ BASICO','NOME FANTASIA', 'RAZAO SOCIAL', 'CATEGORIA CNAE PRINCIPAL', 'PORTE DA EMPRESA','OPCAO PELO SIMPLES','OPCAO PELO MEI', 'CAPITAL SOCIAL']].drop_duplicates().fillna(
        "-").astype(str).reset_index(drop=True)
    csv = filtered_table_emp.to_csv(index=False).encode('utf-8')
    st.download_button('Download dos dados de empresas', data=csv, file_name="dados_cnpj_empresa.csv", mime='text/csv')
    st.dataframe(filtered_table_emp)

with guia17:
    cnpj_temp = filtered_df['CNPJ BASICO'].drop_duplicates()
    filtered_table_socios = df_socios.loc[df_socios['CNPJ BASICO'].isin(cnpj_temp)].drop_duplicates().fillna(
        "-").astype(str).reset_index(drop=True)
    csv = filtered_table_socios.to_csv(index=False).encode('utf-8')
    st.download_button('Download dos dados de socios', data=csv, file_name="dados_cnpj_socios.csv", mime='text/csv')
    st.dataframe(filtered_table_socios)


gc.collect()
