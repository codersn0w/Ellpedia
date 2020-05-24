$(function(){
  $.getJSON("../static/json/weather.json", function(data){
    $("#tokyo_temp").html(data["Tokyo"]["temp"] + '°C');
    $("#ny_temp").html(data["New York"]["temp"] + '°C');
    $("#cp_temp").html(data["Cupertino"]["temp"] + '°C');
    $("#london_temp").html(data["London"]["temp"] + '°C');

    $("#tokyo").html('<img src="../static/weather_images/' + data["Tokyo"]["icon"] + '.png">');
    $("#ny").html('<img src="../static/weather_images/' + data["New York"]["icon"] + '.png">');
    $("#cp").html('<img src="../static/weather_images/' + data["Cupertino"]["icon"] + '.png">');
    $("#london").html('<img src="../static/weather_images/' + data["London"]["icon"] + '.png">');

    $("#last_updated_time").html(data["time"]);
})
})