
function startTimer(startTime, displayElement) {
    setInterval(function () {
        var now = new Date();
        var start = new Date(startTime);
        var diff = now - start;  // diferença em milissegundos

        // Garante que a diferença é válida antes de continuar
        if (isNaN(diff)) {
            displayElement.textContent = "Erro na data";
            return;
        }

        // Converte a diferença em horas, minutos e segundos
        var hours = Math.floor(diff / (1000 * 60 * 60));
        var minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((diff % (1000 * 60)) / 1000);

        // Garante que horas, minutos e segundos sejam válidos
        hours = hours >= 0 ? hours : 0;
        minutes = minutes >= 0 ? minutes : 0;
        seconds = seconds >= 0 ? seconds : 0;

        // Formata o tempo decorrido
        var formattedTime = hours + ":" + (minutes < 10 ? "0" : "") + minutes + ":" + (seconds < 10 ? "0" : "") + seconds;

        // Atualiza o elemento HTML com o tempo decorrido
        displayElement.textContent = formattedTime;
    }, 1000); // Atualiza a cada segundo
}

// Exemplo de como iniciar o contador
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.tempo-decorrido').forEach(function (element) {
        const btnPause = document.getElementById('btn-pause');
        const btnResume = document.getElementById('btn-resume');
        var startTime = element.getAttribute('data-inicio');
        
       

        if (startTime) {
            startTimer(startTime, element);

        }
    });
});




// Desativar o botão "voltar" do navegador
window.history.pushState(null, "", window.location.href)
window.onpopstate = function () {
    window.history.pushState(null, "", window.location.href)
}
function terminarIntervalo() {
    alert("A tua pausa terminou")
}
function iniciarIntervalo() {
    alert("Boa pausa!!!")

}

function canelarIntervalo() {
    alert("Intervalo cancelado!")
}

function iniciarBO(){
    alert("BO iniciado!")
}

function cancelarBO(){
    alert("O teu pedido de BO foi cancelado.")
}

function terminarBO(){
    alert("O teu BO foi terminado com sucesso. Bom atendimento")
}

let alertTriggered = false

function notifyUser(message){
    const originalTitle = document.title;
    let isTitleModified = false

    const titleInterval = setInterval(function(){
        document.title = isTitleModified ? originalTitle : message
        isTitleModified = !isTitleModified
        console.log("funciona ")
    }, 1000)

    window.addEventListener("focus", function handleFocus(){
        if (!alertTriggered) {
            clearInterval(titleInterval)
            document.title = originalTitle
            alert(message)
            alertTriggered = true
            window.removeEventListener("focus", handleFocus)
        }

    })

    setTimeout(function() {
        if (!alertTriggered) {
            clearInterval(titleInterval);
            document.title = originalTitle;
            alert(message);
            alertTriggered = true;
        }
    }, 1000);
}