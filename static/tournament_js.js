function update_bracket(match_id){
  var request = new XMLHttpRequest();
  var winner_id = $('input[name="'+match_id+'"]:checked').val();
  var url = document.getElementById('bracket_url').value;
  $("*").css("cursor", "progress");
  request.open("POST", '/reportTournament', true);
  request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  request.send("bracket_url="+url+"&match_id="+match_id+"&winner_id="+winner_id) 
  request.onreadystatechange=function(){
    if(request.readyState==4 && request.responseText){
      var list = JSON.parse(request.responseText);
      var bracket_url = document.getElementById('bracket_url').value;
      document.getElementById('reloader').innerHTML = '<object data="http://challonge.com/'+bracket_url+'/module?theme=3191" class="embedwindow">';
      closePopup(match_id);
      document.getElementById('popups').innerHTML = "";
      document.getElementById('report').innerHTML = "";
      for(var i = 0; i < list.length; i++){
        document.getElementById('report').innerHTML += '<option value="'+list[i].match_id+'">'+list[i].identifier+'</option>';
        document.getElementById('popups').innerHTML += '<div id="Popup-'+list[i].match_id+'" class="popup"></div>';
        document.getElementById('Popup-'+list[i].match_id).innerHTML += '<img id="close" src="/static/assets/x.png" align="right" onclick="closePopup('+list[i].match_id+')">';
        document.getElementById('Popup-'+list[i].match_id).innerHTML += '<p>ENTER RESULTS HERE</p><br><br>';
        document.getElementById('Popup-'+list[i].match_id).innerHTML += '<input type="radio" class="playerEnter" name="'+list[i].match_id+'" id="'+list[i].match_id+'" value="'+list[i].player1_id+'" checked>'+list[i].player1+'</input>';
        document.getElementById('Popup-'+list[i].match_id).innerHTML += '<input type="radio" class="playerEnter" name="'+list[i].match_id+'" id="'+list[i].match_id+'" value="'+list[i].player2_id+'">'+list[i].player2+'</input><br><br>';
        document.getElementById('Popup-'+list[i].match_id).innerHTML += '<button class="button" onclick="update_bracket('+list[i].match_id+')">Submit</button><br>';
      }
      $("*").css("cursor", "default");
    }
  }
}

function createPopup(){
  var match_id = document.getElementById('report').value;
  document.getElementById('Popup-'+match_id).style.display="block";
  document.getElementById('fade').style.display='block';
}

function closePopup(match_id){
  document.getElementById('fade').style.display="none";
  document.getElementById('Popup-'+match_id).style.display="none"; 
}