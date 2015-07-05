function player_two_update(element){
  var current = document.getElementById("player_one");
  var value = current[current.selectedIndex].value; 
  var op = document.getElementById("player_two").getElementsByTagName("option");
  for (var i = 0; i < op.length; i++) {
    if (op[i].value.toLowerCase() == value) {
      op[i].disabled = true;
    }
    else {
      op[i].disabled = false;
    }
    
  }
  
  if (document.getElementById("player_two").getElementsByTagName("option").length > 1){
    document.getElementById("submitbtn").disabled = false; 
    document.getElementById("random").disabled = false; 
  }

}

function player_one_update(element){
  var current = document.getElementById("player_two");
  var value = current[current.selectedIndex].value; 
  var op = document.getElementById("player_one").getElementsByTagName("option");
  for (var i = 0; i < op.length; i++) {
    if (op[i].value.toLowerCase() == value) {
      op[i].disabled = true;
    }
    else {
      op[i].disabled = false;
    }
    
  }

}

function defaults(element){
  document.getElementById("player_one").selectedIndex = "0";
  document.getElementById("player_two").selectedIndex = "1";
  if (document.getElementById("player_two").getElementsByTagName("option").length < 2){
    document.getElementById("submitbtn").disabled = true; 
    document.getElementById("random").disabled = true; 
  }
    
  
}

function randomize(element){
  document.getElementById("submitbtn").disabled = true; 
  document.getElementById("random").disabled = true;

  var player_one = document.getElementById("player_one");
  var player_two = document.getElementById("player_two");
  var length = player_two.getElementsByTagName("option").length;
  var random = Math.floor((Math.random() * length));
  var random2 = Math.floor((Math.random() * length));
  var op1 = player_one.getElementsByTagName("option");
  var op2 = player_two.getElementsByTagName("option");
  
  
  while (op1[random].value == op2[random2].value || random > length-1 || random < 0 || random2 > length-1 || random2 < 0){
    random2 = Math.floor((Math.random() * length));
  }
   //alert(op1[random].value + "  " + op2[random2].value);

  //allow free use of option boxes
  for (var i = 0; i < length; i++) {
      player_one.getElementsByTagName("option")[i].disabled = false;
      player_two.getElementsByTagName("option")[i].disabled = false;
  }

  player_one.selectedIndex=random;
  player_two.selectedIndex=random2;
  
  document.forms["create"].submit();
}

function btnsubmit(element){
  document.getElementById("submitbtn").disabled = true; 
  document.getElementById("random").disabled = true;
  
  document.forms["create"].submit();
}