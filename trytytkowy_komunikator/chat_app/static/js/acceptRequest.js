function acceptRequest(username){
    $.post("/accept-friend-request/", {
        "username": username
    },
        () =>{
        loadFriends();
    })

    // let requestElement = $(".contact").filter(function() {return $(this).text() === username}).parent()
    // requestElement.remove()

    let requestElements = document.getElementsByClassName("fiend-request-item");

    for(let i=0;i<requestElements.length;i++){
        if (requestElements[i].textContent === username){
            requestElements[i].parentElement.remove();
            return;
        }
    }
}
