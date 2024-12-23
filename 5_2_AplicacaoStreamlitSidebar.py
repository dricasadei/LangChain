# importando as bibliotecas
import streamlit as st
#from langchain_openai import ChatOpenAI
#from langchain.chat_models import ChatOpenAI
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
Formate o relatório utilizando Markdown.
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
# inclusão do sidebar - que cria uma barra lateral. Nesse caso, as opções a serem selecionadas ficarão a esquerda e ficará mais
# página livre para o relatório gerado.
empresa = st.sidebar.selectbox('Selecione a empresa:', empresas)
trimestre = st.sidebar.selectbox('Selecione o trimestre:', trimestres)
ano = st.sidebar.selectbox('Selecione o ano:', anos)
periodo = f"{trimestre} {ano}"
idioma = st.sidebar.selectbox('Selecione o idioma:', idiomas)
analise = st.sidebar.selectbox('Selecione a análise:', analises)

# Criando a função do botão ao clicar no botão Gerar Relatório
if st.sidebar.button('Gerar Relatório'):
    prompt = prompt_template.format(
        empresa=empresa,
        periodo=periodo,
        idioma=idioma,
        analise=analise
    )

    # Chamada ao modelo passando o prompt completo/preenchido
    response = openai.invoke(prompt)

    st.subheader('Relatório Gerado:')
    st.write(response.content) # Imprimindo a resposta do modelo
