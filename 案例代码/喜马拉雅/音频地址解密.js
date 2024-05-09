
    "use strict";
    const r = new Uint8Array([188, 174, 178, 234, 171, 147, 70, 82, 76, 72, 192, 132, 60, 17, 30, 127, 184, 233, 48, 105, 38, 232, 240, 21, 47, 252, 41, 229, 209, 213, 71, 40, 63, 152, 156, 88, 51, 141, 139, 145, 133, 2, 160, 191, 11, 100, 10, 78, 253, 151, 42, 166, 92, 22, 185, 140, 164, 91, 194, 175, 239, 217, 177, 75, 19, 225, 94, 107, 125, 138, 242, 31, 182, 150, 15, 24, 226, 29, 80, 116, 168, 118, 28, 1, 186, 220, 158, 79, 59, 244, 119, 9, 189, 161, 74, 130, 221, 56, 216, 241, 212, 26, 218, 170, 85, 165, 153, 69, 238, 93, 255, 142, 3, 159, 215, 67, 33, 249, 53, 176, 77, 254, 222, 25, 115, 101, 148, 16, 13, 237, 197, 5, 58, 157, 135, 248, 223, 61, 198, 211, 110, 44, 54, 111, 52, 227, 4, 46, 205, 7, 219, 136, 14, 87, 114, 64, 104, 50, 39, 203, 81, 196, 43, 163, 173, 109, 108, 187, 102, 195, 37, 235, 65, 190, 113, 149, 143, 8, 27, 155, 207, 134, 123, 224, 129, 245, 62, 66, 172, 122, 126, 12, 162, 214, 90, 247, 251, 124, 201, 236, 117, 183, 73, 95, 89, 246, 181, 179, 83, 228, 193, 99, 6, 45, 112, 32, 154, 128, 230, 131, 206, 243, 57, 84, 146, 0, 35, 96, 250, 137, 36, 208, 103, 34, 68, 204, 231, 144, 120, 98, 202, 49, 210, 23, 200, 18, 86, 55, 121, 20, 199, 97, 167, 180, 169, 106])
      , n = new Uint8Array([20, 234, 159, 167, 230, 233, 58, 255, 158, 36, 210, 254, 133, 166, 59, 63, 209, 177, 184, 155, 85, 235, 94, 1, 242, 87, 228, 232, 191, 3, 69, 178])
      , o = new Uint8Array([183, 174, 108, 16, 131, 159, 250, 5, 239, 110, 193, 202, 153, 137, 251, 176, 119, 150, 47, 204, 97, 237, 1, 71, 177, 42, 88, 218, 166, 82, 87, 94, 14, 195, 69, 127, 215, 240, 225, 197, 238, 142, 123, 44, 219, 50, 190, 29, 181, 186, 169, 98, 139, 185, 152, 13, 141, 76, 6, 157, 200, 132, 182, 49, 20, 116, 136, 43, 155, 194, 101, 231, 162, 242, 151, 213, 53, 60, 26, 134, 211, 56, 28, 223, 107, 161, 199, 15, 229, 61, 96, 41, 66, 158, 254, 21, 165, 253, 103, 89, 3, 168, 40, 246, 81, 95, 58, 31, 172, 78, 99, 45, 148, 187, 222, 124, 55, 203, 235, 64, 68, 149, 180, 35, 113, 207, 118, 111, 91, 38, 247, 214, 7, 212, 209, 189, 241, 18, 115, 173, 25, 236, 121, 249, 75, 57, 216, 10, 175, 112, 234, 164, 70, 206, 198, 255, 140, 230, 12, 32, 83, 46, 245, 0, 62, 227, 72, 191, 156, 138, 248, 114, 220, 90, 84, 170, 128, 19, 24, 122, 146, 80, 39, 37, 8, 34, 22, 11, 93, 130, 63, 154, 244, 160, 144, 79, 23, 133, 92, 54, 102, 210, 65, 67, 27, 196, 201, 106, 143, 52, 74, 100, 217, 179, 48, 233, 126, 117, 184, 226, 85, 171, 167, 86, 2, 147, 17, 135, 228, 252, 105, 30, 192, 129, 178, 120, 36, 145, 51, 163, 77, 205, 73, 4, 188, 125, 232, 33, 243, 109, 224, 104, 208, 221, 59, 9])
      , a = new Uint8Array([204, 53, 135, 197, 39, 73, 58, 160, 79, 24, 12, 83, 180, 250, 101, 60, 206, 30, 10, 227, 36, 95, 161, 16, 135, 150, 235, 116, 242, 116, 165, 171])
      , i = "function" == typeof atob
      , u = "function" == typeof e;
    "function" == typeof TextDecoder && new TextDecoder,
    "function" == typeof TextEncoder && new TextEncoder;
    const c = (e=>{
        let t = {};
        return e.forEach(((e,r)=>t[e] = r)),
        t
    }
    )(Array.prototype.slice.call("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="))
      , s = /^(?:[A-Za-z\d+\/]{4})*?(?:[A-Za-z\d+\/]{2}(?:==)?|[A-Za-z\d+\/]{3}=?)?$/
      , l = String.fromCharCode.bind(String);
    "function" == typeof Uint8Array.from && Uint8Array.from.bind(Uint8Array);
    const f = i ? e=>atob(e.replace(/[^A-Za-z0-9\+\/]/g, "")) : u ? t=>e.from(t, "base64").toString("binary") : e=>{
        if (e = e.replace(/\s+/g, ""),
        !s.test(e))
            throw new TypeError("malformed base64.");
        e += "==".slice(2 - (3 & e.length));
        let t, r, n, o = "";
        for (let a = 0; a < e.length; )
            t = c[e.charAt(a++)] << 18 | c[e.charAt(a++)] << 12 | (r = c[e.charAt(a++)]) << 6 | (n = c[e.charAt(a++)]),
            o += 64 === r ? l(t >> 16 & 255) : 64 === n ? l(t >> 16 & 255, t >> 8 & 255) : l(t >> 16 & 255, t >> 8 & 255, 255 & t);
        return o
    }
    ;
    function p(e, t, r) {
        let n = Math.min(e.length - t, r.length);
        for (let o = 0; o < n; o++)
            e[o + t] = e[o + t] ^ r[o]
    }
  function getSoundCryptLink(e) {
        const {link: t="", deviceType: i="www2"} = e;
        let u = o
          , c = a;
        ["www2", "mweb2"].includes(i) || (u = r,
        c = n);
        try {
            let e = f(t.replace(/_/g, "/").replace(/-/g, "+"));
            if (null === e || e.length < 16)
                return t;
            let r = new Uint8Array(e.length - 16);
            for (let t = 0; t < e.length - 16; t++)
                r[t] = e.charCodeAt(t);
            let n = new Uint8Array(16);
            for (let t = 0; t < 16; t++)
                n[t] = e.charCodeAt(e.length - 16 + t);
            for (let e = 0; e < r.length; e++)
                r[e] = u[r[e]];
            for (let e = 0; e < r.length; e += 16)
                p(r, e, n);
            for (let e = 0; e < r.length; e += 32)
                p(r, e, c);
            return function(e) {
                var t, r, n, o, a, i;
                for (t = "",
                n = e.length,
                r = 0; r < n; )
                    switch ((o = e[r++]) >> 4) {
                    case 0:
                    case 1:
                    case 2:
                    case 3:
                    case 4:
                    case 5:
                    case 6:
                    case 7:
                        t += String.fromCharCode(o);
                        break;
                    case 12:
                    case 13:
                        a = e[r++],
                        t += String.fromCharCode((31 & o) << 6 | 63 & a);
                        break;
                    case 14:
                        a = e[r++],
                        i = e[r++],
                        t += String.fromCharCode((15 & o) << 12 | (63 & a) << 6 | (63 & i) << 0)
                    }
                return t
            }(r)
        } catch (e) {
            return console.warn(e, "secret failed"),
            ""
        }
    }

var e = {
"deviceType":"www2",
"link": "6T_nnLb2RQehHuxpeGhqlQW6zkhq3onAMks8_m0kDhyoTGMLKgX9zFo38x9rhMhbwf-LKRZ6tkui1_xATL12QgFM8zROhzFuIx6Ky2sD7M-pJXDtOXOb14oAIEwik8QsYg"
}


console.log(getSoundCryptLink(e))
