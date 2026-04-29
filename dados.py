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
    if pd.isna(valor):
        return None
    if moeda == "USD":
        return round(valor * 5.00, 2)
    elif moeda == "EUR":
        return round(valor * 5.50, 2)
    elif moeda == "GBP":
        return round(valor * 6.30, 2)
    else:
        return round(valor, 2)

    
def normaliza_valor(v):
    if pd.isna(v) or str(v).strip() in ('', 'nan'):
        return None
    v = str(v).strip()
    tem_virgula = ',' in v
    tem_ponto   = '.' in v
    if tem_virgula and tem_ponto:
        v = v.replace('.', '').replace(',', '.')
    elif tem_virgula:
        v = v.replace(',', '.')
    try:
        return float(v)
    except ValueError:
        return None
    
#tratamento do codigo tirando os R$ USD EUR GPB e utilização do astype(str) para transforma tudo da coluna em string 
df["Moeda"] = df["Moeda"].astype(str).str.strip()
df["Valor_Transacao"] = df["Valor_Transacao"].astype(str).str.strip()
df["Valor_Transacao"] = df["Valor_Transacao"].str.replace(r'USD|EUR|GBP|R\$', '', regex=True).str.strip()
#transforma em float tirando a , por .

df["Valor_Transacao"] = df["Valor_Transacao"].apply(normaliza_valor)

df["Valor_Transacao"] = pd.to_numeric(df["Valor_Transacao"], errors='coerce')

df["Valor_Transacao"] = df.apply(convertevalor, axis=1)

df.loc[df["Valor_Transacao"] <= 0 , "Valor_Transacao"] = None
df.loc[df["Valor_Transacao"] > 1000000, "Valor_Transacao"] = None

mediana = df["Valor_Transacao"].median()
df["Valor_Transacao"] = df["Valor_Transacao"].fillna(mediana).round(2)
df["Valor_Transacao"] = df["Valor_Transacao"].round(2)

df["Moeda"] = "BRL"


print(mediana)
print(df["Moeda"].head(25))
print(df["Valor_Transacao"].head(25))

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
    'dep.' : "Depósito",
    'saque': 'Saque',
    'retirada': 'Saque',
    'boleto' : 'Pagamento',
    'ted' : 'Transferência',
    'doc' :  'Transferência',
    'resgate': 'Saque',
}

df['Tipo_Transacao'] = (
    df['Tipo_Transacao']
    .str.strip()
    .str.lower()
    .map(mapa_tipo)
    .fillna(df['Tipo_Transacao'].mode()[0])
)
print(df["Tipo_Transacao"].unique())
print(df["Tipo_Transacao"].head())

#topico 8
mapa_status = {
    "aprovada" : "Aprovada",
    "Aprovado" : "Aprovada",
    "autorizada" : "Aprovada",
    "aprov." : "Aprovada",
    "Bloqueada" : "Recusada",
    "recusada" : "Recusada",
    "negada" : "Recusada",
    "boqueada" : "Recusada",
    "recus." : "Recusada",
    "pendente" : "Pendente",
    "em processamento" : "Pendente",
    "aguardando" : "Pendente",
    "pend." : "Pendente"
}



df['Status_Transacao'] = (
    df["Status_Transacao"]
    .str.strip()
    .str.lower()
    .map(mapa_status)
    .fillna(df['Status_Transacao'].mode()[0])
)
print(df['Status_Transacao'].unique())

print(df["Status_Transacao"].head())

# #topico 9

df["Nome_Cliente"] = df["Nome_Cliente"].str.replace(r"_"," ",regex=False)
df["Nome_Cliente"] = df["Nome_Cliente"].str.split().str.join(" ")
df["Nome_Cliente"] = df["Nome_Cliente"].str.title()
df["Nome_Cliente"] = df["Nome_Cliente"].str.replace(r'\b(\w+)\s+\1\b', r'\1', regex=True)

print(df["Nome_Cliente"].head(355))

#topico 10 
df["Num_Parcelas"] = df["Num_Parcelas"].str.replace(r"parcelas","",regex=False)
df["Num_Parcelas"] = df["Num_Parcelas"].str.replace(r"à vista","1",regex=False)
df["Num_Parcelas"] = df["Num_Parcelas"].str.replace(r"X","",regex=False)
df["Num_Parcelas"] = df["Num_Parcelas"].str.replace(r"x","",regex=False)
df["Num_Parcelas"] = df["Num_Parcelas"].str.replace(r".0","",regex=False)
df["Num_Parcelas"] = df["Num_Parcelas"].str.strip()
df["Num_Parcelas"] = pd.to_numeric(df["Num_Parcelas"], errors='coerce')

print(df["Num_Parcelas"].head())

#topico 11
df["Taxa_Servico"] = pd.to_numeric(df["Taxa_Servico"] , errors= "coerce")
df["Taxa_Servico"] = abs(df["Taxa_Servico"])
media =  df["Taxa_Servico"].mean().round(2)
df["Taxa_Servico"] = df["Taxa_Servico"].fillna(media)

print(media)
print(df["Taxa_Servico"].head(31))

#topico 12

df["Valor_Transacao"] = pd.to_numeric(df["Valor_Transacao"], errors="coerce").fillna(0)
df["Taxa_Servico"] = pd.to_numeric(df["Taxa_Servico"], errors="coerce").fillna(0)
df["Valor_Final"] = pd.to_numeric(df["Valor_Final"], errors="coerce").fillna(0)

def verificaFinal(linha):
    taxa = linha["Taxa_Servico"]
    valorFinal = linha["Valor_Final"]
    deposito = linha["Valor_Transacao"]

    valor_atual = round(linha["Valor_Final"], 2)

    esperado = round(deposito + taxa, 2)

    if pd.notna(taxa):
        taxa = taxa
    else:
        taxa = 0
    if pd.notna(deposito):
        deposito = deposito
    else:
        deposito = 0

    if(valorFinal < deposito or valorFinal != (deposito + taxa)):
        return esperado
    return valor_atual  

df["Valor_Final"] = df.apply(verificaFinal, axis=1)

print(df["Valor_Final"].head())

# salvamento do tratamento de dados
df.to_csv("basededadoslimpa.csv",index=False)