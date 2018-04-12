/**
 ***************************************************************************
 * Name            : Processamento PPP em lote
 * Description     : Realiza o download do ponto processado por PPP do IBGE em lote baseado nos arquivos RINEX de medição
 * Version         : 1.0
 * copyright       : 1ºCGEO / DSG
 * reference
 ***************************************************************************
 ***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************
 */

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

const main = process.argv[9] === "true";
let page;
if (main) {
  page =
    "https://www.ibge.gov.br/geociencias-novoportal/informacoes-sobre-posicionamento-geodesico/servicos-para-posicionamento-geodesico/16334-servico-online-para-pos-processamento-de-dados-gnss-ibge-ppp.html?=&t=processar-os-dados";
} else {
  page = "http://www.ppp.ibge.gov.br/ppp.htm";
}

let zips = findPPP(process.argv[6]);

zips = zips.filter(removeDownloaded(process.argv[7]));

fixture("Download PPP: " + zips.length + " arquivos.");

zips.forEach(zip => {
  let name =
    "Download: " + zip.split("\\")[zip.split("\\").length - 1].slice(0, -4);

  test.page(page)(name, async t => {
    if (main) {
      await t
        .typeText(
          Selector("input").withAttribute("name", "email"),
          process.argv[8]
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
    } else {
      await t
        .typeText(
          Selector("input").withAttribute("name", "email"),
          process.argv[8]
        )
        .setFilesToUpload(
          Selector("input").withAttribute("name", "arquivo"),
          zip
        )
        .click(Selector("input").withAttribute("value", "Processar"))
        .wait(10000)
        .click(Selector("div #geral p a"))
        .wait(5000);
    }
  });
});
