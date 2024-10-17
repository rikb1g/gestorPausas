function timeStringToSeconds(timeStr) {
    const [hours, minutes, seconds] = timeStr.split(':').map(Number);
    return hours * 3600 + minutes * 60 + seconds;
}

// Helper function to convert total seconds back to "HH:MM:SS" format
function secondsToTimeString(totalSeconds) {
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}
function resumeTimer(resumeTimer, displayElement){
    setInterval(function(){
        var now = new Date()
        var start = new Date(resumeTimer)
        var diff = now - start

        var hours = Math.floor(diff / (1000 * 60 * 60));
        var minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((diff % (1000 * 60)) / 1000);

        // Garante que horas, minutos e segundos sejam válidos
        hours = hours >= 0 ? hours : 0;
        minutes = minutes >= 0 ? minutes : 0;
        seconds = seconds >= 0 ? seconds : 0;

        // Formata o tempo decorrido
        var formattedTime = hours + ":" + (minutes < 10 ? "0" : "") + minutes + ":" + (seconds < 10 ? "0" : "") + seconds;

        totalSeconds1 = timeStringToSeconds(formattedTime)
        const pausaSeconds = localStorage.getItem('tempo_antes_pausa')
        totalSeconds2 = timeStringToSeconds(pausaSeconds)

        var totalSecundsSum = totalSeconds1 + totalSeconds2

        var resumeTimeStr = secondsToTimeString(totalSecundsSum)

        localStorage.setItem('tempo_decorrido', resumeTimeStr)
        displayElement.textContent = resumeTimeStr;



    }, 1000)
}
function startTimer(startTime, displayElement) {
    setInterval(function () {
        var now = new Date();
        var start = new Date(startTime);
        localStorage.setItem('star_timer',start)

        var diff = now -start

        
    
        

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
        localStorage.setItem('tempo_decorrido', formattedTime)

        // Atualiza o elemento HTML com o tempo decorrido
        displayElement.textContent = formattedTime;
    }, 1000); // Atualiza a cada segundo
}




// Exemplo de como iniciar o contador
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.tempo-decorrido').forEach(function (element) {
        var startTime = element.getAttribute('data-inicio');
        var timetopause = localStorage.getItem('tempo_antes_pausa')
        var retomaPAusa = localStorage.getItem('hora_retoma_bo');
        
        if (retomaPAusa){
            resumeTimer(retomaPAusa, element)
            
            

        }
       
        else if (startTime && !retomaPAusa) {

            startTimer(startTime,element);

        } else if (timetopause) {
            element.textContent = timetopause;
        } 
    });
});
 

function pausarBO() {
    localStorage.removeItem('hora_retoma_bo')
    const timePause = localStorage.getItem('tempo_decorrido')
    localStorage.setItem('tempo_antes_pausa', timePause)
    const hora = new Date()
    localStorage.setItem('hora_paragem', hora)
    

}

function retomarBOAposPausa(){  
    const horaRetoma = new Date()
    localStorage.setItem('hora_retoma_bo', horaRetoma)

}







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
    localStorage.removeItem('tempo_decorrido')
    localStorage.removeItem('hora_retoma_bo')
    localStorage.removeItem('tempo_antes_pausa')
}

function cancelarBO(){
    localStorage.removeItem()
    alert("O teu pedido de BO foi cancelado.")
}

function terminarBO(){
    alert("O teu BO foi terminado com sucesso. Bom atendimento")
    localStorage.removeItem('tempo_decorrido')
    localStorage.removeItem('hora_retoma_bo')
    localStorage.removeItem('tempo_antes_pausa')

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