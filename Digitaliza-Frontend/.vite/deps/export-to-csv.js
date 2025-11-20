import "./chunk-G3PMV62Z.js";

// node_modules/export-to-csv/output/index.js
var q;
(function(x) {
  x["csv"] = "text/csv";
  x["tsv"] = "text/tab-separated-values";
  x["plain"] = "text/plain";
})(q || (q = {}));
var X = (W) => W;
var z = (W) => W;
var Z = X;
var _ = X;
var Y = X;
var N = X;
var V = X;
var h = { fieldSeparator: ",", decimalSeparator: ".", quoteStrings: true, quoteCharacter: '"', showTitle: false, title: "My Generated Report", filename: "generated", showColumnHeaders: true, useTextFile: false, fileExtension: "csv", mediaType: q.csv, useBom: true, columnHeaders: [], useKeysAsHeaders: false, boolDisplay: { true: "TRUE", false: "FALSE" }, replaceUndefinedWith: "" };
var F = "\r\n";
var R = "\uFEFF";
var G = (W) => Object.assign({}, h, W);
var K = class extends Error {
  constructor(W) {
    super(W);
    this.name = "CsvGenerationError";
  }
};
var B = class extends Error {
  constructor(W) {
    super(W);
    this.name = "EmptyHeadersError";
  }
};
var L = class extends Error {
  constructor(W) {
    super(W);
    this.name = "CsvDownloadEnvironmentError";
  }
};
var P = class extends Error {
  constructor(W) {
    super(W);
    this.name = "UnsupportedDataFormatError";
  }
};
var s = function(W, $) {
  if ($ == '"' && W.indexOf('"') > -1) return W.replace(/"/g, '""');
  return W;
};
var w = (W) => typeof W === "object" ? N(W.key) : N(W);
var y = (W) => typeof W === "object" ? V(W.displayLabel) : V(W);
var T = (W, ...$) => $.reduce((j, x) => x(j), W);
var E = (W) => ($) => W.useBom ? _(z($) + R) : $;
var M = (W) => ($) => W.showTitle ? S(_(z($) + W.title))(Y("")) : $;
var S = (W) => ($) => _(z(W) + z($) + F);
var O = (W) => ($, j) => l(W)(Y(z($) + z(j)));
var l = (W) => ($) => X(z($) + W.fieldSeparator);
var b = (W, $) => (j) => {
  if (!W.showColumnHeaders) return j;
  if ($.length < 1) throw new B("Option to show headers but none supplied. Make sure there are keys in your collection or that you've supplied headers through the config options.");
  let x = Y("");
  for (let A = 0; A < $.length; A++) {
    const J = y($[A]);
    x = O(W)(x, v(W, z(J)));
  }
  return x = Y(z(x).slice(0, -1)), S(j)(x);
};
var C = (W, $, j) => (x) => {
  let A = x;
  for (var J = 0; J < j.length; J++) {
    let I = Y("");
    for (let U = 0; U < $.length; U++) {
      const H = w($[U]), D = j[J][z(H)];
      I = O(W)(I, v(W, D));
    }
    I = Y(z(I).slice(0, -1)), A = S(A)(I);
  }
  return A;
};
var k = z;
var m = (W) => +W === W && (!isFinite(W) || Boolean(W % 1));
var p = (W, $) => {
  if (m($)) {
    if (W.decimalSeparator === "locale") return Z($.toLocaleString());
    if (W.decimalSeparator) return Z($.toString().replace(".", W.decimalSeparator));
  }
  return Z($.toString());
};
var Q = (W, $) => {
  let j = $;
  if (W.quoteStrings || W.fieldSeparator && $.indexOf(W.fieldSeparator) > -1 || W.quoteCharacter && $.indexOf(W.quoteCharacter) > -1 || $.indexOf("\n") > -1 || $.indexOf("\r") > -1) j = W.quoteCharacter + s($, W.quoteCharacter) + W.quoteCharacter;
  return Z(j);
};
var g = (W, $) => {
  const j = $ ? "true" : "false";
  return Z(W.boolDisplay[j]);
};
var r = (W, $) => {
  if (typeof $ === "undefined" && W.replaceUndefinedWith !== void 0) return Q(W, W.replaceUndefinedWith + "");
  if ($ === null) return Q(W, "null");
  return Q(W, "");
};
var v = (W, $) => {
  if (typeof $ === "number") return p(W, $);
  if (typeof $ === "string") return Q(W, $);
  if (typeof $ === "boolean" && W.boolDisplay) return g(W, $);
  if ($ === null || typeof $ === "undefined") return r(W, $);
  throw new P(`
    typeof ${typeof $} isn't supported. Only number, string, boolean, null and undefined are supported.
    Please convert the data in your object to one of those before generating the CSV.
    `);
};
var BW = (W) => ($) => {
  const j = G(W), x = j.useKeysAsHeaders ? Object.keys($[0]) : j.columnHeaders;
  let A = T(_(""), E(j), M(j), b(j, x), C(j, x, $));
  if (z(A).length < 1) throw new K("Output is empty. Is your data formatted correctly?");
  return A;
};
var f = (W) => ($) => {
  const j = G(W), x = z($), A = j.useTextFile ? "text/plain" : j.mediaType;
  return new Blob([x], { type: `${A};charset=utf8;` });
};
var LW = (W) => ($) => {
  if (!window) throw new L("Downloading only supported in a browser environment.");
  const j = f(W)($), x = G(W), A = x.useTextFile ? "txt" : x.fileExtension, J = `${x.filename}.${A}`, I = document.createElement("a");
  I.download = J, I.href = URL.createObjectURL(j), I.setAttribute("visibility", "hidden"), document.body.appendChild(I), I.click(), document.body.removeChild(I);
};
export {
  q as MediaType,
  f as asBlob,
  k as asString,
  LW as download,
  BW as generateCsv,
  G as mkConfig
};
//# sourceMappingURL=export-to-csv.js.map
