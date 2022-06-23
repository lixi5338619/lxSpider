window = {}
window.navigator={
'userAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}
function hash(_0x3cb311) {
  function _0x163c9c(_0x46ff88, _0x5150cb) {
    return (_0x46ff88 & 2147483647) + (_0x5150cb & 2147483647) ^ _0x46ff88 & 2147483648 ^ _0x5150cb & 2147483648;
  }

  function _0x26ec8d(_0x3d80d1) {
    var _0x4e7763 = "0123456789abcdef";
    var _0x1603cb = "";

    for (var _0x4a1d1d = 7; _0x4a1d1d >= 0; _0x4a1d1d--) {
      _0x1603cb += _0x4e7763["charAt"](_0x3d80d1 >> _0x4a1d1d * 4 & 15);
    }

    return _0x1603cb;
  }

  function _0x153602(_0x2c0782) {
    var _0x1cd5a1 = (_0x2c0782["length"] + 8 >> 6) + 1,
        _0x1db977 = new Array(_0x1cd5a1 * 16);

    for (var _0x17fd51 = 0; _0x17fd51 < _0x1cd5a1 * 16; _0x17fd51++) {
      _0x1db977[_0x17fd51] = 0;
    }

    for (_0x17fd51 = 0; _0x17fd51 < _0x2c0782["length"]; _0x17fd51++) {
      _0x1db977[_0x17fd51 >> 2] |= _0x2c0782["charCodeAt"](_0x17fd51) << 24 - (_0x17fd51 & 3) * 8;
    }

    _0x1db977[_0x17fd51 >> 2] |= 128 << 24 - (_0x17fd51 & 3) * 8;
    _0x1db977[_0x1cd5a1 * 16 - 1] = _0x2c0782["length"] * 8;
    return _0x1db977;
  }

  function _0x37aa8c(_0x1b0f9a, _0x48e60d) {
    return _0x1b0f9a << _0x48e60d | _0x1b0f9a >>> 32 - _0x48e60d;
  }

  function _0x3ba558(_0x3e8bd0, _0x360d42, _0x2cf1fe, _0x2d6f7f) {
    if (_0x3e8bd0 < 20) {
      return _0x360d42 & _0x2cf1fe | ~_0x360d42 & _0x2d6f7f;
    }

    if (_0x3e8bd0 < 40) {
      return _0x360d42 ^ _0x2cf1fe ^ _0x2d6f7f;
    }

    if (_0x3e8bd0 < 60) {
      return _0x360d42 & _0x2cf1fe | _0x360d42 & _0x2d6f7f | _0x2cf1fe & _0x2d6f7f;
    }

    return _0x360d42 ^ _0x2cf1fe ^ _0x2d6f7f;
  }

  function _0x23a48b(_0x3f81a0) {
    return _0x3f81a0 < 20 ? 1518500249 : _0x3f81a0 < 40 ? 1859775393 : _0x3f81a0 < 60 ? -1894007588 : -899497514;
  }

  var _0x1cdcad = _0x153602(_0x3cb311);

  var _0x32dc39 = new Array(80);

  var _0xccaec7 = 1732584193;

  var _0x32e008 = -271733879;

  var _0x485153 = -1732584194;

  var _0x489b5b = 271733878;

  var _0x205716 = -1009589776;

  for (var _0x41a7c6 = 0; _0x41a7c6 < _0x1cdcad["length"]; _0x41a7c6 += 16) {
    var _0x152b2d = _0xccaec7;
    var _0x1cd17d = _0x32e008;
    var _0xf419f9 = _0x485153;
    var _0x536541 = _0x489b5b;
    var _0x34be50 = _0x205716;

    for (var _0x6d61ab = 0; _0x6d61ab < 80; _0x6d61ab++) {
      if (_0x6d61ab < 16) {
        _0x32dc39[_0x6d61ab] = _0x1cdcad[_0x41a7c6 + _0x6d61ab];
      } else {
        _0x32dc39[_0x6d61ab] = _0x37aa8c(_0x32dc39[_0x6d61ab - 3] ^ _0x32dc39[_0x6d61ab - 8] ^ _0x32dc39[_0x6d61ab - 14] ^ _0x32dc39[_0x6d61ab - 16], 1);
      }

      t = _0x163c9c(_0x163c9c(_0x37aa8c(_0xccaec7, 5), _0x3ba558(_0x6d61ab, _0x32e008, _0x485153, _0x489b5b)), _0x163c9c(_0x163c9c(_0x205716, _0x32dc39[_0x6d61ab]), _0x23a48b(_0x6d61ab)));
      _0x205716 = _0x489b5b;
      _0x489b5b = _0x485153;
      _0x485153 = _0x37aa8c(_0x32e008, 30);
      _0x32e008 = _0xccaec7;
      _0xccaec7 = t;
    }

    _0xccaec7 = _0x163c9c(_0xccaec7, _0x152b2d);
    _0x32e008 = _0x163c9c(_0x32e008, _0x1cd17d);
    _0x485153 = _0x163c9c(_0x485153, _0xf419f9);
    _0x489b5b = _0x163c9c(_0x489b5b, _0x536541);
    _0x205716 = _0x163c9c(_0x205716, _0x34be50);
  }

  return _0x26ec8d(_0xccaec7) + _0x26ec8d(_0x32e008) + _0x26ec8d(_0x485153) + _0x26ec8d(_0x489b5b) + _0x26ec8d(_0x205716);
}

function go(_0x3643f0) {
  function _0x939e9d() {
    var _0x25184e = window["navigator"]["userAgent"],
        _0x3d9896 = ["Phantom"];

    for (var _0x41f164 = 0; _0x41f164 < _0x3d9896["length"]; _0x41f164++) {
      if (_0x25184e["indexOf"](_0x3d9896[_0x41f164]) != -1) {
        return true;
      }
    }

    if (window["callPhantom"] || window["_phantom"] || window["Headless"] || window["navigator"]["webdriver"] || window["navigator"]["__driver_evaluate"] || window["navigator"]["__webdriver_evaluate"]) {
      return true;
    }
  }

  if (_0x939e9d()) {
    return;
  }

  var _0x4a8c9f = new Date();

  function _0x30c06b(_0x56f5b0, _0x447494) {
    var _0x59337c = _0x3643f0["chars"]["length"];

    for (var _0x197671 = 0; _0x197671 < _0x59337c; _0x197671++) {
      for (var _0x47ac04 = 0; _0x47ac04 < _0x59337c; _0x47ac04++) {
        var _0x357062 = _0x447494[0] + _0x3643f0["chars"]["substr"](_0x197671, 1) + _0x3643f0["chars"]["substr"](_0x47ac04, 1) + _0x447494[1];

        if (hash(_0x357062) == _0x56f5b0) {
          return [_0x357062, new Date() - _0x4a8c9f];
        }
      }
    }
  }

  var _0x4f0d12 = _0x30c06b(_0x3643f0["ct"], _0x3643f0["bts"]);

  if (_0x4f0d12) {
    var _0x1dae31;

    if (_0x3643f0["wt"]) {
      _0x1dae31 = parseInt(_0x3643f0["wt"]) > _0x4f0d12[1] ? parseInt(_0x3643f0["wt"]) - _0x4f0d12[1] : 500;
    } else {
      _0x1dae31 = 1500;
    }

      let c = _0x3643f0["tn"] + "=" + _0x4f0d12[0] + ";Max-age=" + _0x3643f0["vt"] + "; path = /";
      console.log(c);
      return c
  } else {
    alert("\u8BF7\u6C42\u9A8C\u8BC1\xE5\xA4\xB1\xE8\xB4\xA5");
  }
}

go({
  "bts": ["1628088065.4|0|rZGRv", "gwlQ6aBQ9ZCDZeup2IEk%3D"],
  "chars": "vMJCKTooRTjlkttqnCeuEL",
  "ct": "db970e51a07226e63edcf9153c748160de4a3622",
  "ha": "sha1",
  "tn": "__jsl_clearance_s",
  "vt": "3600",
  "wt": "1500"
});