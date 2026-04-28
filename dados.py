import pandas as pd


caminho = 'basededados.csv'

df = pd.read_csv(caminho)

#topico 1.
#tirar os espaços das linhas
print("===============================")
print("remoção de espaços")
print("===============================")
df.columns = df.columns.str.strip()

#topico 2.
#tirar linhas nulas
print("===============================")
print("quantidade de linhas e colunas sem nenhuma alteração")
print("Shape: ", df.shape)
print("===============================")

print("linhas nulas antes da remoção:")
print(df.isnull().sum())

df = df.dropna(how='all')

#linhas nulas depois
print()
print("linhas nulas depois da remoção:")
print(df.isnull().sum())
print("===============================")
print("quantidade de linhas e colunas após saida de nulas")
print("Shape: ", df.shape)
print("===============================")


#topico 3.
#tirar linahs duplicadas

df = df.drop_duplicates()


print("===============================")
print("quantidade de linhas e colunas após remoção de duplicadas")
print("Shape: ", df.shape)
print("===============================")
