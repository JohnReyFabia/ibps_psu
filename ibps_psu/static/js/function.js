// Code By Webdevtrick ( https://webdevtrick.com )
//Switcher function:
$(".tab").click(function () {
  //Spot switcher:
  $(this).parent().find(".tab").removeClass("activeTab");
  $(this).addClass("activeTab");
});
