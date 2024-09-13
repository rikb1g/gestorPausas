document.addEventListener("DOMContentLoaded", function(){
    
    var select_num = document.getElementById('num')
    var valor_selecionado_num = select_num.value

    localStorage.setItem('valor_selecionado_num', valor_selecionado_num)
})



function salvarVAlorSelecionado(){
    var select_num = document.getElementById('num')
    console.log(select_num)

    var valor_selecionado_num = select_num.value

    localStorage.setItem('valor_selecionado_num', valor_selecionado_num)
}


window.onload = function() {
    var valor_salvo_num = localStorage.getItem('valor_selecionado_num');
    if (valor_salvo_num) {
        var select_num = document.getElementById('num');
        select_num.value = valor_salvo_num; // Aplica o valor do localStorage ao select
    }
};


