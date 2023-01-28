$(function (){
    const seconds = 2;
    setInterval(() => {refreshChat();refreshFriendRequests();}, seconds*1000);
});
function refreshChat(){
    if(converser===null){
        return;
    }
    $("#chatbox").load("chatbox/?converser=" + converser,
        function (){
            const elements = document.querySelectorAll(".message-content");
            Array.from(elements).forEach((e, i) => {
                e.innerHTML = cryptico.decrypt(e.innerHTML, currentKey)["plaintext"];
            })
            converserPubKey = $("#converser-pub-key").text()
    });
    // console.log("chat refreshed");
}

function refreshFriendRequests(){
    $("#friend-request-container").load("friend-requests/");
}
