
function procurarInteracoesSelect(event) {
    event.preventDefault();
    let utilizador = $('#utilizador-select').val();
    let nota = $('#filtro-note').val();

    console.log(utilizador);
    console.log(nota);
    


}

function atualizarTabelaInteracoes(resultados){
            let tabelaBody = $('.tableInteracoes tbody'); 
            tabelaBody.empty();
                
                if (resultados.length > 0) {
                    resultados.forEach(item => {
                        let corClasse = "";
                        if (item.nota >= 9) {
                            corClasse = "text-success";
                        } else if (item.nota >= 7) {
                            corClasse = "text-warning";
                        } else {
                            corClasse = "text-danger";
                        }
                        let row = `
                            <tr>
                                <td>${item.interacao}</td>
                                <td>${item.funcionario}</td>
                                <td>${item.data}</td>
                                <td class="${corClasse}">${item.nota}</td>
                            </tr>`;
                        tabelaBody.append(row);
                    });
                }
            }


let tabelaOriginal = $('.tableInteracoes tbody').html();

$(document).on('keyup', '#procurarInteracoes', function() {
    let query = $(this).val().trim();
    console.log(query);
    console.log("asadss")

    if (query.length > 1) {
        $.ajax({
            url: '/indicadores/pesquisar_interacoes/',
            data: { 'pesquisaInteracoes': query },
            dataType: 'json',
            success: function (data) {
            atualizarTabelaInteracoes(data.resultados);
            },
                
            error: function () {
                console.error("Erro ao buscar interações.");
            }
        });
    } else if (query.length === 0) {
        $('.tableInteracoes tbody').html(tabelaOriginal)
    }
});
