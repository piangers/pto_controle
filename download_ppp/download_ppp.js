import { Selector } from "testcafe";

import { lstatSync, readdirSync } from "fs";
import { join } from "path";

const findPPP = dir => {
  let zips = [];
  readdirSync(dir).forEach(file => {
    const filepath = join(dir, file);
    if (lstatSync(filepath).isDirectory()) {
      zips = [...zips, ...findPPP(filepath)];
    } else if (
      lstatSync(filepath).isFile() &&
      filepath.split(".")[filepath.split(".").length - 1] == "zip" &&
      filepath.split("\\")[filepath.split("\\").length - 2] == "2_RINEX"
    ) {
      zips.push(filepath);
    }
  });
  return zips;
};

const removeDownloaded = dir => {
  let zips = [];
  readdirSync(dir).forEach(file => {
    const pto_regex = /^(RS|PR|SC|SP)-(HV|Base)-[1-9]+[0-9]*$/;
    if (
      lstatSync(join(dir, file)).isFile() &&
      file.split(".")[file.split(".").length - 1] == "zip" &&
      file.split("_").length == 4 &&
      pto_regex.test(file.split("_")[1].slice(0, -4))
    ) {
      zips.push(file.split("_")[1].slice(0, -4));
    }
  });
  return pto_path => {
    let pto = pto_path
      .split("\\")
      [pto_path.split("\\").length - 1].slice(0, -4);
    if (zips.indexOf(pto) > -1) {
      return false;
    } else {
      return true;
    }
  };
};

fixture("Download all");

const page =
  "https://www.ibge.gov.br/geociencias-novoportal/informacoes-sobre-posicionamento-geodesico/servicos-para-posicionamento-geodesico/16334-servico-online-para-pos-processamento-de-dados-gnss-ibge-ppp.html?=&t=processar-os-dados";

let zips = findPPP("D:\\2018-04-06");

zips = zips.filter(
  removeDownloaded("C:\\Users\\Diniz\\Downloads\\ppp_2018-03-06")
);

zips.forEach(zip => {
  test.page(page)(
    "Download: " +
      zip.split("\\")[pto_path.split("\\").length - 1].slice(0, -4),
    async t => {
      await t
        .typeText(
          Selector("input").withAttribute("name", "email"),
          "diniz.ime@gmail.com"
        )
        .setFilesToUpload(
          Selector("input").withAttribute("name", "arquivo"),
          zip
        )
        .click(Selector("input").withAttribute("value", "Processar"))
        .wait(10000);

      await t
        .switchToIframe("#iframe_resultado")
        .wait(30000)
        .click(Selector("a"))
        .wait(10000);
    }
  );
});

//npm install -g testcafe
//testcafe -c 2 chrome upload_ppp.js
