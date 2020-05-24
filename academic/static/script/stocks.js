$(function(){
  $.getJSON("../static/json/stocks.json", function(data){
    $("#usdjpy").html(data["USDJPY"]["integer"]);
    $("#uj_dec").html(data["USDJPY"]["decimal"]);
})
})