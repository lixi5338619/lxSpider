package com.yize.test;

import com.yize.douban.util.AesEncrypt;
import org.junit.Test;

public class TestEncrypt {

    /**
     * 经过android的Base64加密后的豆瓣APP签名信息，每个版本都是固定的
     *
     * 在安卓里面可以这样获取：
     * Application application=(Application)getApplicationContext();
     * PackageInfo packageInfo=application.getPackageManager().getPackageInfo("com.douban.frodo",PackageManager.GET_SIGNATURES);
     * String sign=Base64.encodeToString(packageInfo.signatures[0].toByteArray(),0);
     *
     * 这里直接给出一个版本的豆瓣APP的签名信息
     */
        public final static String SIGN="MIICUjCCAbsCBEty1MMwDQYJKoZIhvcNAQEEBQAwcDELMAkGA1UEBhMCemgxEDAOBgNVBAgTB0Jl\n" +
            "aWppbmcxEDAOBgNVBAcTB0JlaWppbmcxEzARBgNVBAoTCkRvdWJhbiBJbmMxFDASBgNVBAsTC0Rv\n" +
            "dWJhbiBJbmMuMRIwEAYDVQQDEwlCZWFyIFR1bmcwHhcNMTAwMjEwMTU0NjExWhcNMzcwNjI3MTU0\n" +
            "NjExWjBwMQswCQYDVQQGEwJ6aDEQMA4GA1UECBMHQmVpamluZzEQMA4GA1UEBxMHQmVpamluZzET\n" +
            "MBEGA1UEChMKRG91YmFuIEluYzEUMBIGA1UECxMLRG91YmFuIEluYy4xEjAQBgNVBAMTCUJlYXIg\n" +
            "VHVuZzCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAg622fxLuwQtC8KLYp5gHk0OmfrFiIisz\n" +
            "kzPLBhKPZDHjYS1URhQpzf00T8qg2oEwJPPELjN2Q7YOoax8UINXLhMgFQkyAvMfjdEOSfoKH93p\n" +
            "v2d4n/IjQc/TaDKu6yb53DOq76HTUYLcfLKOXaGwGjAp3QqTqP9LnjJjGZCdSvMCAwEAATANBgkq\n" +
            "hkiG9w0BAQQFAAOBgQA3MovcB3Hv4bai7OYHU+gZcGQ/8sOLAXGD/roWPX3gm9tyERpGztveH35p\n" +
            "aI3BrUWg2Vir0DRjbR48b2HxQidQTVIH/HOJHV0jgYNDviD18/cBwKuLiBvdzc2Fte+zT0nnHXMy\n" +
            "E6tVeW3UdHC1UvzyB7Qcxiu4sBiEO1koToQTWw==\n";
    /**
     * 反编译豆瓣后得到的一个常量，在豆瓣APP里面固定写死了,具体位置看我的图文解析
     */
    public final static String TEXT="bHUvfbiVZUmm2sQRKwiAcw==";

        @Test
        public void testEncrypt(){
//            String hmacKey= AesEncrypt.encrypt(TEXT,SIGN);
//            System.out.println(hmacKey);//输出结果是：bf7dddc7c9cfe6f7
        }
}
