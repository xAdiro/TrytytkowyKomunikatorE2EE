var currentKey = null;
$(generateRSAPair)
function generateRSAPair() {
    const bits = 512;

    const array = new Uint32Array(1);
    let passPhrase = window.crypto.getRandomValues(array)[0] + Date.now();
    currentKey = cryptico.generateRSAKey(passPhrase.toString(), bits);

    $.post("/update-pub-key/",{
        "key": cryptico.publicKeyString(currentKey)
    })
}

function encryptForMe(text) {
    return cryptico.encrypt(text, cryptico.publicKeyString(currentKey))["cipher"];
}

function encryptForSomeone(text, RSAString){
    let mess = cryptico.encrypt(text, RSAString);
    // console.log("sending" + mess["cipher"]);
    return mess["cipher"];
}

function decrypt(text){
    return cryptico.decrypt(text, currentKey);
}
