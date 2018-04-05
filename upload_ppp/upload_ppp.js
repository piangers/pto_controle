import { Selector } from "testcafe";

fixture`Download all`;

const page = `https://www.ibge.gov.br/geociencias-novoportal/informacoes-sobre-posicionamento-geodesico/servicos-para-posicionamento-geodesico/16334-servico-online-para-pos-processamento-de-dados-gnss-ibge-ppp.html?=&t=processar-os-dados`;

const paths = [
  'E:\\RS-HV-1252.zip',
  'E:\\RS-HV-1253.zip'
]

paths.forEach(path => {
  test.page(page)("Download", async t => {
    await t
      .typeText(
        Selector("input").withAttribute("name", "email"),
        "diniz.ime@gmail.com"
      )
      .setFilesToUpload(
        Selector("input").withAttribute("name", "arquivo"),
        path
      )
      .click(Selector("input").withAttribute("value", "Processar"))
      .wait(5000);
      
    await t
      .switchToIframe("#iframe_resultado")
      .wait(20000)
      .click(Selector("a"))
      .wait(5000);
  });
});


//npm install -g testcafe
//testcafe -c 2 chrome upload_ppp.js
