
function getCSRFToken() {
    // Acessa diretamente o cookie csrftoken
    const csrfToken = document.cookie
        .split(';')
        .map(cookie => cookie.trim())
        .find(cookie => cookie.startsWith('csrftoken='));

    // Se encontrado, extrai o valor
    return csrfToken ? csrfToken.split('=')[1] : null;
}


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




// Desativar o botão "voltar" do navegador
window.history.pushState(null, "", window.location.href)
window.onpopstate = function () {
    window.history.pushState(null, "", window.location.href)
}

const intervaloFomrElement = document.getElementById('intervaloForm')

if (intervaloFomrElement) {
    intervaloFomrElement.addEventListener('submit', function(event) {
        event.preventDefault();
        document.body.classList.add('loading');
        fetch('/pausas/iniciarIntervalo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert("Erro: " + data.error);
            } else {
                alert(data.message);
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Erro na requisição:', error);
        });
        document.body.classList.remove('loading');
    });

}

const boFormElement = document.getElementById('boForm')

if (boFormElement){
    boFormElement.addEventListener('submit', function(event){
        event.preventDefault();
        document.body.classList.add('loading');
        fetch('/backoffice/iniciar_bo/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            }
        })
        .then(response => {
            if (!response.ok){
                throw new Error(`Erro ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error){
                alert("Erro: "+ data.error)
            }else {
                alert(data.message);
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Erro na requisição: ', error)
        })
        document.body.classList.remove('loading');
    
    
    })
    

}


function canelarIntervalo() {
    if (confirm("Tens a certeza que pretendes cancelar o teu intervalo ?")) {
        fetch('/pausas/cancelar_intervalo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            }
        })
        .then(response => {
            if (!response.ok){
                throw new Error(`Erro ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error){
                alert("Erro: "+ data.error)
            }else {
                alert(data.message);
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Erro na requisição: ',error)
        })

    }else {

        alert("Ação cancelada")}


}

function terminarIntervalo() {
    alert("A tua pausa terminou")
}


function cancelarBO() {
    if(confirm("Tens a certeza que pretendes cancelar o teu pedido de BO ?")){
        fetch('/backoffice/cancelar_bo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            }
        })
        .then(response => {
            if (!response.ok){
                throw new Error(`Erro ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error){
                alert("Erro: "+ data.error)
            }else {
                alert(data.message);
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Erro na requisição: ',error)
        })

    }else {
        alert("Ação cancelada")
    }

}

function terminarBO() {
    alert("O teu BO foi terminado com sucesso. Bom atendimento")
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


const filterTurno = document.getElementById('filterTurno')

if (filterTurno){
    fetch(`/usuarios/turno_funcionario/`)
    .then(response => response.json())
    .then(data => {
        const turnoFuncionario = data.turno;
        console.log(turnoFuncionario)
        const select = document.getElementById('filterTurno');
        if (turnoFuncionario === 'manha') {
            select.value = 'True';
        }else {
            select.value = 'False';
        }
    })
        
}

function pedirBO() {
    turno = document.getElementById('filterTurno').value
    fetch(`/backoffice/pedir_bo/?turno=${turno}`,{
        method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            }
    })
    .then(response =>{
        if(!response.ok){
            throw new Error(`Erro ${response.status}: ${response.statusText}`);
        }
        return response.json()

    })
    .then(data => {
        if (data.error){
            alert("Erro: "+ data.error)
        }else {
            alert(data.message);
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Erro na requisição: ',error)
    })

}