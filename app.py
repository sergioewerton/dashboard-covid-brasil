# Dashboard COVID-19 Brasil
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import StringIO

# Configuração visual
sns.set_theme(style="darkgrid")

# Baixando os dados
print("Baixando dados...")
url = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv"
response = requests.get(url)
df = pd.read_csv(StringIO(response.text))
print("Dados carregados!")

# Filtrando apenas totais por estado (removendo cidades)
df_estados = df[df['state'] != 'TOTAL']
df_estados = df_estados.dropna(subset=['totalCases', 'deaths'])

# Pegando o dado mais recente de cada estado
df_ultimo = df_estados.sort_values('date').groupby('state').last().reset_index()

# ---- GRÁFICO 1: Total de casos por estado ----
plt.figure(figsize=(14, 6))
df_plot = df_ultimo.sort_values('totalCases', ascending=False).head(15)
sns.barplot(data=df_plot, x='state', y='totalCases', palette='Greens_r')
plt.title('Top 15 Estados com Mais Casos de COVID-19', fontsize=16)
plt.xlabel('Estado')
plt.ylabel('Total de Casos')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('grafico_casos.png')
plt.show()

# ---- GRÁFICO 2: Total de mortes por estado ----
plt.figure(figsize=(14, 6))
df_plot2 = df_ultimo.sort_values('deaths', ascending=False).head(15)
sns.barplot(data=df_plot2, x='state', y='deaths', palette='Reds_r')
plt.title('Top 15 Estados com Mais Mortes por COVID-19', fontsize=16)
plt.xlabel('Estado')
plt.ylabel('Total de Mortes')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('grafico_mortes.png')
plt.show()

# ---- GRÁFICO 3: Evolução de casos no Brasil ao longo do tempo ----
df_brasil = df[df['state'] == 'TOTAL'].copy()
df_brasil['date'] = pd.to_datetime(df_brasil['date'])
df_brasil = df_brasil.sort_values('date')

plt.figure(figsize=(14, 6))
plt.plot(df_brasil['date'], df_brasil['totalCases'], color='#00ff88', linewidth=2)
plt.title('Evolução Total de Casos de COVID-19 no Brasil', fontsize=16)
plt.xlabel('Data')
plt.ylabel('Total de Casos')
plt.tight_layout()
plt.savefig('grafico_evolucao.png')
plt.show()

print("\nDashboard gerado com sucesso!")
print("3 gráficos salvos na pasta do projeto!")
input("\nPressione Enter para fechar...")