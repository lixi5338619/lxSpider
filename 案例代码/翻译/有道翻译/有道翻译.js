
var crypto = require('crypto-js')


function md5(argc) { 
  return crypto.MD5(argc).toString().toLowerCase();
 }

var r = function(e) {
  var t = md5("5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36")
    , r = "" + (new Date).getTime()
    , i = r + parseInt(10 * Math.random(), 10);
  return {
      ts: r,
      bv: t,
      salt: i,
      sign: md5("fanyideskweb" + e + i + "Y2FYu%TNSbMCxc3t2u^XT")
  }
};

