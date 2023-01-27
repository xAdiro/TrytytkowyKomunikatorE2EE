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
    let messageField = $("#message-field");
    // let publicKey = document.getElementById("publicKey");

    //send for me
    let toSend = encryptForMe(messageField.val())
    console.log(toSend);
    $.post("/send-message/", {
        "receiver": converser,
        "message": toSend,
        "used_key": cryptico.publicKeyString(currentKey)
    })

    //send for receiver


    messageField.val("")
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
