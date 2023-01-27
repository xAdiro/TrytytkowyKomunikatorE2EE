var converser = null;
function selectChat(username, element){
    $("#chatbox").load("chatbox/?converser=" + username);
    $(".contact").removeClass("active_contact")
    element.classList.add("active_contact");
    converser = username;
    console.log("selected " + username);
}
