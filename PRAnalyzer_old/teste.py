import requests
import json
from PRAnalizer import PRAnalizer

headers = {'Authorization': 'token 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 ', 'Accept': 'application/vnd.github.v3+json'}
link = "https://api.github.com/repos/elastic/elasticsearch/pulls/63100/files"
response = requests.get(link, headers=headers)
analizer = PRAnalizer("JAVA")
dadosDoPR  = analizer.retornaEstrutura();

for arquivo in json.loads(response.text):
	linkDocumentoCompleto = arquivo['raw_url']
	itensAlterados = arquivo['patch']
	aux = itensAlterados.split("\n");	

	

	for item in aux:

		if(analizer.checkIfModifier(item.strip())):
			result 			= analizer.verify(item.strip())
			# print(item.strip() + "    "+ result)
			modifierType 	= analizer.checkModifierType(item.strip())
			dadosDoPR[result][modifierType] += 1
			dadosDoPR['all'][modifierType] += 1
