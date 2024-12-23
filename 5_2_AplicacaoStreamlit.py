# importando as bibliotecas
import streamlit as st
# from langchain_openai import ChatOpenAI
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI # indicação mais atual 
from langchain.prompts import PromptTemplate
import os
import yaml

# lendo o arquivo config.yaml para ter acesso a chave de acesso da OpenAI
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)
os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']

# instanciando um objeto ChatOpenAI
openai = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)

# Criação do template de prompt
template = '''
Você é um analista financeiro.
Escreva um relatório financeiro detalhado para a empresa "{empresa}" para o período {periodo}.

O relatório deve ser escrito em {idioma} e incluir a seguinte análise:
{analise}

Certifique-se de fornecer insights e conclusões para esta seção.
'''

# Instanciando o objeto PromptTemplate
prompt_template = PromptTemplate.from_template(template=template) 

# Opções de escolha para as variáveis que poderão ser escolhida pelo usuário
empresas = ['ACME Corp', 'Globex Corporation', 'Soylent Corp', 'Initech', 'Umbrella Corporation']
trimestres = ['Q1', 'Q2', 'Q3', 'Q4']
anos = [2021, 2022, 2023, 2024]
idiomas = ['Português', 'Inglês', 'Espanhol', 'Francês', 'Alemão']
analises = [
    "Análise do Balanço Patrimonial",
    "Análise do Fluxo de Caixa",
    "Análise de Tendências",
    "Análise de Receita e Lucro",
    "Análise de Posição de Mercado"
]

# Parâmetro de título da página do streamlit
st.title('Gerador de Relatório Financeiro:')

# Criando os selectbox com as opções que poderão ser escolhidas pelo usuário - streamlit
empresa = st.selectbox('Selecione a empresa:', empresas)
trimestre = st.selectbox('Selecione o trimestre:', trimestres)
ano = st.selectbox('Selecione o ano:', anos)
periodo = f"{trimestre} {ano}"
idioma = st.selectbox('Selecione o idioma:', idiomas)
analise = st.selectbox('Selecione a análise:', analises)

# Criando a função do botão ao clicar no botão Gerar Relatório
if st.button('Gerar Relatório'):
    # Assim que clicar no botão as variáveis escolhidas pelo usuário serão preenchidos no prompt
    prompt = prompt_template.format(
        empresa=empresa,
        periodo=periodo,
        idioma=idioma,
        analise=analise
    )

    # Chamada ao modelo passando o prompt completo/preenchido
    response = openai.invoke(prompt)

    st.subheader('Relatório Gerado:') # Subtítulo para o Relatório
    st.write(response.content) # Imprimindo a resposta do modelo
