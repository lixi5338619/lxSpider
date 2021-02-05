package com.yize.douban.base;
import com.yize.douban.util.HttpRequestHelper;
import java.util.HashMap;
import java.util.Map;

public class DoubanWebRequest {
    public final static String UA_DOUBAN_ANDROID="api-client/1 com.douban.frodo/6.42.2(194) Android/22 product/shamu vendor/OPPO model/OPPO R11 Plus  rom/android  network/wifi  platform/mobile nd/1";

    public static String builder(String baseLink,Map<String,String> paramsMap){
        StringBuilder sb=new StringBuilder();
        sb.append(baseLink+"?");

        Map<String,String> verifyMap=SignatureHelper.getVerifyMap(baseLink,"GET",null);
        for (String key:paramsMap.keySet()){
            sb.append("&"+key+"="+paramsMap.get(key));
        }
        for (String key: verifyMap.keySet()){
            sb.append("&"+key+"="+verifyMap.get(key));
        }
        return sb.toString();
    }

    public static String downloadWebSiteUseGet(String baseLink, Map<String,String> paramsMap,Map<String,String> headerMap){
        if(headerMap==null){
            headerMap=new HashMap<>();
            headerMap.put("User-Agent",UA_DOUBAN_ANDROID);
        }
        paramsMap.put("apikey","0dad551ec0f84ed02907ff5c42e8ec70");
        return HttpRequestHelper.downloadWebSiteUseGet(builder(baseLink,paramsMap),headerMap);
    }

    public static String downloadWebSiteUseGet(String baseLink, Map<String,String> paramsMap){
        return downloadWebSiteUseGet(baseLink,paramsMap,null);
    }
}
