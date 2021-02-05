package com.yize.douban.module;

import com.yize.douban.base.DoubanWebRequest;

public class UrlModule {
    //名人的图片example: "https://frodo.douban.com/api/v2/elessar/subject/27260217/photos?count=100&apikey=0dad551ec0f84ed02907ff5c42e8ec70&_sig=gfTX2YbSiADYaG%2FzXJ%2BpNo5IhbI%3D&_ts=1599316450"
    public final static String photoRequestApi="https://frodo.douban.com/api/v2/elessar/subject/photoid/photos";
    //电影排行榜 example: "https://frodo.douban.com/api/v2/movie/rank_list?apikey=0dad551ec0f84ed02907ff5c42e8ec70&s=rexxar_new&sugar=46000&loc_id=108288&_sig=ANPs38ZIIxIu5UD%2BiqKsnT%2F5AVA%3D&_ts=1599406040"
    public final static String movieRankListApi="https://frodo.douban.com/api/v2/movie/rank_list";

    public final static String movieNewListApi="https://frodo.douban.com/api/v2/tv/coming_soon";

}
