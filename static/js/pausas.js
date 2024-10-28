

// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

// const csrftoken = getCookie('csrftoken');



document.addEventListener('DOMContentLoaded',function(){
    function atualizarTempoBO(){
        document.querySelectorAll('.tempo-decorrido-bo').forEach(function(element){
            const id = element.getAttribute('data-id');  
            fetch(`/backoffice/tempo_bo/${id}/`)
                .then(response => {
                    if (!response.ok){
                        throw new Error('Erro na requisição: ' + response.statusText);
                    }
                    return response.json();
                })
                .then(data => {
    
                    element.innerHTML = `<b>${data.calcular_tempo_bo_ao_segundo}</b>`;
                })
                .catch(error => {
                    element.textContent = "Erro ao carregar";
                });
        });
    }
    
    function atualizarTempoPausa(){
        document.querySelectorAll('.tempo-decorrido-pausa').forEach(function(element){
            const id = element.getAttribute('data-id'); 
            fetch(`/pausas/calcular_tempo_pausa/${id}/`)
                .then(response => {
                    if (!response.ok){
                        throw new Error('Erro na requisição: ' + response.statusText);
                    }
                    return response.json();
                })
                .then(data => {
    
                    element.innerHTML = `<b>${data.calcular_tempo_pausa_ao_segundo}</b>`;
                })
                .catch(error => {
                    console.error('Erro nas pausas ', error);
                    element.textContent = "Erro ao carregar";
                });
        });
    }

    // Atualiza o tempo de cada elemento a cada segundo
    setInterval(atualizarTempoBO, 1000);
    setInterval(atualizarTempoPausa,1000)
})







function pausarBO() {
    localStorage.removeItem('hora_retoma_bo')
    const timePause = localStorage.getItem('tempo_decorrido')
    localStorage.setItem('tempo_antes_pausa', timePause)
    localStorage.setItem('teve-pausa', false)

}

function retomarBOAposPausa() {
    const horaRetoma = new Date()
    localStorage.setItem('hora_retoma_bo', horaRetoma)
    localStorage.setItem('teve-pausa', true)
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

function iniciarBO() {
    alert("BO iniciado!")
    localStorage.removeItem('tempo_decorrido')
    localStorage.removeItem('hora_retoma_bo')
    localStorage.removeItem('tempo_antes_pausa')
}

function cancelarBO() {
    localStorage.removeItem()
    alert("O teu pedido de BO foi cancelado.")
}

function terminarBO() {
    alert("O teu BO foi terminado com sucesso. Bom atendimento")
    localStorage.removeItem('tempo_decorrido')
    localStorage.removeItem('hora_retoma_bo')
    localStorage.removeItem('tempo_antes_pausa')

}

let alertTriggered = false

function notifyUser(message) {
    const originalTitle = document.title;
    let isTitleModified = false

    const titleInterval = setInterval(function () {
        document.title = isTitleModified ? originalTitle : message
        isTitleModified = !isTitleModified
        console.log("funciona ")
    }, 1000)

    window.addEventListener("focus", function handleFocus() {
        if (!alertTriggered) {
            clearInterval(titleInterval)
            document.title = originalTitle
            alert(message)
            alertTriggered = true
            window.removeEventListener("focus", handleFocus)
        }

    })

    setTimeout(function () {
        if (!alertTriggered) {
            clearInterval(titleInterval);
            document.title = originalTitle;
            alert(message);
            alertTriggered = true;
        }
    }, 1000);
}