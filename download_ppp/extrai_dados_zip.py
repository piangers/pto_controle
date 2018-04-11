from zipfile import ZipFile
import zipfile
import os
import os.path
from re import search




def busca_zip(local_zip):
    zips = []
    padrao = "^[\w\.-]+[\w\.-]+@([\w-]+\.)+[\w-]+[\w]+(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]+(.zip)+[\w]+(LIB)+[\w]+[1-9]+[0-9]+[1-9]+[0-9]+[1-9]+[0-9]+[1-9]+(.zip)*$"
    for root, dirs, files in os.walk(local_zip):
        nome = root.split('/')[-1]
        for f in files:
            #print f
            if search(padrao,f) and f.endswith('.zip') and os.path.isfile(os.path.join(root, f)):
                zips.append(os.path.join(root, f))
        
                

''' def extrai_zip(local_destino):

    #with zipfile.ZipFile(local, 'r') as zip_ref:
   
    for root, dirs, files in os.walk(local_destino):
        if root.split('/')[-1] == '6_Processamento_PPP':
            for d in dirs:
                zip_ref.extractall(os.path.join(root,d),d))
 '''




busca_zip(R'/home/piangers/Documentos/desenvolvimento/preparo/zip_ppp_exemplo')
''' extrai_zip(R'/home/piangers/Documentos/desenvolvimento/preparo/2018-04-04')
 '''


