var converser = null;
var converserPubKey = null;
function selectChat(username, element){
    $("#chatbox").load("chatbox/?converser=" + username,
        function (){
            $(".contact").removeClass("active_contact")
            element.classList.add("active_contact");
            converser = username;
            converserPubKey = $("#converser-pub-key").text()
            // console.log("selected " + username);

            const elements = document.querySelectorAll(".message-content");
            Array.from(elements).forEach((e, i) => {
                e.innerHTML = cryptico.decrypt(e.innerHTML, currentKey)["plaintext"];
            });

            $("#chatbox").addClass("active-chatbox");
    });
}
