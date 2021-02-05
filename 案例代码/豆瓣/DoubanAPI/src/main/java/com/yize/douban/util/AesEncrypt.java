package com.yize.douban.util;

import javax.crypto.Cipher;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.io.UnsupportedEncodingException;
import java.security.NoSuchAlgorithmException;

public class AesEncrypt {
    public static final String encrypt(String text,String key){
        SecretKeySpec spec=buildSpec(key);
        byte[] decode=Base64.decode(text,0);
        Cipher instance= null;
        try {
            instance = Cipher.getInstance("AES/CBC/NoPadding");
            instance.init(2,spec,new IvParameterSpec("DOUBANFRODOAPPIV".getBytes()));
            return new String(instance.doFinal(decode));
        } catch (Exception e) {
            e.printStackTrace();
        }
        return text;
    }

    private static SecretKeySpec buildSpec(String key) {
        byte[] b;
        if(key==null){
            key="";
        }
        StringBuilder sb=new StringBuilder();
        sb.append(key);
        while (sb.length()<16){
            sb.append("\u0000");
        }
        if(sb.length()>16){
            sb.setLength(16);
        }
        try {
            b=sb.toString().getBytes("utf-8");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
            b=null;
        }
        return new SecretKeySpec(b,"AES");
    }
}
