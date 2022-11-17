import requests
import json
import time
import re
from PRAnalizer import PRAnalizer
from TrataResponse import TrataResponse

linguagemReferencia = "Python"
headers = {'Authorization': 'token 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', 'Accept': 'application/vnd.github.v3+json'}
analizer = PRAnalizer(linguagemReferencia)
dadosDoPR  = analizer.retornaEstrutura();


response = requests.get("https://api.github.com/repos/pandas-dev/pandas/pulls/38758/files", headers=headers)

trataResponse = TrataResponse()
trataResponse.salvaResponseZipado(response, "pandas-dev/pandas", "38758");
exit()


for item in json.loads(response.text):
	linkDocumentoCompleto = item['raw_url']
	itensAlterados = item['patch']

	aux = itensAlterados.split("\n");	

	for item in aux:
		if(analizer.checkIfModifier(item.strip())):
			result 			= analizer.verify(item.strip())
			modifierType 	= analizer.checkModifierType(item.strip())
			dadosDoPR[result][modifierType] += 1
			dadosDoPR['all'][modifierType] += 1

print(dadosDoPR)



