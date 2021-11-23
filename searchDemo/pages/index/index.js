//index.js
Page({
  data: {
    // 输入框数据
    inputStr:''
  },
  //提交搜索
  searchConfirm: function () {
    // 判断是否是空字符串
    if (this.data.inputStr||this.data.inputStr===0) {
      getApp().search = this.data.inputStr;
      wx.switchTab({
        url: '../repositories/repositories'
      });
    }
  },
  // 记录输入数据
  recordSearch:function(event){
    this.data.inputStr = event.detail.value;
  }
})
