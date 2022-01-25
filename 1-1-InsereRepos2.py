import requests
from bs4 import BeautifulSoup
import time
from Queue import Sender


sender = Sender("repos_problematicos")

def enviarRequest(url):
    time.sleep(5)
    result = requests.get(url)
    if(result.status_code == 200):
        return result

    else:
        time.sleep(10)
        result = requests.get(url)
        if(result.status_code == 200):
            return result
        else:    
            return False

total = 0
for x in range(1,101):
    # url ="https://github.com/search?p="+str(x)+"&q=is%3Apublic+language%3APython+fork%3Afalse+mirror%3Afalse+archived%3Afalse+stars%3A%3E3000+sort%3Astars-asc&type=Repositories"
    url ="https://github.com/search?o=desc&p="+str(x)+"&q=is%3Apublic+language%3AJavascript+fork%3Afalse+mirror%3Afalse+archived%3Afalse+stars%3A%3E3000+sort%3Astars-asc&s=stars&type=Repositories"

    result = enviarRequest(url)
    if(result == False):
        print("erro pagina "+str(x))
    
    soup = BeautifulSoup(result.text, "lxml")
    listaItens = soup.find_all("a", class_="v-align-middle")
    
    for repo in listaItens:
        total += 1
        sender.send(repo.text)

    print("Inserindo novos: "+str(len(listaItens)))
    print("Total Agora: "+str(total))
    print("Pagina: "+str(x))
