
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



function exibirPopUpConfirmacaoEliPAusa(nome){
    if(confirm("Tens a certeza que pretendes anular o intervalo de " +nome+ " ?")){
        var url = "/pausas/cancelar_intervalo_sup?nome="+encodeURIComponent(nome);
        window.location.href = url
    }
    else {
        alert("Ação cancelada")
    }
}

function exibirPopUpConfirmacaoAutPausa(nome){
    if(confirm("Tens a certeza que pretendes autorizar o intervalo de " +nome+ " ?")){
        var url = "/pausas/autorizar_intervalo_sup?nome="+encodeURIComponent(nome);
        window.location.href = url
    }
    else {
        alert("Ação cancelada")
    }
}

function exibirPopUpconfirmacaoEliBO(nome){
    if(confirm("Tens a certeza que pretendes anular o BO de "+nome+ " ?")){
        var url = "/backoffice/cancelar_bo_supervisor?nome="+encodeURIComponent(nome);
        window.location.href = url
    }
    else {
        alert("Ação cancelada")
    }
}

function exibirPopUpconfirmacaoInicioBO(nome){
    if(confirm("Tens a certeza que pretendes iniciar o BO de "+nome+ " ?")){
        var url = "/backoffice/iniciar_bo_supervisor?nome="+encodeURIComponent(nome);
        window.location.href = url
    }
    else{
        alert("Ação cancelada")
    }
}
function exibirPopUpconfirmacaoAutBO(nome){
    if(confirm("Tens a certeza que pretendes autorizar o BO de "+nome+ " ?")){
        var url = "/backoffice/autorizar_bo_supervisor?nome="+encodeURIComponent(nome);
        window.location.href = url
    }
    else{
        alert("Ação cancelada")
    }
}

function exibirPopUpconfirmacaoRetomarBO(id,nome){
    if(confirm("Tens a certeza que pretendes retomar o BO de "+nome+ " ?")){
        var url = "/backoffice/despausar_bo_sup?id="+encodeURIComponent(id);
        window.location.href = url
    }
    else{
        alert("Ação cancelada")
    }
}


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


function atualizarSelectMaximo(){
    const intervalos = document.getElementById('num-1')
    const intervalos2 = document.getElementById('num-2')
    const boManha = document.getElementById('num-bo')
    const  boTarde= document.getElementById('num-bo-tarde')

    fetch(`/backoffice/maximos_autorizados/`)
    .then(response => response.json())
    .then(data => {
        intervalos.value= data.maximo_intervalos1,
        intervalos2.value = data.maximo_intervalos2,
        boManha.value =data.maximo_bo_manha,
        boTarde.value = data.maximo_bo_tarde
        
    })

}

atualizarSelectMaximo()

window.addEventListener("beforeunload", function () {
    localStorage.setItem("scrollPosition", window.scrollY);
});


window.addEventListener("load", function () {
    const scrollPosition = localStorage.getItem("scrollPosition");
    if (scrollPosition) {
        window.scrollTo(0, scrollPosition);
    }
});