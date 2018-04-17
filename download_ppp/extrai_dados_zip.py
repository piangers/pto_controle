# -*- coding: utf-8 -*-

## DSG=group
## local=folder

from zipfile import ZipFile
import os
from re import search



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




            endereco = []
            for root2, dirs, files in os.walk(local_destino):

                todos_os_zips = lista_zip.keys()
                #print todos_os_zips
                
                if root2.split(R'/')[-1] == "6_Processamento_PPP":
                    local = root2
                    pai = root2.split(R'/')[-2]

                    for z in todos_os_zips:
                        nome = z.split('_')[1].split('.')[0]
                        #print z
                        if pai == nome:
                            #print pai
                            #print nome
                            caminho_zip = lista_zip[z]
                            #print caminho_zip
                            
                            #EXTRAIR AQUI
                            
                            
                            with ZipFile(caminho_zip,"r") as zip_ref:
                                    # carrega o zip
                                    zip_obj = ZipFile(caminho_zip)
                                    
                                    # percorre todos arquivos dentro do zip.
                                    for nome in zip_obj.namelist():
                                        if not nome.endswith('/'): # se o arquivo(nome) não terminar com /, então descompacta.
                                            outfile = open(os.path.join(caminho_zip, nome), 'wb')
                                            
                                            outfile.write(zip_obj.read(nome))
                                            outfile.close()

            

    # nao deu erro, exclui o arquivo

    #os.remove(arquivo)

            
            

                        
busca_zip(R'/home/piangers/Documentos/desenvolvimento/preparo/zip_ppp_exemplo', R'/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04')

