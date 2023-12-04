import zipfile
import os

class TrataResponse():

    def salvaResponseZipado(self, response, repo, pr_id):
        repo = str(repo).replace("/", "-")
        repo = str(repo).replace("#", "")

        nomeArquivo = repo+"#"+str(pr_id)
        caminhoCompletoArquivoTxt = "zip_request/"+nomeArquivo+".txt"

        with open(caminhoCompletoArquivoTxt, 'w') as arquivo:
            # arquivo.write(response.text)
            arquivo.write(response)
        
        compressaoBemSucedida =  self.salvaZipado(caminhoCompletoArquivoTxt);

        if(compressaoBemSucedida):
            self.removeArquivoTexto(caminhoCompletoArquivoTxt)
        

    def salvaZipado(self, arquivo):
        arquivoZip = str(arquivo).replace(".txt", ".zip")

        try:
            jungle_zip = zipfile.ZipFile(arquivoZip, 'w')
            jungle_zip.write(arquivo, compress_type=zipfile.ZIP_BZIP2)
            jungle_zip.close()    

            return True
        except:
            return False

    def removeArquivoTexto(self, arquivo):
        os.remove(arquivo)


        