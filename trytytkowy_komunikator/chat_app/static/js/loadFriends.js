var friends = -1;
$(() =>{
    loadFriends();
    friends = document.getElementsByClassName("contact-container").length;
})
function loadFriends(){
    console.log("loading friends");
    $("#contacts").load("contacts/");

    let currentFriends = document.getElementsByClassName("contact-container").length;
    if (currentFriends === friends) {
        setTimeout(loadFriends, 300);
    }
    else{
        friends = currentFriends;
    }
}
