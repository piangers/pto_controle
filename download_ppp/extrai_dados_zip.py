# -*- coding: utf-8 -*-

## DSG=group
## local=folder

from zipfile import ZipFile
import os
from re import search
import shutil


def busca_zip(local_zip,local_destino):

    padrao = "^[\w\.-]+[\w\.-]+@([\w-]+\.)+[\w-]+[\w]+(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]+(.zip)+[\w]+(LIB)+[\w]+[1-9]+[0-9]+[1-9]+[0-9]+[1-9]+[0-9]+[1-9]+(.zip)*$"
    
    for root, dirs, files in os.walk(local_zip):
        lista_zip = {}
        
        lista_pedaco_zip = []
        for f in files:    
            if search(padrao,f) and f.endswith('.zip') and os.path.isfile(os.path.join(root, f)):
                
                s1 = f.split('_')[1]
                pedaco_nome_zip = s1.split('.')[0] # s2 recebe o trecho do nome do ZIP selecionado, que será comparado com o do endereço

                caminho = os.path.join(root,f)

                #lista_zip[pedaco_nome_zip] = caminho
                lista_zip[f] = caminho

                #lista_pedaco_zip.append(pedaco_nome_zip) # procurar em todos os elementos nessa lista
                #lista_pedaco_zip.sort()

    i = 0
    todos_os_zips = lista_zip.keys()
    for z in todos_os_zips:
        caminho_zip = lista_zip[z]
        nome = z.split('_')[1].split('.')[0]
                
        existe = False
        
        for local, dirs, files in os.walk(local_destino):
            pai = ''
            if local.split(R'/')[-1] == "6_Processamento_PPP":
                pai = local.split(R'/')[-2]
                
            #print z
            if pai == nome:
                existe = True

                if len(os.listdir(local)) > 0:
                    frase = "O diretório " + local + " já contém arquivos!"
                    frase.decode("utf8")
                    print(frase)
                    continue

                
                with ZipFile(caminho_zip,"r") as zip_ref: # carrega o zip
                            
                    zip_obj = ZipFile(caminho_zip)
                        # percorre todos arquivos dentro do zip.
                    for ob in zip_obj.namelist():
                        filename = os.path.basename(ob)
                        
                        # pula diretórios
                        if not filename:
                            continue

                        # copia o arquivo para o diretório destino (em vez de extraí-lo)
                        abre = zip_ref.open(ob)
                        pega = file(os.path.join(local, filename), "wb")
                        with abre, pega:
                            shutil.copyfileobj(abre, pega)
                    
                    frase = "O ZIP para o MI "+ nome + " foi extraído com sucesso!"
                    frase.decode("utf8")
                    print (frase)

                    
        # Mostrar MI se a pasta ja tiver arquivos
        if not existe:
            frase = "O ZIP para o MI "+ nome + " não possui pasta correspondente!"
            frase.decode("utf8")
            print (frase)
            
                
            # Mostrar MI se o ZIP não tiver uma pasta correspondente           


busca_zip(R'/home/piangers/Documentos/desenvolvimento/preparo/zip_ppp_exemplo', R'/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04')

