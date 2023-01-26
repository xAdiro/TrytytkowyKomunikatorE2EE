$(generateRSAPair)
function generateRSAPair() {
    const bits = 512;

    const array = new Uint32Array(1);
    let passPhrase = window.crypto.getRandomValues(array)[0] + Date.now();
    var RSAKey = cryptico.generateRSAKey(passPhrase, )
}
