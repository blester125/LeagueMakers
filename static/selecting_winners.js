function select(element){
  if(element.className.indexOf("selected") >= 0){
    element.className = element.className.replace("selected", "");
    var round = element.className.charAt(12);
    document.getElementById("round"+round+"winner").value="";
    document.getElementById("round"+round+"loser").value="";
    document.getElementById("rounds_entered").value=document.getElementById("rounds_entered").value.replace(round+"-","")
  } 
  else{
    var round = element.className.charAt(12);
    var roundClass = "round" + round;
    var classSearch = roundClass + " selected";
    if(document.getElementsByClassName(classSearch).length > 0){
      alert("You can only select one winner of each Match Up");
      return;
    }
    element.className += " selected";
    var winnerId = "round" + round + "winner";
    var loserId = "round" + round + "loser";
    var player_letter = 'A';
    if(element.id.indexOf("A") >= 0){
      player_letter = 'B';
    }
    var other_button = "round" + round +" player"+player_letter+"_button";
    document.getElementById(winnerId).value=element.getAttribute("name");
    document.getElementById(loserId).value=document.getElementById(other_button).getAttribute("name");
    document.getElementById("rounds_entered").value=document.getElementById("rounds_entered").value + round+"-";
  }
}