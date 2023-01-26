$(generateRSAPair)
function generateRSAPair() {
    const bits = 512;

    const array = new Uint32Array(1);
    let passPhrase = window.crypto.getRandomValues(array)[0] + Date.now();
    var RSAKey = cryptico.generateRSAKey(passPhrase, bits);
}

function encryptForMe(text) {
    return cryptico.encrypt(text, RSAKey)
}

function encryptForSomeone(text, RSAKeyString){
    return cryptico.encrypt(text, RSAKeyString)
}
