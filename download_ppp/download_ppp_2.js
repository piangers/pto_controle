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

let zips = findPPP(process.argv[6]);

zips = zips.filter(removeDownloaded(process.argv[7]));

fixture("Download PPP: " + zips.length + " arquivos.");

const page = "http://www.ppp.ibge.gov.br/ppp.htm";

zips.forEach(zip => {
  let name =
    "Download: " + zip.split("\\")[zip.split("\\").length - 1].slice(0, -4);

  test.page(page)(name, async t => {
    await t
      .typeText(
        Selector("input").withAttribute("name", "email"),
        process.argv[8]
      )
      .setFilesToUpload(Selector("input").withAttribute("name", "arquivo"), zip)
      .click(Selector("input").withAttribute("value", "Processar"))
      .wait(10000)
      .click(Selector("div #geral p a"))
      .wait(5000);
  });
});

//npm install -g testcafe
//testcafe -c 2 chrome upload_ppp.js
