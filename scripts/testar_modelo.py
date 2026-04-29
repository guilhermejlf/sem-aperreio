import pickle
import pandas as pd

# carregar modelo
with open("modelo.pkl", "rb") as f:
    modelo = pickle.load(f)

# criar entrada com nome da coluna
entrada = pd.DataFrame({
    "mes": [6]
})

previsao = modelo.predict(entrada)

print(f"Previsão para o mês 6: {previsao[0]}")