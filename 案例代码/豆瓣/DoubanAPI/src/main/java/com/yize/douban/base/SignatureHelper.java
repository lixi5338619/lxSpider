package com.yize.douban.base;

import com.yize.douban.util.AesEncrypt;
import com.yize.douban.util.HMACHash1;
import com.yize.douban.util.TextUtils;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Map;

public class SignatureHelper {
    private static final char[] HEX_DIGITS = "0123456789ABCDEF".toCharArray();
    private static final String DEFAULT_ENCODING = "UTF-8";
    public static final String AMPERSAND = "&";
    private final static int NOT_FOUND = -1;
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
    public static Map<String, String> getVerifyMap(String str, String str2, String str3) {
        Map<String, String> map=new HashMap<>();
        String decode;
        if (TextUtils.isEmpty(str)) {
            return null;
        }
        //String str4= AesEncrypt.encrypt(TEXT,SIGN);
        String str4 = "bf7dddc7c9cfe6f7";
        if (TextUtils.isEmpty(str4)) {
            return null;
        }
        StringBuilder sb = new StringBuilder();
        sb.append(str2);
        String encodedPath = encodedPath(str);
        System.out.println(encodedPath);
        if (encodedPath == null || (decode = encodedPath) == null) {
            return null;
        }
        if (decode.endsWith("/")) {
            decode = decode.substring(0, decode.length() - 1);
        }
        sb.append(AMPERSAND);
        sb.append(uriEncode(decode,null));
        if (!TextUtils.isEmpty(str3)) {
            sb.append(AMPERSAND);
            sb.append(str3);
        }
        long currentTimeMillis = System.currentTimeMillis() / 1000;
        sb.append(AMPERSAND);
        sb.append(currentTimeMillis);
        try {
            map.put("_sig", URLEncoder.encode(HMACHash1.a(str4, sb.toString()),"utf-8"));
        } catch (Exception e) {
            e.printStackTrace();
        }
        map.put("_ts",String.valueOf(currentTimeMillis));
        return map;
    }

    public static String uriEncode(String s, String allow) {
        if (s == null) {
            return null;
        }

        // Lazily-initialized buffers.
        StringBuilder encoded = null;

        int oldLength = s.length();

        // This loop alternates between copying over allowed characters and
        // encoding in chunks. This results in fewer method calls and
        // allocations than encoding one character at a time.
        int current = 0;
        while (current < oldLength) {
            // Start in "copying" mode where we copy over allowed chars.

            // Find the next character which needs to be encoded.
            int nextToEncode = current;
            while (nextToEncode < oldLength
                    && isAllowed(s.charAt(nextToEncode), allow)) {
                nextToEncode++;
            }

            // If there's nothing more to encode...
            if (nextToEncode == oldLength) {
                if (current == 0) {
                    // We didn't need to encode anything!
                    return s;
                } else {
                    // Presumably, we've already done some encoding.
                    encoded.append(s, current, oldLength);
                    return encoded.toString();
                }
            }

            if (encoded == null) {
                encoded = new StringBuilder();
            }

            if (nextToEncode > current) {
                // Append allowed characters leading up to this point.
                encoded.append(s, current, nextToEncode);
            } else {
                // assert nextToEncode == current
            }

            // Switch to "encoding" mode.

            // Find the next allowed character.
            current = nextToEncode;
            int nextAllowed = current + 1;
            while (nextAllowed < oldLength
                    && !isAllowed(s.charAt(nextAllowed), allow)) {
                nextAllowed++;
            }

            // Convert the substring to bytes and encode the bytes as
            // '%'-escaped octets.
            String toEncode = s.substring(current, nextAllowed);
            try {
                byte[] bytes = toEncode.getBytes(DEFAULT_ENCODING);
                int bytesLength = bytes.length;
                for (int i = 0; i < bytesLength; i++) {
                    encoded.append('%');
                    encoded.append(HEX_DIGITS[(bytes[i] & 0xf0) >> 4]);
                    encoded.append(HEX_DIGITS[bytes[i] & 0xf]);
                }
            } catch (UnsupportedEncodingException e) {
                throw new AssertionError(e);
            }

            current = nextAllowed;
        }

        // Encoded could still be null at this point if s is empty.
        return encoded == null ? s : encoded.toString();
    }

    private static boolean isAllowed(char c, String allow) {
        return (c >= 'A' && c <= 'Z')
                || (c >= 'a' && c <= 'z')
                || (c >= '0' && c <= '9')
                || "_-!.~'()*".indexOf(c) != NOT_FOUND
                || (allow != null && allow.indexOf(c) != NOT_FOUND);
    }

    public static String encodedPath(String url) {
        String scheme="https";
        int pathStart = url.indexOf('/', scheme.length() + 3); // "://".length() == 3.
        int pathEnd = delimiterOffset(url, pathStart, url.length(), "?#");
        return url.substring(pathStart, pathEnd);
    }

    public static int delimiterOffset(String input, int pos, int limit, String delimiters) {
        for(int i = pos; i < limit; ++i) {
            if (delimiters.indexOf(input.charAt(i)) != -1) {
                return i;
            }
        }
        return limit;
    }
}