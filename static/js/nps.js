


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
                        tituloResultados.empty();
                        
                        
                        const table = listaResultados.append('<table>');
                        table.addClass('tableInterlocutores');
                        table.addClass('m-5')
                       
                        const thead = table.append('<thead>');
                        const tr = thead.append('<tr>');
                        tr.append('<th>Interação</th>');
                        tr.append('<th>Nome Assistente</th>');
                        tr.append('<th>Data</th>');
                        tr.append('<th>Nota</th>');
                        const tbody = table.append('<tbody>');
                        resultados.forEach(item => {
                            tbody.append('<td>' + item.interacao + '</td>');
                            tbody.append('<td>' + item.nome + '</td>');
                            tbody.append('<td>' + item.data + '</td>');
                            tbody.append('<td>' + item.nota + '</td>');
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