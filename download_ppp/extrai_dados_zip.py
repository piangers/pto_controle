# -*- coding: utf-8 -*-

##DSG=group
##Local_do_zip=folder
##Local_do_destino=folder

import sys
from zipfile import ZipFile
import os
from re import search
import shutil


def extrai_zip(local_zip,local_destino):

    padrao = "^[\w\.-]+[\w\.-]+@([\w-]+\.)+[\w-]+[\w]+(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]+(.zip)+[\w]+(LIB)+[\w]+[1-9]+[0-9]+[1-9]+[0-9]+[1-9]+[0-9]+[1-9]+(.zip)*$"
    
    for root, dirs, files in os.walk(local_zip):
        lista_zip = {}
        
        lista_pedaco_zip = []
        for f in files:    
            if search(padrao,f) and f.endswith('.zip') and os.path.isfile(os.path.join(root, f)):
                
                s1 = f.split('_')[1]
                pedaco_nome_zip = s1.split('.')[0] 
                caminho = os.path.join(root,f)
                lista_zip[f] = caminho

    todos_os_zips = lista_zip.keys()
    for z in todos_os_zips:
        caminho_zip = lista_zip[z]
        nome = z.split('_')[1].split('.')[0]
                
        existe = False
        
        for local, dirs, files in os.walk(local_destino):
            pai = ''
            if local.split(R'/')[-1] == "6_Processamento_PPP":
                pai = local.split(R'/')[-2]
                
            if pai == nome:
                existe = True

                if len(os.listdir(local)) > 0:
                    frase = "O diretório " + local + " já contém arquivos!"
                    frase.decode("utf8")
                    print(frase)
                    continue

                with ZipFile(caminho_zip,"r") as zip_ref:     
                    zip_obj = ZipFile(caminho_zip)
                    for ob in zip_obj.namelist():
                        filename = os.path.basename(ob)
    
                        if not filename:
                            continue

                        abre = zip_ref.open(ob)
                        pega = file(os.path.join(local, filename), "wb")
                        with abre, pega:
                            shutil.copyfileobj(abre, pega)
                    
                    frase = "O ZIP para o MI "+ nome + " foi extraído com sucesso!"
                    frase.decode("utf8")
                    print (frase)
              
        if not existe:
            frase = "O ZIP para o MI "+ nome + " não possui pasta correspondente!"
            frase.decode("utf8")
            print (frase)
            
#referencia para locais.               
#extrai_zip(R'/home/piangers/Documentos/desenvolvimento/preparo/zip_ppp_exemplo', R'/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04')

if __name__== '__builtins__':
    extrai_zip(local_do_zip,local_do_destino)

