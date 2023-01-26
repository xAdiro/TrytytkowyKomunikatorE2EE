function addFriend(){
    if(event.key !== 'Enter') return;

    let friendField = $("#add-contact-input");
    $.post("/add-friend/", {
        "username": friendField.val()
    })

    friendField.val("");
}
