import { Selector } from "testcafe";

fixture`Download all`;

const page = `https://www.ibge.gov.br/geociencias-novoportal/informacoes-sobre-posicionamento-geodesico/servicos-para-posicionamento-geodesico/16334-servico-online-para-pos-processamento-de-dados-gnss-ibge-ppp.html?=&t=processar-os-dados`;

test.page(page)("Download", async t => {
  await t
    .typeText(
      Selector("input").withAttribute("name", "email"),
      "diniz.ime@gmail.com"
    )
    .setFilesToUpload(
      Selector("input").withAttribute("name", "arquivo"),
      "C:\\Users\\Diniz\\Downloads\\alegranzi_2018-03-27-20180330T112916Z-001\\alegranzi_2018-03-27\\RS-HV-983\\2_RINEX\\RS-HV-983.zip"
    )
    .click(Selector("input").withAttribute("value", "Processar"))
    .wait(20000)
    .switchToIframe("#iframe_resultado")
    .click(Selector("a"))
    .wait(5000);
});
//npm install -g testcafe

//testcafe chrome upload_ppp.js
