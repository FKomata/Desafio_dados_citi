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
#tirar linhas duplicadas

df = df.drop_duplicates()


print("===============================")
print("quantidade de linhas e colunas após remoção de duplicadas")
print("Shape: ", df.shape)
print("===============================")

#topico 4.
#padronização do CPF
df["CPF_Cliente"] = df["CPF_Cliente"].str.strip()
df["CPF_Cliente"] = df["CPF_Cliente"].str.replace(r'[.-]', '', regex=True)
#tirar os . e - para garantir que todos os cpf vao se comportar igual
df["CPF_Cliente"] = df["CPF_Cliente"].fillna("Não informado")
df["CPF_Cliente"] = df["CPF_Cliente"].str.title()
#indicar a parte nao informada 

#filtro para o .loc saber o tamanho da string que ele deve mexer
numerosseparados = (df['CPF_Cliente'].str.len() == 11)

#mudanças que indicam onde dee ser otado o . e a -
df.loc[numerosseparados,"CPF_Cliente"] = (
    df.loc[numerosseparados,"CPF_Cliente"].str[:3] + "." + df.loc[numerosseparados,"CPF_Cliente"].str[3:6] + "." + df.loc[numerosseparados,"CPF_Cliente"].str[6:9] +"-"+ df.loc[numerosseparados,"CPF_Cliente"].str[9:]
)


#salvamento do tratamento de dados
#df.to_csv("basededadoslimpa.csv",index=False)
print(df["CPF_Cliente"].head())

