# Pandas é uma biblioteca para análise de dados (dataframes)
import pandas as pd   
# Biblioteca de gráficos em cima do matplolib (mais avançado) 
import seaborn as sns
# Biblioteca mais utilizada para visualização de gráfico em python 
import matplotlib.pyplot as plt
# Biblioteca para navegação do sistema operacional 
import os
# Navega dentro dos diretórios e caminhos do os
from os.path import dirname, abspath

# A biblioteca 'OS' foi utilizada para que o programa conseguisse abstrair a localização dos arquivos necessários para criação dos gráficos ou resultados - "Reprodutibilidade em qualquer máquina".  
# Diretório Pai onde está a pasta continuum 
parent_dir: str = dirname(dirname(abspath(__file__)))
# Onde está esse arquivo continuum.py 
here: str = abspath(dirname(__file__))
# Diretório onde estão os arquivos csv
src_dir: str = os.path.join(parent_dir, 'src/')
# Onde serão salvos os gráficos 
graphs_dir: str = os.path.join(parent_dir, 'graphs/')
 
def dfcsv(file_name: str, file_path: str) -> pd.DataFrame:
    """
    Lê arquivo csv e retorna um dataframe.
    
    Args: 
        file_name(str): Nome do arquivo
        file_path(str): Diretório onde está localizado o arquivo
        
    Returns:
        pd.DataFrame: Uma tabela
    """
    # Junta o caminho do diretório com o nome do arquivo
    file: str = os.path.join(file_path, file_name)
    # Cria o dataframe através da leitura do arquivo csv
    df: pd.Dataframe = pd.read_csv(file)
    # Retorna o dataframe criado acima
    return df

## Graphs part
def barplots(df: pd.DataFrame, filename: str, title: str):
    """
    Cria um gráfico de barras baseado no dataframe recebido.
    
    Args: 
        df(pd.DataFrame): Dataframe
        filename(str): Nome do arquivo do gráfico a ser salvo
        title(str): Título do gráfico    
    """
    # Dimensionamento da figura 
    plt.figure(figsize=(15, 60))
    # Design da imagem e alteração de padrão
    # Todos esses parâmetros encontrados na documentação presente na internet <https://matplotlib.org/stable/tutorials/introductory/customizing.html> - 'Design de gráfico'
    plt.rcParams.update(
            {
            "font.size": 12,
            "figure.facecolor": "w",
            "axes.facecolor": "w",
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.spines.bottom": False,
            "xtick.top": False,
            "xtick.bottom": False,
            "ytick.right": False,
            "ytick.left": False,
            }
            )
    # Comando para plotar o gráfico pelos valores de porcentagem em ordem crescente.
    ax = df.sort_values(by='perc', ascending=True).plot.bar()
    # Definindo nome do eixo y
    ax.set_ylabel('Total/Percentage')
    # Definindo o título do gráfico
    plt.title(f'{title}', y=1.1, fontsize=12)
    # Imagem auto escalada (estava cortando os nomes). Esse comando serviu para que os nomes coubessem na imagem. 
    plt.autoscale()
    # Criando caminho onde será salvo o arquivo
    path = os.path.join(graphs_dir, f'{filename}.png')
    # Comando para salvar o gráfico
    plt.savefig(path, bbox_inches="tight", dpi=300)
    # Comando de exibição do gráfico na tela
    plt.show()

def correlation(df: pd.DataFrame, filename: str, title: str):
    """
    Criação da correlação matricial no dataframe.
    """
    # Definindo o tamanho da figura
    plt.figure(figsize=(16, 8))
    # Comando para criar o gráfico - sns = seaborn cujo design gráfico é mais sofisticado - annot = indice de correlação anotado dentro dos quadrantes.  
    sns.heatmap(df.corr(), annot=True)
    # Criando o caminho onde será o arquivo 
    path = os.path.join(graphs_dir, f'{filename}.png')
    # Definindo o título do gráfico
    plt.title(f'{title}', y=1.1, fontsize=16)
    # Comando para salvar a figura
    plt.savefig(path, bbox_inches="tight", dpi=300)
    # Exibir na tela
    plt.show()



# Função principal para chamar todas as outras funções e fazer o programa rodar. 
def main(): 
    
    ## Momento de criação do dataframe
    dfdt: pd.DataFrame = dfcsv('Continuum_tipos_de_dados - DataType.csv', src_dir)
    dfdu: pd.DataFrame = dfcsv('Continuum_tipos_de_dados - DataUse.csv', src_dir)

    # Colocando nomes dos autores relacionados ao datatypes dataframe
    dfdt = dfdt.set_index('Authors')
    # Limpando coluna "inútil" no dataframe - todos os valores positivos
    del dfdt['Privacy concerns?']
    # Somatório dos dados feitos no excel e que por sua vez foram agregados tanto no somatório, valores percentuais correspondentes aos papers encontrados por cada autor. Esse comando é a base central da pesquisa, pois é nela que os dados são a fonte geradora para a construção do continnum de sensibilidade dos consumidores. Lembrando que associa-se ao data types. 
    dt: pd.DataFrame = pd.DataFrame({'total': dfdt.sum(), 'perc':(dfdt.sum().values / len(dfdt))*100}, index=dfdt.sum().index)


    # Colocando nomes dos autores relacionados ao datause dataframe.
    dfdu = dfdu.set_index('Authors')
    # Idem ao comando anterior, porém voltado para a confecção do gráfico data uses. 
    du: pd.DataFrame = pd.DataFrame({'total': dfdu.sum(), 'perc':(dfdu.sum().values / len(dfdu))*100}, index=dfdu.sum().index)
    
    ## Barplots
    barplots(dt, 'barplot_datatype', title='Nome maneiro')
    barplots(du, 'barplot_datause', title='Total of percentage  regarding literature review and consumer concern')

    ## Correlation plot
    correlation(dfdt, 'correlation_datatype', title='Correlation of consumer concern regarding the different types of personal data')
    correlation(dfdu, 'correlation_datause', title='Nome maneiro')

# Convenção que se associa a função principal. 
if __name__ == "__main__":
    main()