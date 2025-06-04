# EU Logistic Performance Index Analysis

[🚀 Acesse a aplicação online](https://eu-lpi-analysis.streamlit.app)

Análise detalhada do desempenho logístico dos países da União Europeia, com base no Índice de Desempenho Logístico (LPI). Aplicação interativa para explorar dados, realizar análises estatísticas e ranqueamentos multicritério (TOPSIS, DEA).

---

## Índice

- [Sobre](#sobre)
- [Acesso à Aplicação](#acesso-à-aplicação)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Instalação e Uso Local](#instalação-e-uso-local)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Licença](#licença)
- [Contato](#contato)

---

## Sobre

Este projeto é fruto da Iniciação Científica intitulada **"Avaliação do Desempenho Logístico dos Países da União Europeia com Base no Índice de Desempenho Logístico"**. O objetivo principal é fornecer uma ferramenta que permita a análise e o ranqueamento dos países da UE conforme indicadores logísticos, utilizando dados do World Bank.

A aplicação, desenvolvida em Python com Streamlit, integra métodos estatísticos e multicritério para facilitar a compreensão e a tomada de decisões baseada em dados.

---

## Acesso à Aplicação

Acesse a aplicação online sem necessidade de instalação:

👉 [https://eu-lpi-analysis.streamlit.app](https://eu-lpi-analysis.streamlit.app)

---

## Funcionalidades

- Exploração interativa dos dados do Índice de Desempenho Logístico (LPI)
- Análises estatísticas descritivas detalhadas
- Ranqueamento com o método TOPSIS configurável por critérios e pesos
- Avaliação de eficiência via Análise Envoltória de Dados (DEA)
- Visualizações gráficas dinâmicas e exportação dos resultados
- Interface web intuitiva e responsiva via Streamlit

---

## Tecnologias

- Python 3.10+
- Pandas, NumPy, SciPy, scikit-learn
- Streamlit para interface interativa
- Matplotlib, Seaborn e Plotly para visualizações
- cvxpy para modelo DEA
- Outras dependências detalhadas em `requirements.txt`

---

## Instalação e Uso Local

Para rodar a aplicação localmente:

1. Clone o repositório

```
git clone https://github.com/seu-usuario/eu-lpi-analysis.git
cd eu-lpi-analysis
```

2. Crie e ative um ambiente virtual

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências

```
pip install -r requirements.txt
```

4. Execute a aplicação

```
streamlit run app.py
```

5. Abra no navegador

```
http://localhost:8501
```

## Estrutura do Projeto

```
eu-lpi-analysis/
│
├── data/                  # Dados brutos e processados
├── src/                   # Código-fonte
│   ├── models/            # Implementação de TOPSIS, DEA, etc.
│   ├── plots/             # Funções para visualizações
│   └── utils/             # Utilitários auxiliares
├── app.py                 # Aplicação principal Streamlit
├── requirements.txt       # Dependências
└── README.md              # Documentação do projeto
└── LICENSE                # Licença
```

## Licença
Distribuído sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## Contato
Luis Enrique Krulikowski

LinkedIn: linkedin.com/in/luis-krulikowski
