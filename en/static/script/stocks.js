$(function(){
  $.getJSON("../static/json/stocks.json", function(data){
    $("#usdjpy").html(data["EURUSD"]["integer"]);
    $("#uj_dec").html(data["EURUSD"]["decimal"]);
})
})