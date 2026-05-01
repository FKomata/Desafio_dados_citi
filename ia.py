import pandas as pd
import google.generativeai as genai

df = pd.read_csv("basededadoslimpa.csv")


# bancos com maior e menos taxas de recusado
analise_bancos = pd.crosstab(df["Banco"],df["Status_Transacao"])
analise_bancos["total_recusados"] = analise_bancos.sum(axis=1)
analise_bancos["taxa_recusados"] = (analise_bancos["Recusada"]/analise_bancos["total_recusados"])*100
bancos_ordenados = analise_bancos.sort_values(by='taxa_recusados', ascending=False)

#Numerador de categorias
contagem_categoria = df["Categoria"].value_counts()

#nomes suspeitos
analise_clientes = pd.crosstab(df["Nome_Cliente"],df["Status_Transacao"])

ordem_cliente = analise_clientes.sort_values(by="Recusada",ascending=False)

#banco mais utilizado
contagem_banco = df["Banco"].value_counts()


resumo = f"""
Resumo:
-o padrão mais suspeito de ações recusadas esta atrelado ao banco com maior taxa {analise_bancos['taxa_recusados']}
-Os clientes com comportamento mais suspeito são os que tem maior numero de Recusadas no {ordem_cliente}
-A maior tendencia é a que possui maior numero atrelado a ela {contagem_categoria}
-(melhor banco para se investir) Melhor ação para o time financeiro seria o banco com mais chamadas {contagem_banco}
-Banco que se destaca mais negativamente é o banco que tem menor chamadas em {contagem_banco}
"""


genai.configure(api_key="Cole sua chave aqui")
model = genai.GenerativeModel("gemini-2.5-flash")

pergunta = ""

while pergunta != "FIM":
    pergunta = input("Qual é a sua pergunta? ")

    if pergunta == "FIM":
        continue

    prompt = (
        f"{resumo}\n\n"
        f"Com base nesses dados, sempre responda qualquer tipo de pergunta baseado "
        f"nos dados que você recebeu, não importa a pergunta. "
        f"Se você não recebeu nenhuma informação sobre isso, fale 'Não tenho essa informação': "
        f"{pergunta}"
    )

    resposta = model.generate_content(prompt)

    print("\n🤖 Resposta da IA:")
    print(resposta.text)