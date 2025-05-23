
$(document).ready(function() {
    $('#procurarInteracoes').on('keyup', function() {
        let query = $(this).val().trim();

        if (query.length > 1) {
            $.ajax({
                url: '/indicadores/pesquisar_interacoes/',
                data: {
                    'pesquisaInteracoes': query
                },
                dataType: 'json',
                success: function (data) {
                    let resultados = data.resultados;
                    let tabelaBody = $('.tableInteracoes tbody'); 

                    tabelaBody.empty();
                    
                    if (resultados.length > 0) {
                        
                        resultados.forEach(item => {
                            let corClasse = "";
                                    if (item.nota >= 9) {
                                        corClasse = "text-success"; // Verde
                                    } else if (item.nota >= 7) {
                                        corClasse = "text-warning"; // Amarelo
                                    } else {
                                        corClasse = "text-danger"; // Vermelho
                                    }
                            let row = `<tr>
                                <td>${item.interacao}</td>
                                <td>${item.funcionario}</td>
                                <td>${item.data}</td>
                                <td class="${corClasse}">${item.nota}</td>
                            </tr>`;
                            tabelaBody.append(row);
                        });
                    }
                    else {
                }
            },
            error: function () {
                console.error("Erro ao buscar interlocutores.");
            }
           
        });
        }
    });       

});