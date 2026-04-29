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

print("===============================")
print("Tratamento de CPF")
print("===============================")

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

#topico 5
#data de transação

print("===============================")
print("Tratamento de data no modelo YYYY-MM-DD")
print("===============================")

#utilização das duas funções de tratamento de datas mais o "mixed" para identificar caso haja um mes escrito no meio das datas
df["Data_Transacao"] = pd.to_datetime(df["Data_Transacao"], format="mixed")
df["Data_Transacao"] = df["Data_Transacao"].dt.strftime("%Y-%m-%d")


print(df["Data_Transacao"].head(100))

#topico 6

def convertevalor(linha):
    moeda = linha["Moeda"]
    valor = linha["Valor_Transacao"]
    
    if moeda == "USD":
        return valor * 5.00
    elif moeda == "EUR":
        return valor * 5.50
    elif moeda == "GBP":
        return valor * 6.30
    else:
        return valor
    
#tratamento do codigo tirando os R$ USD EUR GPB e utilização do astype(str) para transforma tudo da coluna em string 
df["Valor_Transacao"] = df["Valor_Transacao"].str.strip()
df["Valor_Transacao"] = df["Valor_Transacao"].astype(str).str.replace('R$', '', regex=False)
df["Valor_Transacao"] = df["Valor_Transacao"].str.replace(r'[GPB]', '', regex=True)
df["Valor_Transacao"] = df["Valor_Transacao"].str.replace(r'[EUR]', '', regex=True)
df["Valor_Transacao"] = df["Valor_Transacao"].str.replace(r'[USD]', '', regex=True)

#transforma em float tirando a , por .
df["Valor_Transacao"] = df["Valor_Transacao"].str.replace(r'[.]', '', regex=True)
df["Valor_Transacao"] = df["Valor_Transacao"].str.replace(r'[,]', '.', regex=True)

df["Valor_Transacao"] = pd.to_numeric(df["Valor_Transacao"], errors='coerce')

df["Valor_Transacao"] = df.apply(convertevalor, axis=1)

df.loc[df["Valor_Transacao"] <= 0 , "Valor_Transacao"] = None


mediana = df["Valor_Transacao"].median()
df["Valor_Transacao"] = df["Valor_Transacao"].fillna(mediana)
df["Valor_Transacao"] = df["Valor_Transacao"].round(2)

df["Moeda"] = "BRL"


print(mediana)
print(df["Moeda"].head(100))
print(df["Valor_Transacao"].head(100))

#topico 7
mapa_tipo = {
    'transferencia': 'Transferência',
    'transferência': 'Transferência',
    'transf.': 'Transferência',
    'pgto.': 'Pagamento',
    'pagamento': 'Pagamento',
    'pix': 'PIX',
    'p.i.x': 'PIX',
    'pix': 'PIX',
    'pixe': 'PIX',
    'depósito': 'Depósito',
    'deposito': 'Depósito',
    'saque': 'Saque',
    'retirada': 'Saque',
    'boleto' : 'Pagamento',
    'ted' : 'Transferência',
    'doc' :  'Transferência'
}

df['Tipo_Transacao'] = (
    df['Tipo_Transacao']
    .str.strip()
    .str.lower()
    .map(mapa_tipo)
    .fillna(df['Tipo_Transacao'].mode()[0])
)

print(df["Tipo_Transacao"].head())
#salvamento do tratamento de dados
#df.to_csv("basededadoslimpa.csv",index=False)