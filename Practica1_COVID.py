# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PwcuGiJY23ejKu0CFP1DjH-plW0Upufj

Importacion de Datos
"""

import requests
import io
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
from typing import Tuple, List


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def print_tabulate(df: pd.DataFrame):
    print(tabulate(df, headers=df.columns, tablefmt='orgtbl'))

def get_csv_from_url(url: str) -> pd.DataFrame:
    s = requests.get(url).content
    return pd.read_csv(io.StringIO(s.decode('utf-8')))

def Covid() -> pd.DataFrame:
    soup = get_soup("https://es.wikipedia.org/wiki/Pandemia_de_COVID-19_en_México")
    list_of_lists = []
    rows = soup.find_all("table")[7].find_all('tr')
    for row in rows[1:]:
        columns = row.find_all('td')
        listado_de_valores_en_columnas = [column.text.strip() for column in columns]
        list_of_lists.append(listado_de_valores_en_columnas)
    return pd.DataFrame(list_of_lists, columns=["Estados","Casos","Cantidad de Fallecidos","porcentaje de Fallecidos","Cantidad de Recuperados","porcentaje de Recuperados","Casos por 100,000 habitantes","Reporte"])

df = Covid()

df.head()

df.to_csv("Estimadores_Covid.csv", index=False)

"""Análisis de Datos

Import librerias que usaremos para graficas, analysis y tablas
"""

import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols

df_Modif = pd.read_csv("Estimadores_Covid.csv")
#Eliminamos las columnas mencionadas despues de .drop que sera el data fram de df_Modif
df_Modif = df_Modif.drop(['porcentaje de Fallecidos', 'porcentaje de Recuperados','Casos por 100,000 habitantes','Reporte'], axis=1)

df_Modif.head(5)

#Aqui agrupamos las columnas de cantidad de fallecidoa y la de cantidad de recuperados y la ponemos con la columna de casos
df_by_casos = df_Modif.groupby(["Cantidad de Fallecidos", "Cantidad de Recuperados"])[["Casos"]].aggregate(pd.DataFrame.sum)
df_by_casos.head(5)

"""Aqui le asinamos ceros a los valores que tienen "null", es decir que son nulos """

#Aqui le asinamos ceros a los valores que tienen "null", con .fillna(0), es decir que son nulos 
df_Help = df_Modif[["Cantidad de Recuperados","Cantidad de Fallecidos","Casos"]].fillna(0)
df_Help.columns = ['Cantidad_de_Recuperados','Cantidad_de_Fallecidos','Casos']
df_Help.head(5)

"""Aqui observamos la informacion y tipos de datos que tiene el df_Help, observando que tiene datos que son tipo object, es decir que tienen texto , entonces tendremos que limiparlos para que sean de tipo texto """

df_Help.info()

"""Aqui elimine las dos últimas filas y las dos últimas columnas del Data Frame pues son 0. Pero no modifico el DF original, lo asigno a uno nuevo."""

df_Help_2 = df_Help.drop([0,1,34,35], axis = 0).reset_index().drop(['index'],axis = 1)

df_Help_2

"""Aqui modifique me fije que las columnas de casos, cantidad_de_fallecidos,cantidad_de_recuperados son de tipo object por que tienen "\xa" entre los numeros y eso hay que eliminarlo. para que quede solo dato numerico."""

#Aqui modifique la primer columna de"Cantidad_de_Recuperados" para que quedaran puros datos numericos enteros.
df_Help_2["Cantidad_de_Recuperados"] = df_Help_2["Cantidad_de_Recuperados"].apply(lambda x: x.replace(u'\xa0', u''))
df_Help_2["Cantidad_de_Recuperados"]= df_Help_2["Cantidad_de_Recuperados"].astype(int)
df_Help_2["Cantidad_de_Recuperados"]

#Aqui modifique la segunda columna de"Cantidad_de_Fallecidos" para que quedaran puros datos numericos enteros.
df_Help_2["Cantidad_de_Fallecidos"] = df_Help_2["Cantidad_de_Fallecidos"].apply(lambda x: x.replace(u'\xa0', u''))
df_Help_2["Cantidad_de_Fallecidos"]= df_Help_2["Cantidad_de_Fallecidos"].astype(int)
df_Help_2["Cantidad_de_Fallecidos"]

#Aqui modifique la Tercer columna de"Casos" para que quedaran puros datos numericos enteros.
df_Help_2["Casos"] = df_Help_2["Casos"].apply(lambda x: x.replace(u'\xa0', u''))
df_Help_2["Casos"] = df_Help_2["Casos"].astype(int)
df_Help_2["Casos"]

"""Aqui se hara la tabla de los casos que hay por estado"""

df_by_casosporEdo = df_Modif.groupby(["Estados"])[['Casos']].aggregate(pd.DataFrame.sum)
df_by_casosporEdo.head(5)

#Aqui tabulamos los datos dela nueva base de datos llamada df_Help_2
print_tabulate(df_Help_2.head(5))

"""Grafico de Caja de Bigotes """

df_Help_2.loc[:,'Cantidad_de_Recuperados'].plot(kind='box',figsize=(4,4))
plt.title('Grafica de caja de Casos de Covid en Mexico') #Aqui es para agregar el titulo
plt.ylabel('Casos Mexico')
plt.grid(linestyle='--')
plt.tight_layout()

"""Aqui obtengo la info del segundo df_Help_2 los tipos de datos del df """

df_Help_2.info()

"""Aqui hacemos el plot de las columnas de "Cantidad_de_Recuperados" con  "Casos""""

df_Help_2.plot(x="Cantidad_de_Recuperados", y = 'Casos', legend=False, figsize=(4,4))
plt.title("Plot de Cant Recuperados")  #Aqui es para agregar titulo al grafico

"""Aqui hacemos el plot de las columnas de "Cantidad_de_Fallecidos" con "Casos""""

df_Help_2.plot(x="Cantidad_de_Fallecidos", y='Casos', legend=False, figsize=(4,4))
plt.title("Plot de Cant fallecidos")  #Aqui es para agregar titulo al grafico

"""Hacemos dos graficos en una sola ventana """

#Dos gráficos en una sola notación

plt.subplot(121) #GRAFICO 1
plt.plot(df_Help_2.loc[:,'Cantidad_de_Recuperados'],df_Help_2.loc[:,'Casos'])
plt.ylabel('Casos')
plt.xlabel('Cantidad de recuperados')
plt.tight_layout()
plt.title("Gráfico de Cant fallecidos") #Aqui es para agregar titulo al grafico 1
plt.subplot(122) #GRAFICO 2
plt.plot(df_Help_2.loc[:,'Cantidad_de_Fallecidos'],df_Help_2.loc[:,'Casos'])
plt.xlabel('Cantidad de fallecidos')
plt.tight_layout()
plt.title("Gráfico de Cant fallecidos")  #Aqui es para agregar titulo al grafico 2

#DOS GRAFICOS DE PUNTOS en una sola notación

plt.subplot(121) #GRAFICO 1
plt.plot(df_Help_2.loc[:,'Cantidad_de_Recuperados'],df_Help_2.loc[:,'Casos'],'o')
plt.ylabel('Casos')
plt.xlabel('Cantidad de recuperados')
plt.tight_layout()
plt.title("Gráfico de Cant fallecidos") #Aqui es para agregar titulo al grafico 1
plt.subplot(122) #GRAFICO 2
plt.plot(df_Help_2.loc[:,'Cantidad_de_Fallecidos'],df_Help_2.loc[:,'Casos'],'o')
plt.xlabel('Cantidad de fallecidos')
plt.tight_layout()
plt.title("Gráfico de Cant fallecidos")  #Aqui es para agregar titulo al grafico 2

#DOS GRAFICOS PUNTEADOS en una sola notación.
plt.subplot(121) #GRAFICO 1
plt.plot(df_Help_2.loc[:,'Cantidad_de_Recuperados'],df_Help_2.loc[:,'Casos'],'--')
plt.ylabel('Casos')
plt.xlabel('Cantidad de recuperados')
plt.tight_layout()
plt.title("Gráfico de Cant fallecidos") #Aqui es para agregar titulo al grafico 1
plt.subplot(122) #GRAFICO 2
plt.plot(df_Help_2.loc[:,'Cantidad_de_Fallecidos'],df_Help_2.loc[:,'Casos'],'--')
plt.xlabel('Cantidad de fallecidos')
plt.tight_layout()
plt.title("Gráfico de Cant fallecidos")  #Aqui es para agregar titulo al grafico 2

#DOS GRAFICOS CON LAMINA en una sola notación.
plt.subplot(121) #GRAFICO 1
plt.plot(df_Help_2.loc[:,'Cantidad_de_Recuperados'],df_Help_2.loc[:,'Casos'])
plt.ylabel('Casos')
plt.xlabel('Cantidad de Cant recuperados')
plt.title("Gráfico de Cant fallecidos") #Aqui es para agregar titulo al grafico 1
plt.grid()
plt.tight_layout()
plt.subplot(122) #GRAFICO 2
plt.plot(df_Help_2.loc[:,'Cantidad_de_Fallecidos'],df_Help_2.loc[:,'Casos'])
plt.xlabel('Cantidad de fallecidos')
plt.title("Gráfico de Cant fallecidos")  #Aqui es para agregar titulo al grafico 2
plt.grid()
plt.tight_layout()

"""Gráfico de casos confirmados con colores """

df_Help_2.sort_values('Casos').reset_index().drop('index',axis = 1).plot(kind = 'line')
plt.title("Plot Casos Confirmados COVID en México")  #Aqui es para agregar titulo al grafico

"""Estadistica DESCRIPTIVA"""

#Estadistica DESCRIPTIVA de datos
df_Help_2.describe()

Gráfico de barras de FRECUENCIA

#Gráfica de barras de FRECUENCIAS de 3 columnas de casos
df_Help_2.sort_values('Casos').reset_index().drop('index',axis = 1).plot(kind = 'bar')
plt.tight_layout()
plt.title("Frecuencias de Casos confirmados COVID en México")  #Aqui es para agregar titulo al grafico

DJ = pd.DataFrame({'Estados':[24098,45952,27465,8789,10285]},index = ['Aguascalientes','BajaCalifornia','BajaCalif_Sur','Campeche','Chiapas'])
DJ.plot(kind='bar')
plt.title("Casos confirmados por Estado")  #Aqui es para agregar titulo al grafico

"""Histograma de casos"""

import matplotlib.pyplot as plot

histograma=df_Help_2["Casos"]
intervalos = [10000,15000,20000,30000,40000] #indicamos los extremos de los intervalos
plot.hist(x=df_Help_2["Casos"], bins=intervalos, color='#F2AB6D', rwidth=0.85,)
plot.title('Histograma de casos confirmados por Estados')
plot.xlabel('Casos')
plot.ylabel('Estados')
plot.xticks(intervalos)

plot.show() #dibujamos el histograma

DJ2 = pd.DataFrame({'Casos confirmados':[24098,45952,27465,8789,10285]},index = ['Aguascalientes','Baja Calif Norte','Baja Calif Sur','Campeche','Chiapas'])
DJ2.plot(kind = 'line')

"""Aqui sacamos el p valor con Anova"""

#Sacamos el p-valor
modl = ols("Cantidad_de_Recuperados ~ Casos", data=df_Help_2).fit()
anova_df = sm.stats.anova_lm(modl, typ=2)
if anova_df["PR(>F)"][0] < 0.005:
    print("hay diferencias")
    print(anova_df)
    # Prueba tukey
    # imprimir los resultados
else:
    print("No hay diferencias")