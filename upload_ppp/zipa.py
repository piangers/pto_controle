  
def zipa_arquivos(arqs):
    nome_pasta = "^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]*$"
    nome_zip = nome_pasta
    fls = []
    for root, dirs, files in os.walk(pasta):
        if root.split('\\')[-1] == "2_RINEX" and len(files) > 0:
            for fl in files:
                if fl.endswith('.txt') and os.path.isfile(os.path.join(root, fl)):
                    fls.append(os.path.join(root, fl))
                    with zipfile.ZipFile(nome_pasta,'w', zipfile.ZIP_DEFLATED) as compactar:
                        for arq in arqs:
                            if(os.path.isfile(arq)): # se for ficheiro
                                compactar.write(arq)
                            else: # se for diretorio
                                for root, dirs, files in os.walk(arq):
                                    for pasta in files:
                                        compactar.write(os.path.join(root, pasta), os.path.relpath(os.path.join(folder,file), 'C:\\'), compress_type = zipfile.ZIP_DEFLATED)

                                        print fls