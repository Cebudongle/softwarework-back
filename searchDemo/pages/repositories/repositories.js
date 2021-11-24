// 获取后台数据函数
function getSearch(callback) {
    //用wx.request直接请求api
    wx.request({
        url: 'https://api.github.com/search/repositories',// 查询库api
        data: {
            q: getApp().search,//输入的关键字
            per_page: 15,   //分页-每页包含的数量
            page: pageNum,  //要查询的页数，pageNum为1
            client_id: "GitHub Search",
            client_secret: "0067e8e5bbbde8e9553cc2d69504b859d3218b5c"
        },
        method: 'GET',
        dataType: 'jsonp',
        header: {
            'content-type': 'application/json'
        },
        success: function (res) {
            // 需要对json字符串格式化
            var dataTmp = JSON.parse(res.data);
            // 调用回调函数
            callback(dataTmp);
            console.log('请求成功',res)
        },
        fail: function (res) {
            // fail，不做什么
        },
        complete: function (res) {
            console.log('请求成功',res)
        }
    });
}

// 记录要查询的页数
var pageNum = 1;

Page({
    data: {
        // 搜索结果数量
        result: "",
        // 搜索结果
        list: [
        ],
        // 本次搜索词
        search: ""
    },
    onShow: function () {
        // 判断上一次搜索词与当前搜索词是否一致
        if (this.data.search !== getApp().search) {
            // 不一致则重新发起请求
            // 存储本次搜索词
            this.setData({
                search: getApp().search
            });
            // 设置标题栏
            wx.setNavigationBarTitle({
                title: 'Search for ' + getApp().search
            });
            // 在页面加载完成后、得到数据前，打开等待窗口
            wx.showLoading({
                title: '加载中'
            });
            // 查询第一页
            pageNum = 1;
            var that = this;
            // 获取数据
            getSearch(function (dataTmp) {
                // 更新数据
                that.setData({
                    result: dataTmp.total_count,
                    list: dataTmp.items
                });
                // 关闭等待窗口
                wx.hideLoading();
            });
        }
    },
    // 下拉刷新
    onPullDownRefresh: function () {
        // 开启标题栏等待样式
        wx.showNavigationBarLoading();
        // 查询第一页
        pageNum = 1;
        var that = this;
        getSearch(function (dataTmp) {
            that.setData({
                result: dataTmp.total_count,
                list: dataTmp.items
            });
            // 关闭标题栏等待样式
            wx.hideNavigationBarLoading();
            // 停止当前页面下拉刷新
            wx.stopPullDownRefresh();
        });
    },
    // 触底事件
    onReachBottom: function () {
        // 开启标题栏等待样式
        wx.showNavigationBarLoading();
        // 查询下一页
        pageNum++;
        var that = this;
        getSearch(function (dataTmp) {
            // 拼接数据
            var tmp = that.data.list.concat(dataTmp.items);
            that.setData({
                list: tmp
            });
            // 关闭标题栏等待样式
            wx.hideNavigationBarLoading();
        });
    }
})