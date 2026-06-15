import pandas as pd
import numpy as np
# pip install matplotlib
import matplotlib.pyplot as plt

# Preparando os dados
try:
    print('Obtendo os dados...')
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'


    # utf-8, iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep = ';', encoding = 'iso-8859-1')
    #print(df_ocorrencias.head())

    #delimitando as variáveis
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]

    # Totalizando os roubos pelo municípios
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()

    # Ordenando o dataframe
    df_roubo_veiculo = df_roubo_veiculo.sort_values(by = 'roubo_veiculo', ascending=False)

    #print(df_roubo_veiculo.head(10))


except Exception as e:
    print(f'Erro ao obter dados: {e}')


# Obtendo as medidas
try:
    print('Calculando as medidas...')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia_decimal = abs((media_roubo_veiculo - mediana_roubo_veiculo)/ mediana_roubo_veiculo)
    distancia_percentual = abs((media_roubo_veiculo - mediana_roubo_veiculo)/ mediana_roubo_veiculo * 100)


    print('Medidas de Tendência Central')
    print(30 * '-')
    print(f'Média: {media_roubo_veiculo:.2f}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância decimal: {distancia_decimal:.2f}')
    print(f'Distância percentual: {distancia_percentual:.2f} %')


except Exception as e:
    print(f'Erro ao processar medidas: {e}')


# Obtendo a distribuição
try:
    print('\nProcessando os quartis...')

    q1 = np.quantile(array_roubo_veiculo, .25)
    q3 = np.quantile(array_roubo_veiculo, .75)

    print('\nQuartis')
    print(30 * '-')

    print(f'Q1: {q1}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Q3: {q3}')

    # Municípios com menos roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]
    
    # Municípios com mais roubos
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]


    print('\nMunicípios com menos casos de roubos de veículos: ')
    print(30 * '-')
    print(df_roubo_veiculo_menores.sort_values(by = 'roubo_veiculo', ascending=True))

    print('\nMunicípios com mais casos de roubos de veículos: ')
    print(30 * '-')
    print(df_roubo_veiculo_maiores)


except Exception as e:
    print(f'Erro ao obter a distribuição: {e}')



# obtendo medidas de dispersão
try:
    # Amplitude Total
    # amplitude = maximo - minimo
    # Resultado mais próximo do minimo, baixa dispersão.
    # Se for 0, quer dizer que todos os dado são iguais
    # Resultado mais próximo do maximo, alta dispersão.
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo

    print('\nMedidas de Dispersão')
    print(30 * '=')
    print(f'Máximo: {maximo}')
    print(f'Mínimo: {minimo}')
    print(f'Amplitude Total: {amplitude}')

except Exception as e:
    print(f'Erro ao calcular medidas de dispersão {e}')


# Calculando outliers
try:
    # IQR (Intervalo Interquartil) - Amplitude dos 50% dos dados mais centrais.
    # IQR = Q3 - Q1
    # Ele ignora os valores extremos. Max e Min estão fora do IQR
    # Não sofre interferência dos valores extremos.
    # Quanto mais próximo do zero, mais homogênenos são os dados
    # Quanto mais próximo do Q3, menos homogênenos são os dados (Mais dispersos)

    iqr = q3 - q1

    # Limite inferior:
    # É uma medida que vai identificar como outliers, os valores abaixo dele.

    limite_inferior = q1 - (1.5 * iqr)

    # Limite superior:
    # É uma medida que vai identificar como outliers, os valores acima dele.

    limite_superior = q3 + (1.5 * iqr)


    print('\nMedidas de Dispersão')
    print(30 * '=')
    print(f'IQR: {iqr}')
    print(f'Mínimo: {minimo}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Mediana: {mediana_roubo_veiculo}') # Q2
    print(f'Q3: {q3}')
    print(f'Limite Superior: {limite_superior}')
    print(f'Máximo: {maximo}')


except Exception as e:
    print(f'Erro ao calcular os limites: {e}')



# Exibindo os outliers
try:
    # outliers superiores
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]

    # outliers sinferiores
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]


    print('\nMunicípios com Outliers Inferiores')
    print(30 * '=')
    
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print(f'\nNão existe Outliers inferiores!')

    else:
        print(df_roubo_veiculo_outliers_inferiores.sort_values(by = 'roubo_veiculo', ascending = True))


    print('\nMunicípios com Outliers Superiores')
    print(30 * '=')
    
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print(f'\nNão existe Outliers Superiores!')

    else:
        print(df_roubo_veiculo_outliers_superiores)


except Exception as e:
    print(f'Erro ao Calcular outliers: {e}')


# Visualizando os dados
try:
    # Plotando o Gráfico Colunas
    
    
    plt.figure(figsize=(16, 8))

    df_roubo_veiculo_maiores = df_roubo_veiculo_maiores.sort_values(by ='roubo_veiculo', ascending = False).head(10)
    
    
    # Plotando o Gráfico Colunas
    plt.bar(df_roubo_veiculo_maiores['munic'], df_roubo_veiculo_maiores['roubo_veiculo'])
    plt.title('Municípios com Maiores Roubos')
    plt.show()

except Exception as e:
    print(f'Erro ao plotar o gráfico: {e}')