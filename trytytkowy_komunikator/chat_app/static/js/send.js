$(function () {
    $("#message-field")
})

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        }
    }
});

function sendMessage(){
    if(event.key !== 'Enter') return;

    if(converser === null){
        return;
    }
    let messageField = $("#message-field");

    //send for receiver
    let mess = encryptForSomeone(messageField.val(), converserPubKey);
    // console.log(mess);
    $.post("/send-message/", {
        "receiver": converser,
        "message": mess,
        "used_key": converserPubKey
    });


    //send for me
    $.post("/send-message/", {
        "receiver": converser,
        "message": encryptForMe(messageField.val()),
        "used_key": cryptico.publicKeyString(currentKey)
    }, refreshChat);

    messageField.val("");
}

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

