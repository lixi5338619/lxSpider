"use strict";
require("./runtime.js"),
  require("./vendor2.js"),
  require("./main.js");

function get_sig3(params){
    window.lxrealm.realm.global.$encode.apply(window.lxrealm.realm,[
        params,
      {
          suc: function (t) {
            e("__NS_sig3=".concat(t));
          },
          err: function (e) {
            t(e);
          },
        }
    ])
    return window.lxsig3;
}

function set_sig3(){
    window.lxsig3 = null;
}

var params = process.argv[2];
console.log(get_sig3(params))
set_sig3()

process.exit()