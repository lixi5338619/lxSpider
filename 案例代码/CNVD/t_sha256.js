window = {}
window.navigator={
'userAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}

function hash(_0xb3a2f3) {
  var _0x436214 = 8;
  var _0x3ebd36 = 0;

  function _0x70fb8(_0x3b1fbb, _0x4a616c) {
    var _0x5df8da = (_0x3b1fbb & 65535) + (_0x4a616c & 65535);

    var _0x23a7a2 = (_0x3b1fbb >> 16) + (_0x4a616c >> 16) + (_0x5df8da >> 16);

    return _0x23a7a2 << 16 | _0x5df8da & 65535;
  }

  function _0x4e57dd(_0x4d810e, _0x184aac) {
    return _0x4d810e >>> _0x184aac | _0x4d810e << 32 - _0x184aac;
  }

  function _0x36087b(_0x152685, _0x48a182) {
    return _0x152685 >>> _0x48a182;
  }

  function _0x399548(_0x4dcebb, _0xab0153, _0x7dbf5b) {
    return _0x4dcebb & _0xab0153 ^ ~_0x4dcebb & _0x7dbf5b;
  }

  function _0x48ee3a(_0x333fa7, _0x55d2ec, _0x17a443) {
    return _0x333fa7 & _0x55d2ec ^ _0x333fa7 & _0x17a443 ^ _0x55d2ec & _0x17a443;
  }

  function _0x310842(_0x2be1b1) {
    return _0x4e57dd(_0x2be1b1, 2) ^ _0x4e57dd(_0x2be1b1, 13) ^ _0x4e57dd(_0x2be1b1, 22);
  }

  function _0x7d5a12(_0x647765) {
    return _0x4e57dd(_0x647765, 6) ^ _0x4e57dd(_0x647765, 11) ^ _0x4e57dd(_0x647765, 25);
  }

  function _0x1cdddc(_0x8ec478) {
    return _0x4e57dd(_0x8ec478, 7) ^ _0x4e57dd(_0x8ec478, 18) ^ _0x36087b(_0x8ec478, 3);
  }

  function _0x38e736(_0x57bc8e) {
    return _0x4e57dd(_0x57bc8e, 17) ^ _0x4e57dd(_0x57bc8e, 19) ^ _0x36087b(_0x57bc8e, 10);
  }

  function _0x58103a(_0x3b9164, _0x1e15fd) {
    var _0xea397a = new Array(1116352408, 1899447441, 3049323471, 3921009573, 961987163, 1508970993, 2453635748, 2870763221, 3624381080, 310598401, 607225278, 1426881987, 1925078388, 2162078206, 2614888103, 3248222580, 3835390401, 4022224774, 264347078, 604807628, 770255983, 1249150122, 1555081692, 1996064986, 2554220882, 2821834349, 2952996808, 3210313671, 3336571891, 3584528711, 113926993, 338241895, 666307205, 773529912, 1294757372, 1396182291, 1695183700, 1986661051, 2177026350, 2456956037, 2730485921, 2820302411, 3259730800, 3345764771, 3516065817, 3600352804, 4094571909, 275423344, 430227734, 506948616, 659060556, 883997877, 958139571, 1322822218, 1537002063, 1747873779, 1955562222, 2024104815, 2227730452, 2361852424, 2428436474, 2756734187, 3204031479, 3329325298);

    var _0x429abc = new Array(1779033703, 3144134277, 1013904242, 2773480762, 1359893119, 2600822924, 528734635, 1541459225);

    var _0x2b18db = new Array(64);

    var _0x57b507, _0x2f7eb6, _0x3a62a0, _0x38f7e0, _0x880a21, _0x5a6598, _0xa6d654, _0x3f0a05, _0x1f3b08, _0x521f34;

    var _0x4bc8b6, _0x394ae6;

    _0x3b9164[_0x1e15fd >> 5] |= 128 << 24 - _0x1e15fd % 32;
    _0x3b9164[(_0x1e15fd + 64 >> 9 << 4) + 15] = _0x1e15fd;

    for (var _0x1f3b08 = 0; _0x1f3b08 < _0x3b9164["length"]; _0x1f3b08 += 16) {
      _0x57b507 = _0x429abc[0];
      _0x2f7eb6 = _0x429abc[1];
      _0x3a62a0 = _0x429abc[2];
      _0x38f7e0 = _0x429abc[3];
      _0x880a21 = _0x429abc[4];
      _0x5a6598 = _0x429abc[5];
      _0xa6d654 = _0x429abc[6];
      _0x3f0a05 = _0x429abc[7];

      for (var _0x521f34 = 0; _0x521f34 < 64; _0x521f34++) {
        if (_0x521f34 < 16) {
          _0x2b18db[_0x521f34] = _0x3b9164[_0x521f34 + _0x1f3b08];
        } else {
          _0x2b18db[_0x521f34] = _0x70fb8(_0x70fb8(_0x70fb8(_0x38e736(_0x2b18db[_0x521f34 - 2]), _0x2b18db[_0x521f34 - 7]), _0x1cdddc(_0x2b18db[_0x521f34 - 15])), _0x2b18db[_0x521f34 - 16]);
        }

        _0x4bc8b6 = _0x70fb8(_0x70fb8(_0x70fb8(_0x70fb8(_0x3f0a05, _0x7d5a12(_0x880a21)), _0x399548(_0x880a21, _0x5a6598, _0xa6d654)), _0xea397a[_0x521f34]), _0x2b18db[_0x521f34]);
        _0x394ae6 = _0x70fb8(_0x310842(_0x57b507), _0x48ee3a(_0x57b507, _0x2f7eb6, _0x3a62a0));
        _0x3f0a05 = _0xa6d654;
        _0xa6d654 = _0x5a6598;
        _0x5a6598 = _0x880a21;
        _0x880a21 = _0x70fb8(_0x38f7e0, _0x4bc8b6);
        _0x38f7e0 = _0x3a62a0;
        _0x3a62a0 = _0x2f7eb6;
        _0x2f7eb6 = _0x57b507;
        _0x57b507 = _0x70fb8(_0x4bc8b6, _0x394ae6);
      }

      _0x429abc[0] = _0x70fb8(_0x57b507, _0x429abc[0]);
      _0x429abc[1] = _0x70fb8(_0x2f7eb6, _0x429abc[1]);
      _0x429abc[2] = _0x70fb8(_0x3a62a0, _0x429abc[2]);
      _0x429abc[3] = _0x70fb8(_0x38f7e0, _0x429abc[3]);
      _0x429abc[4] = _0x70fb8(_0x880a21, _0x429abc[4]);
      _0x429abc[5] = _0x70fb8(_0x5a6598, _0x429abc[5]);
      _0x429abc[6] = _0x70fb8(_0xa6d654, _0x429abc[6]);
      _0x429abc[7] = _0x70fb8(_0x3f0a05, _0x429abc[7]);
    }

    return _0x429abc;
  }

  function _0xe1c49c(_0x1f224c) {
    var _0xb5927 = Array();

    var _0xc3530a = 255;

    for (var _0x1c5849 = 0; _0x1c5849 < _0x1f224c["length"] * _0x436214; _0x1c5849 += _0x436214) {
      _0xb5927[_0x1c5849 >> 5] |= (_0x1f224c["charCodeAt"](_0x1c5849 / _0x436214) & _0xc3530a) << 24 - _0x1c5849 % 32;
    }

    return _0xb5927;
  }

  function _0x4756fb(_0x57f4af) {
    var _0x1d8407 = new RegExp("\n", "g");

    _0x57f4af = _0x57f4af["replace"](_0x1d8407, "\n");
    var _0x577056 = "";

    for (var _0x2ed237 = 0; _0x2ed237 < _0x57f4af["length"]; _0x2ed237++) {
      var _0x6189ac = _0x57f4af["charCodeAt"](_0x2ed237);

      if (_0x6189ac < 128) {
        _0x577056 += String["fromCharCode"](_0x6189ac);
      } else {
        if (_0x6189ac > 127 && _0x6189ac < 2048) {
          _0x577056 += String["fromCharCode"](_0x6189ac >> 6 | 192);
          _0x577056 += String["fromCharCode"](_0x6189ac & 63 | 128);
        } else {
          _0x577056 += String["fromCharCode"](_0x6189ac >> 12 | 224);
          _0x577056 += String["fromCharCode"](_0x6189ac >> 6 & 63 | 128);
          _0x577056 += String["fromCharCode"](_0x6189ac & 63 | 128);
        }
      }
    }

    return _0x577056;
  }

  function _0x37f0cd(_0x536fde) {
    var _0x57d084 = "0123456789abcdef";
    var _0x5f16c6 = "";

    for (var _0x39c170 = 0; _0x39c170 < _0x536fde["length"] * 4; _0x39c170++) {
      _0x5f16c6 += _0x57d084["charAt"](_0x536fde[_0x39c170 >> 2] >> (3 - _0x39c170 % 4) * 8 + 4 & 15) + _0x57d084["charAt"](_0x536fde[_0x39c170 >> 2] >> (3 - _0x39c170 % 4) * 8 & 15);
    }

    return _0x5f16c6;
  }

  _0xb3a2f3 = _0x4756fb(_0xb3a2f3);
  return _0x37f0cd(_0x58103a(_0xe1c49c(_0xb3a2f3), _0xb3a2f3["length"] * _0x436214));
}

function go(_0x50cd53) {
  function _0x42fc6c() {
    var _0x20ef9d = window["navigator"]["userAgent"],
        _0x54abc6 = ["Phantom"];

    for (var _0x27b17f = 0; _0x27b17f < _0x54abc6["length"]; _0x27b17f++) {
      if (_0x20ef9d["indexOf"](_0x54abc6[_0x27b17f]) != -1) {
        return true;
      }
    }

    if (window["callPhantom"] || window["_phantom"] || window["Headless"] || window["navigator"]["webdriver"] || window["navigator"]["__driver_evaluate"] || window["navigator"]["__webdriver_evaluate"]) {
      return true;
    }
  }

  if (_0x42fc6c()) {
    return;
  }

  var _0x171728 = new Date();

  function _0x107d5a(_0x3569e5, _0x3a4385) {
    var _0x26d368 = _0x50cd53["chars"]["length"];

    for (var _0x2f27d0 = 0; _0x2f27d0 < _0x26d368; _0x2f27d0++) {
      for (var _0x2726ec = 0; _0x2726ec < _0x26d368; _0x2726ec++) {
        var _0x58eac9 = _0x3a4385[0] + _0x50cd53["chars"]["substr"](_0x2f27d0, 1) + _0x50cd53["chars"]["substr"](_0x2726ec, 1) + _0x3a4385[1];

        if (hash(_0x58eac9) == _0x3569e5) {
          return [_0x58eac9, new Date() - _0x171728];
        }
      }
    }
  }

  var _0x454576 = _0x107d5a(_0x50cd53["ct"], _0x50cd53["bts"]);

  if (_0x454576) {
    var _0x3fef91;

    if (_0x50cd53["wt"]) {
      _0x3fef91 = parseInt(_0x50cd53["wt"]) > _0x454576[1] ? parseInt(_0x50cd53["wt"]) - _0x454576[1] : 500;
    } else {
      _0x3fef91 = 1500;
    }


      let c = _0x50cd53["tn"] + "=" + _0x454576[0] + ";Max-age=" + _0x50cd53["vt"] + "; path = /";
      return c;

  } else {
    alert("\u8BF7\u6C42\u9A8C\u8BC1\xE5\xA4\xB1\xE8\xB4\xA5");
  }
}

console.log(go({"bts":["1628085220.599|0|tiI","3%2FYgQQn8dPhB2M%2FaZ%2Br%2FxM%3D"],"chars":"fcWjlrafYQYbXeqadeXCvr","ct":"49fe40ac16199b24ad4c096b09d73d39dbc07cccab4aa2d53a6304acdc31e931","ha":"sha256","tn":"__jsl_clearance_s","vt":"3600","wt":"1500"}
));