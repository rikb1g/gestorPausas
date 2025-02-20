


// pesquisa ajax

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
                    let listaResultados = $('#resultados');

                    if (resultados.length > 0) {
                        listaResultados.empty();
                        resultados.forEach(item => {
                            listaResultados.append('<li>' + item.interacao + '</li>');
                            listaResultados.append('<li>' + item.nome + '</li>');
                            listaResultados.append('<li>' + item.data + '</li>');
                            listaResultados.append('<li>' + item.nota + '</li>');
                        })}
                    else {
                        listaResultados.empty();
                    }
                }
            })
        }
        else {
            $('#resultados').empty();
        }
    })

});