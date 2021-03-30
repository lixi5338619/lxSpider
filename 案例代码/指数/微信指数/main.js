// toast('Hello, Auto.js');
app.launchApp('微信');

//返回到首页
function goToHomePage(){    
    let k = 0;
    while(k < 30){
        k = k + 1;        
        if(text("微信").depth(10).exists()){
            //要支持的动作
            toast('已到首页');  
            break;
        }else{
            back();
            sleep(1000*0.2);
        }
    }
}

// goToHomePage()
// exit();

//前往公众号搜索
function goToSearchPage(){
    //搜索按钮
    var it = className("android.widget.ImageView").depth(17).findOne();
    var b = it.bounds();
    click(b.centerX(), b.centerY());
    sleep(500);
    text('公众号').click();
    sleep(1000);    
    text('公众号').click();
}

//获取界面上的搜索结果
function getSearchResult(saveArray){
    sleep(500);
    let tList = depth(18).find();//从第 18 级开始取元素

    for(let i=0;tList && i<tList.length;i++){
        let item = {title:'',desc:'',idx:0};
        if(tList[i].childCount() > 0){
            let indexInParent = tList[i].indexInParent();// 搜索出来第几个  索引
            // toastLog('索引:' + indexInParent);sleep(1000*0.5);

            let cell = tList[i].child(0);// 19
            if(cell && cell.childCount() > 2){
                cell = cell.child(2);//20
                let title = '';
                let desc = '';
                if(cell.childCount() >= 3){
                    title = cell.child(1).text();//21
                    desc = cell.child(2).text();//21    
                }else{
                    title = cell.child(0).text();//21
                    desc = cell.child(1).text();//21    
                }
                // toastLog(title);    
                // sleep(1000*2);
                // toastLog(desc);    
                // sleep(1000*2);

                item.idx = indexInParent;
                item.title = title;
                item.desc = desc;

            }else if(cell && cell.childCount() > 1){
                cell = cell.child(1);//20
                let title = cell.child(0).text();//21
                let desc = cell.child(1).text();//21
                // toastLog(title);    
                // sleep(1000*2);
                // toastLog(desc);    
                // sleep(1000*2);

                item.idx = indexInParent;
                item.title = title;
                item.desc = desc;

            }else{
                // toastLog(cell);
            }            
        }

        //往数组里面添加索引结果
        if(item.idx != 0){
            if(saveArray.length > 0){
                if(item.idx > saveArray[saveArray.length - 1].idx){
                    saveArray.push(item);
                }
            }else{
                saveArray.push(item);
            }
        }

    }
    
}

//滑动搜索结果
function swapSearchResult(){
    scrollDown();
}

function searchForKey(tkey){
    sleep(1000*1.5);
    //设置输入框里面的文字
    id('m7').findOne().setText(tkey);

    //点击键盘上面的'搜索'按钮
    click(device.width - 8, device.height - 8);

    var saveArray = [];
    var rounds = 200;
    for(var i=0;i<rounds;i++){
        try {
            getSearchResult(saveArray);            
        } catch (error) {
            console.log('查行记录异常');
            console.error(error);
        }
        try {
            swapSearchResult();         
        } catch (error) {
            console.log('翻页异常');
            // console.error(error);
        }
        sleep(1000*0.2);
    //  log('testmemem');
        if(text("没有更多的搜索结果").exists()){
            toast('搜索结束');        
            console.log('查找结果', JSON.stringify(saveArray));
            break;
        }
    }
    console.log('查找结果', JSON.stringify(saveArray));
    toast(JSON.stringify(saveArray));

    //TODO. 保存本地  或者 保存到云服务器
}

//跳转到指数页面 
function goToZhiShuPage(){
    var it = className("android.widget.ImageView").depth(17).findOne();
    var b = it.bounds();
    click(b.centerX(), b.centerY());
    sleep(1500);

    //跳转到 微信指数 小程序    
    id('m7').findOne().setText('微信指数');
    sleep(1000);

    var wxzs = text('微信指数').depth(14).findOne();
    var bb = wxzs.bounds();
    click(bb.centerX(), bb.centerY());
}

//根据关键字查 指数
function getZhiShuForKey(tkey){
    sleep(1000*1.5);
    var wxzs = text('搜索').findOne();
    var bb = wxzs.bounds();
    click(bb.centerX(), bb.centerY());
    
    className('android.widget.EditText').findOne().setText(tkey);
    sleep(1000);

    //点击键盘上面的'搜索'按钮
    click(device.width - 16, device.height - 16);
    sleep(1000*2);

    //获取关键字和指数
    let findData = {keyword:tkey, //关键字
        dataKey:'',//时间戳，显示在界面上的时间
         zhishu:''//指数值
        };

    //TODO. 可以通过 xxx日统计 的正则表达式来搜索到具备该文本的控件，然后通过它的上级的上级的下级的下级，这样去查找指数
    try {
        //此处没调通
        findData.dataKey = className('android.view.View').findOne().text();
    } catch (error) {
        toast(error);
        exit();
    }

    // try {
    //     findData.zhishu = className('android.view.View').depth(22).indexInParent(1).findOne().text();
    // } catch (error) {
    //     toast(error);
    //     exit();
    // }    

    toast('日期' + findData.dataKey + ', 指数' + findData.zhishu);

    //TODO. 保存本地  或者 保存到云服务器
}


// ---------  查找关键字逻辑 -------
if(1){
    goToHomePage();
    goToSearchPage();
    searchForKey('起名');
    sleep(1000);
    goToHomePage();    
}

// ---------  查找小程序“微信指数”逻辑 ------

if(1){
    goToHomePage();
    goToZhiShuPage();
    getZhiShuForKey('起名');
    sleep(1000);
    // goToHomePage();

}