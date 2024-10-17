
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


function setDarkMode(isBlack){
    localStorage.setItem('isBlack', isBlack)   


    if (isBlack === true){
        document.body.style.backgroundColor = "black"
        document.body.style.color = "white"
        document.getElementById("toogleback").innerHTML = "Lighmode"
    } else {
        document.body.style.backgroundColor = "white"
        document.body.style.color = "black"
        document.getElementById("toogleback").innerHTML = "Darkmode"
    }

}


function mudarcorfundo(){

    let isBlack = localStorage.getItem('isBlack') === 'true'

    setDarkMode(!isBlack)

    
}


function loadTheme(){
    let isBlack = localStorage.getItem('isBlack') === 'true'
    setDarkMode(isBlack)
}



loadTheme()
document.addEventListener("DOMContentLoaded", function(){
    /*
    var select_num = document.getElementById('num')
    var valor_selecionado_num = select_num.value
    var select_num_bo = document.getElementById('num-bo')
    var valor_salvo_num_bo = select_num_bo.value


    localStorage.setItem('select_num', valor_selecionado_num)
    localStorage.setItem('select_num_bo', valor_selecionado_num_bo)
        */
    history.pushState(null, null, '');
    window.onpopstate = function () {
        history.go(1);
    };
})
