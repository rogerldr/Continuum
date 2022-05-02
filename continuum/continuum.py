import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from os.path import dirname, abspath

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
    Reads a csv file and returns a dataframe.
    """
    file: str = os.path.join(file_path, file_name)
    df: pd.Dataframe = pd.read_csv(file)
    return df

## Graphs part
def barplots(df: pd.DataFrame, filename: str, title: str):
    """
    Creates a barplot of the dataframe.
    """
    plt.figure(figsize=(15, 60))
    plt.rcParams.update(
        {
            'font.size': 12,
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
  
    ax = df.sort_values(by='perc', ascending=True).plot.bar()
    ax.set_ylabel('Total/Percentage')
    plt.title(f'{title}', y=1.1, fontsize=12)
    plt.autoscale()
    path = os.path.join(graphs_dir, f'{filename}.png')
    plt.savefig(path, bbox_inches="tight", dpi=300)
    plt.show()

def barplot(df: pd.DataFrame, filename: str, title: str):
    """
    Creates a barplot of the dataframe.
    """
    sns.set_color_codes("pastel")
    sns.set_style("whitegrid")
    sns.despine(left=True, bottom=True, top=True, right=True)
    plt.figure(figsize=(15, 6))
    sns.barplot(x=df.index, y=df.values)
    plt.xticks(rotation=65)
    plt.title(f'{title}', y=1.1, fontsize=12)
    path = graphs_dir + f'{filename}.png'
    plt.savefig(path, bbox_inches="tight", dpi=300)
    plt.show()


def correlation(df: pd.DataFrame, filename: str, title: str):
    """
    Creates a correlation matrix of the dataframe.
    """
    plt.figure(figsize=(16, 8))
    sns.heatmap(df.corr(), annot=True)
    path = os.path.join(graphs_dir, f'{filename}.png')
    #plt.title('Heat Map of consumer sensisivity regarding the different types of personal data', y=1.1, fontsize=16)
    plt.title(f'{title}', y=1.1, fontsize=16)
    plt.savefig(path, bbox_inches="tight", dpi=300)
    plt.show()


## Create a dataframe
dfdt: pd.DataFrame = dfcsv('Continuum_tipos_de_dados - DataType.csv', src_dir)
dfdu: pd.DataFrame = dfcsv('Continuum_tipos_de_dados - DataUse.csv', src_dir)

# Working with datatypes dataframe
dfdt = dfdt.set_index('Authors')
# clean dataframe
del dfdt['Privacy concerns?']
dt: pd.DataFrame = pd.DataFrame({'total': dfdt.sum(), 'perc':(dfdt.sum().values / len(dfdu))*100}, index=dfdt.sum().index)


# Working with datause dataframe
dfdu = dfdu.set_index('Authors')
du: pd.DataFrame = pd.DataFrame({'total': dfdu.sum(), 'perc':(dfdu.sum().values / len(dfdu))*100}, index=dfdu.sum().index)

def main():
    ## Barplots
    barplots(dt, 'barplot_datatype', title='Nome maneiro')
    barplots(du, 'barplot_datause', title='Total of percentage  regarding literature review and consumer concern')

    ## Correlation plot
    correlation(dfdt, 'correlation_datatype', title='Correlation of consumer concern regarding the different types of personal data')
    correlation(dfdu, 'correlation_datause', title='Correlation of consumer concern regarding the different types of personal data')

if __name__ == "__main__":
    main()