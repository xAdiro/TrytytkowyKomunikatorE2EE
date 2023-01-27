function deleteFriend(contact){
    $.post("/delete-friend/", {
        "friend_username": contact
    });
}
