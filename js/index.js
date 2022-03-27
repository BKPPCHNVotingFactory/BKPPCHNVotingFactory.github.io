// tab 激活状态
$(function () {
  $("#myMenu li").click(function () {
    $(this).children("a").addClass("tab_active");
    $(this).siblings().children("a").removeClass("tab_active");
  });
});