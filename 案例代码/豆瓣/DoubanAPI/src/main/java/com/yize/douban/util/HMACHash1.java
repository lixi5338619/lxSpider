package com.yize.douban.util;

import com.yize.douban.util.Base64;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;


public class HMACHash1 {
    public static final String HMAC_SHA1 = "HmacSHA1";
    public static final String a(String str, String str2) {
        try {
            SecretKeySpec secretKeySpec = new SecretKeySpec(str.getBytes(),HMAC_SHA1);
            Mac instance = Mac.getInstance(HMAC_SHA1);
            instance.init(secretKeySpec);
            return Base64.encodeToString(instance.doFinal(str2.getBytes()), 2);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }


}