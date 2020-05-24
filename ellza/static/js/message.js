$('#chat_text').keydown(function(event){
  if(event.keycode==13){event.preventDefault();func();}})
$('#submit_button').on('click', function(event){event.preventDefault();func();})
function func(){
$(function(){
if($('#chat_text').val()!='' && $('#chat_text').val().match(/\S/g)){
  var txt = $('#chat_text').val();
  var hhtml = "<div class='usr'><div class='guest'>" + esc(txt) + "</div></div>";
  $('#chat').html($('#chat').html()+hhtml);
  var data = $('form').serialize();
  $('#chat_text').val('');
  $('input').blur();
  window.scroll(0,$(document).height());
  $.ajax({
    url: '/',
    type: 'POST',
    data: data,
    success: function(bot){
        var html = "<div class='bot'><img class='icon' src='../static/images/ell.png'><div class='ellza'>";
        if(Object.keys(bot['results']).length !== 0){
          if(bot['results'][0]['help']){
            html += esc(bot['results'][0]['title']) + "<div class='help'>" + bot['results'][0]['help'] + "</div></div></div>";
          }else if(bot['results'][0]['chatbot']){
            html += esc(bot['results'][0]['chatbot']);
          }else if(bot['results'][0]['source']){
            var i = 0;
            while(bot['results'][i]){
              html += "<div class='time'>" + esc(bot['results'][i]['time']) + "</div><a href='"+ bot['results'][i]['url']+"' target='_blank'>"+ esc(bot['results'][i]['title']) +"</a><div class ='url'>by " + esc(bot['results'][i]['source'])+ "</div><br>"; 
              i++;
              }
              html+="</div></div>";
          }else if(bot['results'][0]['thumb_src']){
            var i = 0;
            while(bot['results'][i]){
              html += "<br><a href='"+ bot['results'][i]['img_src']+"' target='_blank'><img class='imsrc' src='"+ bot['results'][i]['thumb_src'] +"'></a><br><div class='url'>" + bot['results'][i]['d_url'] + "</div><a href='" + bot['results'][i]['url']+ "' target='_blank'>Website</a><br>"; i++;
              }
              html+="<br></div></div>";
          }else if(Object.keys(bot['results']).length == 2){
            if(bot['results'][1]['url']){
              html += "<a href='"+ bot['results'][1]['url']+"' target='_blank'>"+ esc(bot['results'][1]['title']) +"</a><div class='url'>" + esc(bot['results'][1]['d_url'])+ "</div><br>";
              }
            if(bot['results'][0]['url']){
              html += "<a href='"+ bot['results'][0]['url']+"' target='_blank'>"+ esc(bot['results'][0]['title']) +"</a><div class='url'>" + esc(bot['results'][0]['d_url'])+ "</div><div class='descr'>" + esc(bot['results'][0]['descr']);
              }
            html+= "</div></div>";
          }else{
             html += "検索結果が見つかりません</div></div>";
          }
        }else{
          html += "検索結果が見つかりません</div></div>";
        }
          $('#chat').html($('#chat').html()+html);
          window.scroll(0,$(document).height());
          var ua = navigator.userAgent;
          if(!(ua.indexOf('iPhone') > 0) && !(ua.indexOf('Android') > 0 && ua.indexOf('Mobile') > 0)){
            $('#chat_text').focus();
        }
    },
  });
}else{return false;}
});
}

function esc(s){
  return s.replace('&', '&amp;').replace('<','&lt;')
          .replace('>', '&gt;').replace("'", '&#x27;')
          .replace('`', '&#x60;').replace('"', '&quot;');
}