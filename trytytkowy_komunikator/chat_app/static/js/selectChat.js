function selectChat(username, element){
    $("#chatbox").load("chatbox/?converser=" + username);
    $(".contact").removeClass("active_contact")
    element.classList.add("active_contact");
}
