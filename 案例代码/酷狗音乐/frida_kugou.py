# -*- coding: utf-8 -*-
# @Time    : 2021/10/19 9:32
# @Author  : lx
# @IDE ：PyCharm

# 版本 10.0.7
#frida -U -l exploit.js -f com.package.name

import frida
d = frida.get_remote_device()
f = d.get_frontmost_application()
print(f)


import frida, sys

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


jscode_hook = """
Java.perform(
    function(){
            console.log("1. start hook");
            var ba = Java.use("com.kugou.common.utils.ba");
            if (ba != undefined) {
                console.log("2. find class");
                ba.b.overload('java.lang.String').implementation = function (a) {
                    console.log("计算参数a: " + a);
                    var res = ba.b(a);
                    console.log("计算result:" + res);
                    return res;
                }
            }
    }
)
"""

process = frida.get_usb_device().attach('com.kugou.android')
script = process.create_script(jscode_hook)
script.on('message', on_message)
print('[*] Hook Start Running')
script.load()
sys.stdin.read()

