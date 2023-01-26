function acceptRequest(username){
    $.post("/accept-friend-request/", {
        "username": username
    })

    // let requestElement = $(".friend-request-name").filter(function() {return $(this).text() === username}).parent()
    // requestElement.remove()
}
