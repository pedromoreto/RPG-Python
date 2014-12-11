__author__ = 'nenodias'

import json

# Teste Quebra é lançado (raise) uma AssertionError
# assert False , 'Erro do Mal'

with open("../../resources/map/mapa1.json") as arquivoJson:
    data = json.load(arquivoJson)
    print(data)

#Gerando String com o JSON
# jsonString = json.dumps({'nome': 'Neno', 'idade': 22,"itens":[{"nome":"moeda", "quantidade": 2},{"nome":"mochila", "quantidade": 1}]}, sort_keys=True, indent=4)
#Gerando o Objeto com JSON
# x = json.loads(jsonString)
#Pegando um Atributo
# print(x.get("itens")[0].get("quantidade"))
# print(dir(x.get("idade")))
# print(jsonString)