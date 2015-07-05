function uploadPhoto(){
  var request = new XMLHttpRequest();
  
  request.open("POST", '/photoUpload', true);
  request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  request.send("");
}

var loadFile = function(event) {
  var output = document.getElementById('output');
  output.src = URL.createObjectURL(event.target.files[0]);
};

function userInfo(){
  var request = new XMLHttpRequest();
  jQuery(".active").toggleClass("active")
  jQuery(".manage").toggleClass("active")
  jQuery(".userInfoLink").toggleClass("active")
  request.onreadystatechange=function(){
    if(request.readyState==4 && request.status==200){
      var list = JSON.parse(request.responseText);
      document.getElementById('content').innerHTML="";
      document.getElementById('content').innerHTML+='<h2>Leagues you are a member of:</h2>';
      for(var i = 0; i < list.length; i++){
        var league = list[i];
        displayUserInfo(league.name, league.urlkey, league.rank, league.score);
      }
    } else if(request.readyState==4){
      alert("somthing went wrong");
    }
  }
  request.open("GET", '/getUserInfo', true);
  request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  request.send("");
} 

/*
{'name':league_name, 'urlkey':key 'rank':memebr_rank, 'score':member_score}
*/
function displayUserInfo(leagueName, leagueKey, rank, score){
  var html = '<div class="panel panel-default col-md-6 col-md-offset-3">';
  html += '<div class="panel-heading text-center"><strong>'+leagueName+'</strong></div>';
  html += '<p align="center">Rank: '+rank+"</p>";
  html += '<p align="center">Score: '+score+"</p>";
  html += '<div id="buttonbar"><a href="/ranking?league_key_string='+leagueKey+'" class="button">See The Rankings</a></div><br></div>';
  document.getElementById('content').innerHTML += html;
}

function showAdmins(){
  var request = new XMLHttpRequest();
  $("*").css("cursor", "progress");
  request.onreadystatechange=function(){
    if(request.readyState==4 && request.status==200){
      jQuery(".active").toggleClass("active");
      jQuery(".manage").toggleClass("active");
      jQuery(".showAdminsLink").toggleClass("active");
      var list = JSON.parse(request.responseText);
      document.getElementById('content').innerHTML="";
      document.getElementById('content').innerHTML+='<h2>Admins for '+list[0].name+' are:</h2>';
      for(var i = 1; i < list.length; i++){
        var admin = list[i];
        document.getElementById('content').innerHTML+='<p align="center">'+admin.name+ '</p><br>';
      }
      $("*").css("cursor", "default");
    } else if(request.readyState==4){
      alert("something went wrong");
    }
  }
  var league_key_string = getParameterByName('league_key_string');
  request.open("GET", '/showAdmins?league_key_string='+league_key_string, true);
  request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  request.send("");
}

function addAdmins(){
  var request = new XMLHttpRequest();
  $("*").css("cursor", "progress");
  request.onreadystatechange=function(){
    if(request.readyState==4 && request.status==200){
      showAdmins();
    }
    $("*").css("cursor", "default");
  }
  var league_key_string = $("input#league_key_string").val();
  var email = $("input#admin_email").val();
  if(email == ""){
    alert('You need to enter an email!');
    $("*").css("cursor", "default");
    return;
  }
  request.open("POST",'/addAdmin', true);
  request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  request.send("league_key_string="+league_key_string+"&admin_email="+email);
}

function deleteAdminsShow(){
  var request = new XMLHttpRequest();
  $("*").css("cursor", "progress");
  request.onreadystatechange=function(){
    if(request.readyState==4 && request.status==200){
      jQuery(".active").toggleClass("active");
      jQuery(".manage").toggleClass("active");
      jQuery(".delAdminLink").toggleClass("active");
      var list = JSON.parse(request.responseText);
      document.getElementById('content').innerHTML="";
      document.getElementById('content').innerHTML+='<h2>Delete an Admin from '+list[0].name+"</h2>";
      document.getElementById('content').innerHTML+='<select class="form-control" id="admin_list" name="admin_email">';
      for(var i = 1; i < list.length; i++){
        var admin = list[i];
        document.getElementById('admin_list').innerHTML+='<option value="'+admin.name+'">'+admin.name+'</option>';
      }
      $("*").css("cursor", "default");
      document.getElementById('content').innerHTML+='<div id="buttonbar"><button class="button" onclick="deleteAdmin()">Delete</button></div>';
    } else if(request.readyState==4){
      alert('something went wrong'); 
    }
  }
  var league_key_string = getParameterByName('league_key_string');
  request.open("GET", '/deleteAdmin?league_key_string='+league_key_string, true);
  request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  request.send();
}

function deleteAdmin(){
  var request = new XMLHttpRequest();
  $("*").css("cursor", "progress");
  request.onreadystatechange=function(){
    if(request.readyState==4 && request.status==200){
      showAdmins();
      $("*").css("cursor", "default");
    }
  }
  var league_key_string = getParameterByName('league_key_string');
  request.open("POST", '/deleteAdmin', true);
  request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  request.send("league_key_string="+league_key_string+"&admin_email="+document.getElementById('admin_list').value);
}

function yourLeagues(){
  var request = new XMLHttpRequest();
  jQuery(".active").toggleClass("active")
  jQuery(".manage").toggleClass("active")
  jQuery(".yourLeagueLink").toggleClass("active")
  $("*").css("cursor", "progress");
  request.onreadystatechange=function(){
    if(request.readyState==4 && request.status==200){
      var leagues = JSON.parse(request.responseText);
      document.getElementById('content').innerHTML = "";
      document.getElementById('content').innerHTML += '<h2>Leagues you are a member of:</h2>';
      document.getElementById('content').innerHTML += '<form action="/switchLeagues" method="POST" id="league_member_form">';
      document.getElementById('league_member_form').innerHTML += '<select id="league_member_pick" name="league_pick" class="form-control">';
      for(var i = 0; i < leagues.league_member.length; i++){
        var league = leagues.league_member[i];
        //alert(league.name);
        document.getElementById('league_member_pick').innerHTML += '<option value="'+league.key+'">'+league.name+'</option>';
      }  
      document.getElementById('league_member_form').innerHTML += '</select><div id="buttonbar1" class="buttonbar">';
      document.getElementById('buttonbar1').innerHTML += '<button class="button" type="submit">Select League</button>';
      document.getElementById('league_member_form').innerHTML += '</div></form>';

      document.getElementById('content').innerHTML += '<h2>Leagues you are an admin of</h2>';
      document.getElementById('content').innerHTML += '<form action="/switchLeagues" method="POST" id="league_form">';
      document.getElementById('league_form').innerHTML += '<select id="league_pick" name="league_pick" class="form-control">';
      for(var i = 0; i < leagues.league_admin.length; i++){
        var league = leagues.league_admin[i];
        document.getElementById('league_pick').innerHTML +='<option value="'+league.key+'">'+league.name+'</option>';
      } 
      document.getElementById('league_form').innerHTML += '</select><div id="buttonbar">';
      document.getElementById('buttonbar').innerHTML += '<button class="button" type="submit">Select League</button>';
      document.getElementById('league_form').innerHTML += '</div></form>';
      $("*").css("cursor", "default");
    }
  }
  request.open("POST", '/showLeagues', true);
  request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  request.send("");    
}

function leagueInfo(){
  var request = new XMLHttpRequest();
  jQuery(".active").toggleClass("active")
  jQuery(".manage").toggleClass("active")
  jQuery(".leagueInfoLink").toggleClass("active")
  $("*").css("cursor", "progress");
  request.onreadystatechange=function(){
    if(request.readyState===4 && request.status==200){
      var members = JSON.parse(request.responseText);
      document.getElementById('content').innerHTML = "";
      document.getElementById('content').innerHTML += "<h2>"+members[0].league_name+"</h2>";
      document.getElementById('content').innerHTML += '<p align="center">Created on: '+members[0].date+'</p>';
      document.getElementById('content').innerHTML += "<h2>"+members[0].number+" members in the league</h2>";
      document.getElementById('content').innerHTML += "<h2>Members of this League</h2>"
      for(var i = 1; i < members.length; i++){
        var email = ((members[0].admin) ? " : " + members[i].email : "");
        document.getElementById('content').innerHTML += "<p align='center'>"+members[i].name+email+"</p>";
      }
      $("*").css("cursor", "default");
    }
  }
  var league_key_string = getParameterByName('league_key_string');
  request.open("POST", '/leagueInfo', true);
  request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  request.send("league_key_string="+league_key_string);
}  

function addMember(){
  var request = new XMLHttpRequest();
  $("*").css("cursor", "progress");
  request.onreadystatechange=function(){
    if(request.readyState==4 && request.status==200){
      leagueInfo();
      $("*").css("cursor", "default");
    }
  }
  var league_key_string = $('input#league_key_string').val()
  var memberName = $('input#memberName').val()
  var memberEmail = $('input#memberEmail').val()
  if(memberName == ""){
    alert('You need to enter a Member Name');
    $("*").css("cursor", "default");
    return;
  }
  if(memberEmail == ""){
    alert('You need to enter an Email');
    $("*").css("cursor", "default");
    return;
  }
  request.open("POST", '/addMember', true);
  request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  request.send("league_key_string="+league_key_string+"&memberName="+memberName+"&memberEmail="+memberEmail);
}

function deleteMemberShow(){
  var request = new XMLHttpRequest();
  $("*").css("cursor", "progress");
  request.onreadystatechange=function(){
    if(request.readyState==4 && request.status==200){
      jQuery(".active").toggleClass("active");
      jQuery(".manage").toggleClass("active");
      jQuery(".delMemberLink").toggleClass("active");
      var list = JSON.parse(request.responseText);
      document.getElementById('content').innerHTML="";
      document.getElementById('content').innerHTML+='<h2>Delete a Member</h2>';
      document.getElementById('content').innerHTML+='<select class="form-control" id="member_list" name="member_email">';
      for(var i = 0; i < list.length; i++){
        var member = list[i];
        document.getElementById('member_list').innerHTML+='<option value="'+member.key+'">'+member.name+'</option>';
      }
      document.getElementById('content').innerHTML+='<div id="buttonbar"><button class="button" onclick="deleteMember()">Delete</button></div>';
      $("*").css("cursor", "default");
    }
  }
  var league_key_string = getParameterByName('league_key_string');
  request.open("GET", '/deleteMember?league_key_string='+league_key_string, true);
  request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  request.send();
}
 
function deleteMember(){
  var request = new XMLHttpRequest();
  request.onreadystatechange=function(){
    if(request.readyState==4 && request.status==200){
      leagueInfo();
    }
  }
  var league_key_string = getParameterByName('league_key_string');
  request.open("POST", '/deleteMember', true);
  request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  request.send("league_key_string="+league_key_string+"&toDelete="+document.getElementById('member_list').value);
}

function showHistory(){
  var request = new XMLHttpRequest();
  jQuery(".active").toggleClass("active");
  jQuery(".manage").toggleClass("active");
  jQuery(".historyLink").toggleClass("active");
  $("*").css("cursor", "progress");
  document.getElementById('content').innerHTML = '<div class="panel panel-default" id="input">';
  document.getElementById('input').innerHTML = '<div id="playerAdiv" class="col-xs-4"></div>';
  document.getElementById('input').innerHTML += '<div id="score" class="col-xs-4"></div>';
  document.getElementById('input').innerHTML += '<div id="playerBdiv" class="col-xs-4"></div>';
  document.getElementById('playerAdiv').innerHTML = '<input class="form-control" id="playerA" name="playerA">';
  document.getElementById('score').innerHTML = '';
  document.getElementById('playerBdiv').innerHTML = '<input class="form-control" id="playerB" name="playerB"><br>';
  document.getElementById('input').innerHTML += '<div id="buttonbar"></div>';
  document.getElementById('buttonbar').innerHTML += '<button class="button" onclick=showHistoryPlayers()>Show History</button>';
  document.getElementById('content').innerHTML +='<div class="panel panel-default" id="historyTable"></div>'
  request.onreadystatechange=function(){
    if(request.readyState==4 && request.status==200){
      var historys = JSON.parse(request.responseText);
      drawHistoryTable(historys)
      document.getElementById('score').innerHTML = historys.league[0].wins + ' - ' + historys.league[0].losses;
      $("*").css("cursor", "default");  
    }
  }
  var league_key_string = getParameterByName('league_key_string');
  request.open("POST", '/history', true)
  request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  request.send("league_key_string="+league_key_string+"&playerA=&playerB="); 
}

function showHistoryPlayers(){
  var request = new XMLHttpRequest();
  $("*").css("cursor", "progress");
  request.onreadystatechange=function(){
    if(request.readyState==4 && request.status==200){
      var historys = JSON.parse(request.responseText);
      drawHistoryTable(historys)
      document.getElementById('score').innerHTML = historys.league[0].wins + ' - ' + historys.league[0].losses;
      $("*").css("cursor", "default");
    }
  }
  var league_key_string = getParameterByName('league_key_string');
  var playerA = document.getElementById('playerA').value;
  var playerB = document.getElementById('playerB').value;
  request.open("POST", '/history', true)
  request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  request.send("league_key_string="+league_key_string+"&playerA="+playerA+"&playerB="+playerB); 
}

function drawHistoryTable(historys){  
  var html = "";
  html += '<div class="panel-heading text-center"><strong>'+historys.league[0].name+'</strong></div>'
  html += '<table class="table rankTable">'
  html += '<thead>'
  html += '<tr>'
  html += '<th class="col-rank">Date</th>'+
          '<th class="col-Aname">Player One</th>'+
          '<th class="col-Ascore">Rank</th>'+
          '<th class="col-Bname">Player Two</th>'+
          '<th class="col-Bscore">Rank</th>'+
          '<th class="col-win">Winner</th>'+
          '</tr>'+
          '</thead>';
  if(historys.history.length <= 0){
    html += '</table>';
    html +='<p align="center">No History of Player Found</p>';
    html += '</div>';
    document.getElementById('historyTable').innerHTML = html;
    return
  }
  for(var i = 0; i < historys.history.length; i++){
    html += '<tr>'+
            '<td align="center">'+historys.history[i].date+'</td>'+
            '<td align="center">'+historys.history[i].playerA+'</td>'+
            '<td align="center">'+historys.history[i].playerA_rank+'</td>'+
            '<td align="center">'+historys.history[i].playerB+'</td>'+
            '<td align="center">'+historys.history[i].playerB_rank+'</td>'+
            '<td align="center">'+historys.history[i].winner+'</td>'+
            '</tr>'
  }
  html += '</table></div>';
  document.getElementById('historyTable').innerHTML = html;
}

/*rewrite JOSN style*/
function showTournament(){
  var request = new XMLHttpRequest();
  $("*").css("cursor", "progress");
  jQuery(".active").toggleClass("active");
  jQuery(".manage").toggleClass("active");
  jQuery(".tournamentLink").toggleClass("active");
  request.onreadystatechange=function(){
    var list = JSON.parse(request.responseText);
    document.getElementById('content').innerHTML = "";
    document.getElementById('content').innerHTML += '<h2>Tournaments in league: '+list[0].name+'</h2>';
    document.getElementById('content').innerHTML += '<div style="text-align: center;" id="links"></div>'
    var league_key = getParameterByName('league_key_string');
    if(list[0].admin){
      document.getElementById('links').innerHTML += '<a href="/tournament?league_key_string='+league_key+'">New Tournament</a><br>';
    }
    for(var i = 1; i < list.length; i++){
      document.getElementById('links').innerHTML += '<a href="/tournament?league_key_string='+list[i].key+'&bracket_url='+list[i].url+'">'+list[i].url+'</a><br>';
    }    
    $("*").css("cursor", "default");
  }
  var league_key_string = getParameterByName('league_key_string');
  request.open("POST", '/showTournament', true);
  request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  request.send("league_key_string="+league_key_string);
}

//When the page loads set content div to userInfo and mark userInfoLink to active
jQuery(document).ready(function() {
  event.preventDefault() 
    $("*").css("cursor", "progress");
    userInfo();
    $("*").css("cursor", "default");
});

//upload pic link
jQuery(document).ready(function() {
  jQuery(".uploadPicLink").click(function(event) {
    event.preventDefault() 
    jQuery(".active").toggleClass("active")
    jQuery(".manage").toggleClass("active")
    jQuery(".uploadPicLink").toggleClass("active")
    jQuery('#content').html(jQuery("#uploadPic").html()); 
  });
});

//create league
jQuery(document).ready(function() {
  jQuery(".createLeagueLink").click(function(event) {
    event.preventDefault() 
    jQuery(".active").toggleClass("active")
    jQuery(".manage").toggleClass("active")
    jQuery(".createLeagueLink").toggleClass("active")
    jQuery('#content').html(jQuery("#createLeague").html()); 
  });
});

//Add Member Link
jQuery(document).ready(function() {
  jQuery(".addMemberLink").click(function(event) {
    event.preventDefault() 
    jQuery(".active").toggleClass("active")
    jQuery(".manage").toggleClass("active")
    jQuery(".addMemberLink").toggleClass("active")
    jQuery('#content').html(jQuery("#addMember").html()); 
  });
});

//Add Admin Link
jQuery(document).ready(function() {
  jQuery(".addAdminLink").click(function(event) {
    event.preventDefault() 
    jQuery(".active").toggleClass("active")
    jQuery(".manage").toggleClass("active")
    jQuery(".addAdminLink").toggleClass("active")
    jQuery('#content').html(jQuery("#addAdmin").html()); 
  });
});

//Email Results Link
jQuery(document).ready(function() {
  jQuery(".emailResultsLink").click(function(event) {
    event.preventDefault() 
    jQuery(".active").toggleClass("active")
    jQuery(".manage").toggleClass("active")
    jQuery(".emailResultsLink").toggleClass("active")
    jQuery('#content').html(jQuery("#emailResults").html()); 
  });
});

//Reset Scores Link
jQuery(document).ready(function() {
  jQuery(".resetLink").click(function(event) {
    event.preventDefault() 
    jQuery(".active").toggleClass("active")
    jQuery(".manage").toggleClass("active")
    jQuery(".resetLink").toggleClass("active")
    jQuery('#content').html(jQuery("#resetScores").html()); 
  });
});

//Delete League Link
jQuery(document).ready(function() {
  jQuery(".deleteLeagueLink").click(function(event) {
    event.preventDefault() 
    jQuery(".active").toggleClass("active")
    jQuery(".manage").toggleClass("active")
    jQuery(".deleteLeagueLink").toggleClass("active")
    jQuery('#content').html(jQuery("#deleteLeague").html()); 
  });
});

function getParameterByName(name) {
    var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}