package com.yize.douban.module;

import com.yize.douban.base.DoubanWebRequest;
import java.util.HashMap;

import static com.yize.douban.module.UrlModule.movieNewListApi;
import static com.yize.douban.module.UrlModule.photoRequestApi;

public class CelebrityPhoto {
    public String requestCelebrityMovie(String start,String count){
        HashMap<String,String> paramsMap=new HashMap<>();
        paramsMap.put("count",count+"");
        paramsMap.put("start",start+"");
        String response= DoubanWebRequest.downloadWebSiteUseGet(movieNewListApi,paramsMap);
        return response;
    }

    public String requestCelebrityPhoto(String photoId,String start,String count){
        HashMap<String,String> paramsMap=new HashMap<>();
        paramsMap.put("count",count+"");
        paramsMap.put("start",start+"");
        String response= DoubanWebRequest.downloadWebSiteUseGet(photoRequestApi.replace("photoid",photoId),paramsMap);
        return response;
    }
}
