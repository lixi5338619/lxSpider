function ncv(e) {
    return function(e) {
        try {
            return btoa(e);
        } catch (t) {
            return Buffer.from(e).toString("base64")
        }
    }(encodeURIComponent(e).replace(/%([0-9A-F]{2})/g, (function(e, t) {
        return i("0x" + t)
    }
    )))
}

function noZ(e, t) {
    t || (t = s());
    for (var a = (e = e.split("")).length, n = t.length, o = "charCodeAt", r = 0; r < a; r++)
        e[r] = i(e[r][o](0) ^ t[(r + 10) % n][o](0));
    return e.join("")
}

function i(e) {
    var t, a = (t = "",
    ["66", "72", "6f", "6d", "43", "68", "61", "72", "43", "6f", "64", "65"].forEach((function(e) {
        t += unescape("%u00" + e)
    }
    )),
    t);
    return String[a](e)
}


// 此部分是f的生成，但是发现f是个定值，所以注释了
// var cookie = ""
// function nej(e) {
//     var t, a = new RegExp("(^| )" + e + "=([^;]*)(;|$)");
//     return (t = cookie.match(a)) ? unescape(t[2]) : null
// }
// var t = (0,nej)("synct");
// f = -(0,nej)("syncd") || +new Date - 1e3 * t


function get_analysis(xhr,brand){
    var f = 267;
    var l = "0000000c735d856";
    var a,
    o = +new Date - (f || 0) - 1515125653845,
    r = [];
    var e = {};
    e.url = xhr;
    e.params = {
        brand: brand,
        country: "cn",
        device: "iphone",
        genre: "5000"
    };
Object.keys(e.params).forEach((function(t) {
    if (t == false)
        return !1;
    e.params.hasOwnProperty(t) && r.push(e.params[t])
})),
    r = r.sort().join(""),
    r = (0,
    ncv)(r),
    r += "@#" + e.url.replace('https://api.qimai.cn', ""),
    r += "@#" + o,
    r += "@#" + 1,
    a = (0,ncv)((0, noZ)(r, l)),
    -1 == e.url.indexOf("analysis") && (e.url += (-1 != e.url.indexOf("?") ? "&" : "?") + "analysis" + "=" + encodeURIComponent(a)),
    e;
    return e
}


// console.log(get_analysis("/rank/index","paid"));
