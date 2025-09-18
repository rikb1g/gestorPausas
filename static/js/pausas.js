
function getCSRFToken() {
    // Acessa diretamente o cookie csrftoken
    const csrfToken = document.cookie
        .split(';')
        .map(cookie => cookie.trim())
        .find(cookie => cookie.startsWith('csrftoken='));

    // Se encontrado, extrai o valor
    return csrfToken ? csrfToken.split('=')[1] : null;
}


function carregarConteudo(url) {
    pararAtualizacaoPausa();
    fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(response => response.text())
        .then(html => {
            document.getElementById("content-dynamic").innerHTML = html;
        })
        .catch(error => console.error("Erro na requisição:", error));
    atualizarSelectTurno();
}   




// Desativar o botão "voltar" do navegador
window.history.pushState(null, "", window.location.href)
window.onpopstate = function () {
    window.history.pushState(null, "", window.location.href)
}



function pedirPausa(event){
    event.preventDefault()
    fetch('/pausas/pedir_pausa/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success){
            if(data.message === "Boa Pausa!!!"){
                notifyUser("✅ Pausa Aprovada!");
            }
            carregarConteudo(window.pausasList);
        }
        else {
            alert(data.message);
        }
    })
}

function pedirBO(event){
    event.preventDefault()
    var turno = document.getElementById('filterTurno').value
    fetch(`/backoffice/pedir_bo/?turno=${turno}`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success){
            if(data.message === "BackOffice Aprovado!!!"){
                notifyUser("✅ BackOffice Aprovado!!!");
            }
            carregarConteudo(window.pausasList);
        }
        else {
            alert(data.message);
        }
    })
}

function iniciarBo(event){
    event.preventDefault()
    fetch('/backoffice/iniciar_bo/',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success){
            carregarConteudo(window.pausasList);
        }
        else {
            alert(data.message);
        }
    })
}


function pausarBo(event, id, pausa){
    event.preventDefault()
    fetch(`/backoffice/pausar_bo/${id}/${pausa}/`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success){
            if (data.supervisor === true){
                carregarConteudo(window.locationHomePage);
            } else {
                carregarConteudo(window.pausasList);
            }
        }
        else {
            alert(data.message);
        }
    })
}

function retomarBo(event, id){
    event.preventDefault();
        fetch(`/backoffice/retomar_bo/${id}/`,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success){
                if (data.supervisor === true){
                    carregarConteudo(window.locationHomePage);
                }
                carregarConteudo(window.pausasList);
            }
            else {
                alert(data.message);
            }
        })
}


function exibirPopUpconfirmacaoInicioBO(event,id,nome){
    event.preventDefault();
    if (confirm("Tens a certeza que pretendes iniciar o BO de " + nome + " ?")) {
        var url = "/backoffice/iniciar_bo/?id=" + encodeURIComponent(id);
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success){
                carregarConteudo(window.locationHomePage);
            }
            else {
                alert(data.message);
            }
        })
    }
    else {
        alert("Ação cancelada")
    }
}

function exibirPopUpconfirmacaoEliBO(event,id, nome) {
    event.preventDefault();
    if (confirm("Tens a certeza que pretendes anular o BO de " + nome + " ?")) {
        var url = "/backoffice/cancelar_bo/?id=" + encodeURIComponent(id);
        console.log(url);
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success){
                carregarConteudo(window.locationHomePage);
            }
            else {
                alert(data.message);
            }
        })
    }
    else {
        alert("Ação cancelada")
    }
}

function exibirPopUpconfirmacaoPausarBO(event, id, nome, pausa) {
    event.preventDefault();
    if (confirm("Tens a certeza que pretendes pausar o BO de " + nome + " ?")) {
        var url = `/backoffice/pausar_bo/${id}/${pausa}/`;
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success){
                carregarConteudo(window.locationHomePage);
            }
            else {
                alert(data.message);
            }
        })
    }
}

function exibirPopUpconfirmacaoRetomarBO(event, id, nome) {
    event.preventDefault();
    if (confirm("Tens a certeza que pretendes retomar o BO de " + nome + " ?")) {
        var url = `/backoffice/retomar_bo/${id}/`;
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success){
                carregarConteudo(window.locationHomePage);
            }
            else {
                alert(data.message);
            }
        })
    }
}

function exibirPopUpconfirmacaoAutBO(event, id, nome) {
    event.preventDefault();
    if (confirm("Tens a certeza que pretendes autorizar o BO de " + nome + " ?")) {
        var url = "/backoffice/autorizar_bo/?id=" + encodeURIComponent(id);
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success){
                carregarConteudo(window.locationHomePage);
            }
            else {
                alert(data.message);
            }
        })
    }
}

function exibirPopUpConfirmacaoAutPausa(event, id, nome) {
    event.preventDefault();
    if (confirm("Tens a certeza que pretendes autorizar o intervalo de " +nome+ " ?")) {
        var url = "/pausas/autorizar_intervalo/?id="+encodeURIComponent(id);
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success){
                carregarConteudo(window.locationHomePage);
            }
            else {
                alert(data.message);
            }
        })
    }
}
function exibirPopUpConfirmacaoEliPAusa(event, id, nome) {
    event.preventDefault();
    console.log(id);
   if (confirm("Tens a certeza que pretendes anular o intervalo de " +nome+ " ?")) {
        var url = "/pausas/cancelar_intervalo/?id="+encodeURIComponent(id);
        console.log(url);
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
        if (data.success){
            alert(data.message);
            carregarConteudo(window.locationHomePage);
        }
        else {
            alert(data.message);
        }
    })
    }   
} 
    


function canelarIntervalo(event) {
    event.preventDefault();
    if (confirm("Tens a certeza que pretendes cancelar o teu intervalo ?")) {
        fetch('/pausas/cancelar_intervalo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
        if (data.success){
            alert(data.message);
            carregarConteudo(window.pausasList);
        }
        else {
            alert(data.message);
        }
    })
    }


}

function terminarIntervalo(event) {
    event.preventDefault();
    fetch('/pausas/finalizar_intervalo/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success){
            pararAtualizacaoPausa()
            carregarConteudo(window.pausasList);
        }
        else {
            alert(data.message);
        }
    })
}


function cancelarBO(event) {
    event.preventDefault();
    if(confirm("Tens a certeza que pretendes cancelar o teu pedido de BO ?")){
        fetch('/backoffice/cancelar_bo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success){
                alert(data.message);
                carregarConteudo(window.pausasList);
            }
            else {
                alert(data.message);
            }
        })
    }
}

function terminarBO(event) {
    event.preventDefault();
    fetch('/backoffice/finalizar_bo/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success){
            pararAtualizacaoPausa()
            carregarConteudo(window.pausasList);
        }
        else {
            alert(data.message);
        }
    })
}

let alertTriggered = false

function notifyUser(message) {
    const originalTitle = document.title;
    let isTitleModified = false

    const titleInterval = setInterval(function () {
        document.title = isTitleModified ? originalTitle : message
        isTitleModified = !isTitleModified
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


function iniciarIntervalo(event){
    event.preventDefault();
    console.log("iniciar intervalo");
   fetch('/pausas/iniciarIntervalo/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success){
            console.log(data.message);
            console.log(window.pausasList)
            carregarConteudo(window.pausasList);
        } else {
            console.warn(data.message);
        }
    })
    .catch(error => {
        console.error('Erro na requisição: ', error)
    })
    .finally(() => {
        document.body.classList.remove('loading'); // sempre remove
    });
}

 

document.addEventListener("submit", function (e) {
    if (e.target && e.target.matches("form[id^='form-filter']"))  {
        e.preventDefault();

        const form = e.target;
        const url = form.action;
        const formData = new FormData(form);

        fetch(url, {
        method: "POST",
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken(),
    }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            carregarConteudo(window.locationHomePage);
        } else {
            alert(data.message);
        }
    });
    }




});