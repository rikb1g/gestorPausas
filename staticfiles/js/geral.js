
function salvarVAlorSelecionado(){ 
    var select_num = document.getElementById('num')
    
    console.log(select_num.value)
    var valor_selecionado_num = select_num.value

    localStorage.setItem('valor_selecionado_num', valor_selecionado_num)
}
function salvarVAlorSelecionadoBO(){
    var select_num = document.getElementById('num-bo')
    
    console.log(select_num.value)
    var valor_selecionado_num_bo = select_num.value

    localStorage.setItem('valor_selecionado_num_bo', valor_selecionado_num_bo)
}


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
function exibirPopUpconfirmacaoPausarBO(nome){
    if(confirm("Tens a certeza que pretendes pausar o BO de "+nome+ " ?")){
        var url = "/backoffice/pausar_bo_sup?nome="+encodeURIComponent(nome);
        window.location.href = url
    }
    else{
        alert("Ação cancelada")
    }

}

function exibirPopUpconfirmacaoRetomarBO(nome){
    if(confirm("Tens a certeza que pretendes retomar o BO de "+nome+ " ?")){
        var url = "/backoffice/despausar_bo_sup?nome="+encodeURIComponent(nome);
        window.location.href = url
    }
    else{
        alert("Ação cancelada")
    }
}


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
    history.pushState(null, null, '');
    window.onpopstate = function () {
        history.go(1);
    };
    document.querySelectorAll('.tempo-decorrido').forEach(function (element) {
        var startTime = element.getAttribute('data-inicio');
        if (startTime) {
            startTimer(startTime, element);
        }
    });
});
