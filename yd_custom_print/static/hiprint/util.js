// 复制
var copy_txt = function () {//无组件复制
    var _this = this;
    this.copy = function (txt) {

        $("#input_copy_txt_to_board").val(txt);//赋值
        $("#input_copy_txt_to_board").removeClass("hide");//显示
        $("#input_copy_txt_to_board").focus();//取得焦点
        $("#input_copy_txt_to_board").select();//选择
        document.execCommand("Copy");
        $("#input_copy_txt_to_board").addClass("hide");//隐藏
    }

    let html = '<input type class="hide" id="input_copy_txt_to_board" value="" />';//添加一个隐藏的元素
    $("body").append(html);
}
