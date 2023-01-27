function deleteFriend(contact){
    $.post("/delete-friend/", {
        "username": contact
    });
}