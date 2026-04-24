import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# 1. Criando dados
dados = {
    "mes": [1,2,3,4,5,6,7,8,9,10,11,12],
    "gasto": [1000,1200,1100,1300,1500,1700,1600,1800,2000,2100,2200,2500]
}

# 2. Transformando em tabela
df = pd.DataFrame(dados)

# 3. Separando entrada (X) e saída (y)
X = df[["mes"]]
y = df["gasto"]

# 4. Criando modelo
modelo = LinearRegression()

# 5. Treinando modelo
modelo.fit(X, y)

# 6. Salvando modelo
with open("modelo.pkl", "wb") as f:
    pickle.dump(modelo, f)

print("Modelo treinado e salvo!")