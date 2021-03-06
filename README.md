# Conjunto de ferramentas para medição
Conjunto de ferramentas em Python e Node.js que automatizam parte do processo de processamento e controle de qualidade da medição de pontos de controle.

## Valida estrutura de pontos de controle
Esta rotina verifica se a pasta definida atende as padronizações determinadas no Manual Técnico de Medição de Pontos de Controle do 1º Centro de Geoinformação.

### Execução
A rotina pode ser executada por linha de comando e como Script no QGIS 2.18.

O script está disponível em [Valida estrutura de pontos de controle](../master/valida_estrutura/valida_estrutura_pto_controle.py)

A rotina possui os seguintes parâmetros:
* *pasta dos pontos de controle*: Pasta com a estrutura de pontos de controle
* *operadores*: Nome dos operadores separados por ;
* *data*: Data de realização da medição
* *fuso horário*: Fuso horário dos tempos informados
* *ignora_processamento*: Valor booleano que informa se deve ignorar as pastas e arquivos de processamento na avaliação.
* *log*: Arquivo com o relatório de erros

```
python valida_estrutura_pto_controle.py D:\2018-04-06 alegranzi;tolfo;alves 2018-04-06 -3 True D:\relatorios\relatorio_erros_2018-04-06
```

## Atualiza banco de dados de controle
Esta rotina busca na pasta definida e nas suas subpastas pelos arquivos .CSV padrão de medição e atualiza o banco de dados de pontos de controle.

As seguintes informações são atualizadas:
* *medidor*: Nome do operador que realizou a medição
* *data_medicao*: Dada que ocorreu a medição
* *tipo_situacao_id*: Atualiza com o valor 4 (Aguardando avaliação)

É interessante que seja executada a rotina **Valida estrutura de pontos de controle** antes da execução desta rotina.

### Execução
A rotina pode ser executada por linha de comando e como Script no QGIS 2.18.

O script está disponível em [Atualiza banco de dados de controle](../master/bd/atualiza_bd.py)

A rotina possui os seguintes parâmetros:
* *pasta dos pontos de controle*: Pasta com a estrutura de pontos de controle
* *servidor*: IP do servidor de banco de dados PostgreSQL
* *porta*: Porta de acesso ao servidor de banco de dados
* *nome do banco de dados*: Nome do banco de dados de ponto de controle
* *usuario*: Usuário com acesso ao banco de dados
* *senha*: Senha para o usuário definido

```
python atualiza_bd.py D:\2018-04-06 localhost 5432 pto_controle usuario senha
```

## Processamento PPP em lote
Esta rotina verifica se a pasta definida atende as padronizações determinadas no Manual Técnico de Medição de Pontos de Controle do 1º Centro de Geoinformação.

### Execução
O processamento é composto de 3 rotinas, sendo duas em python, que podem ser executadas por linha de comando e como Script no QGIS 2.18, e uma em Node.js que é executada utilizando TestCafé.

Primeiramente deve-se executar o script de preparo [Preparo para processamento PPP](../master/download_ppp/pre_ppp.py)

Esta rotina cria as pastas *6_Processamento_PPP* e *7_Processamento_TBC_RBMC* na estrutura de pastas e compacta os arquivos RINEX no formato zip.

A rotina possui o seguinte parâmetro:
* *pasta dos pontos de controle*: Pasta com a estrutura de pontos de controle

```
python pre_ppp.py D:\2018-04-06
```

A próxima rotina envia os arquivos RINEX compactados em formato zip para o site do [IBGE](https://www.ibge.gov.br/geociencias-novoportal/informacoes-sobre-posicionamento-geodesico/servicos-para-posicionamento-geodesico/16334-servico-online-para-pos-processamento-de-dados-gnss-ibge-ppp.html?=&t=processar-os-dados) para utilização do método de [Posicionamento por Ponto Preciso](https://www.ibge.gov.br/geociencias-novoportal/informacoes-sobre-posicionamento-geodesico/servicos-para-posicionamento-geodesico/16334-servico-online-para-pos-processamento-de-dados-gnss-ibge-ppp.html?=&t=o-que-e).

Para executar o script de download de arquivos PPP é necessário ter Node.js instalando a ferramenta [TestCafé](https://github.com/DevExpress/testcafe).

O script se encontra em [Download PPP](../master/download_ppp/download_ppp.js)

A rotina possui o seguinte parâmetro:
* *número de navegadores*: Número de navegadores que o TestCafé utilizará simultâneamente
* *nome do navegador*: Nome do navegador que será utilizado para executar o download
* *pasta dos pontos de controle*: Pasta com a estrutura de pontos de controle
* *pasta destino de download*: Pasta padrão onde os arquivos baixados são enviados. Esse parâmetro não configura a pasta, somente verifica se o arquivo já foi baixado percorrendo o conteúdo da pasta.
* *email*: Email necessário para processar no site do IBGE
* *principal*: Determina se será utilizado o site principal do IBGE ([1](https://www.ibge.gov.br/geociencias-novoportal/informacoes-sobre-posicionamento-geodesico/servicos-para-posicionamento-geodesico/16334-servico-online-para-pos-processamento-de-dados-gnss-ibge-ppp.html?=&t=processar-os-dados)) ou o antigo ([2](http://www.ppp.ibge.gov.br/ppp.htm)). No caso de positivo o valor deve ser *true*.

```
testcafe -c 3 chrome upload_ppp.js D:\2018-04-06 D:\downloads\ppp test@email.com.br true
```

Por último deve-se executar o script de finalização [Pós processamento PPP](../master/download_ppp/pos_ppp.py)

Esta rotina descompacta os arquivos PPP no formato zip e distribui os arquivos na estrutura padrão de pastas de ponto de controle.

A rotina possui os seguintes parâmetros:
* *pasta dos pontos de controle*: Pasta com a estrutura de pontos de controle
* *pasta com arquivos PPP*: Pasta com os arquivos PPP no formato zip

```
python pos_ppp.py D:\2018-04-06 D:\downloads\ppp
```

##  Cria PDFs do processamento TBC
Esta rotina gera os relatórios de cada ponto em PDF a partir do relatorio em HTML gerado pelo software TBC. Os relatórios são distribuídos na estrutura correta de pastas. 

### Execução
A rotina pode ser executada por linha de comando. O script depende das bibliotecas:
* [pdfkit](https://github.com/JazzCore/python-pdfkit)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
* [wkthmltopdf](https://wkhtmltopdf.org/)

O script está disponível em [Cria PDF Processamento](../master/extrai_dados/cria_pdf_processamento.py)

A rotina possui os seguintes parâmetros:
* *Executável do wkhtmltopdf*: Caminho para o arquivo executável do wkhtmltopdf
* *Arquivo HTML*: Arquivo HTML index do relatório gerado pelo software TBC
* *Pasto de destino*: Pasta com a estrutura de pontos de controle

```
python cria_pdf_processamento.py "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe" D:\processamento\tbc\relatorio.html  D:\2018-04-06 
```

## Extrai dados para análise
Esta rotina busca na pasta definida relatórios gerados do PPP e relatórios gerados pelo TBC (utilizando RBMC) e gera um arquivo CSV com a comparação entre as coordenadas calculadas.

### Execução
A rotina pode ser executada por linha de comando e como Script no QGIS 2.18. O script depende da biblioteca [PyPDF2](https://github.com/mstamy2/PyPDF2).

O script está disponível em [Extrai dados](../master/extrai_dados/extrai_dados.py)

A rotina possui os seguintes parâmetros:
* *pasta dos pontos de controle*: Pasta com a estrutura de pontos de controle
* *Pasto de destino*: Pasta de destino do arquivo CSV a ser criado

```
python extrai_dados.py D:\2018-04-06 relatorio_2018-04-06.csv
```