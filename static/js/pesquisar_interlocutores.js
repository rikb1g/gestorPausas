function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$(document).on('click', '.edit-btn',function () {

        let row = $(this).closest('tr');
        let at = row.find('.at').text();
        let destinatarios = row.find('.destinatarios').text().trim();
        let cc = row.find('.cc').text().trim();

        row.find('.at').html(`<input type="text" class="edit-at" value="${at}">`);
        row.find('.destinatarios').html(`<input type="text" class="edit-destinatarios" value="${destinatarios}">`);
        row.find('.cc').html(`<input type="text" class="edit-cc" value="${cc}">`);

        row.find('.edit-btn').hide();
        row.find('.save-btn').show();
        row.find('.remove-btn').hide();
    })
    $('.save-btn').on('click', function (e) {
        e.preventDefault();

        let row = $(this).closest('tr');
        let id = row.attr('data-id');
        let at = row.find('.edit-at').val().trim();
        let destinatarios = row.find('.edit-destinatarios').val().trim();
        let cc = row.find('.edit-cc').val().trim();

        $.ajax({
            url: '/indicadores/editar_interlocutores/',
            method: 'POST',

            data: {
                'id': id,
                'at': at,
                'destinatarios': destinatarios,
                'cc': cc,
                'csrfmiddlewaretoken': getCookie('csrftoken'),
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    row.find('.at').text(at);
                    row.find('.destinatarios').text(destinatarios);
                    row.find('.cc').text(cc);

                    row.find('.edit-btn').show();
                    row.find('.save-btn').hide();
                    row.find('.remove-btn').show();
                }
            }
        })
    })


window.addEventListener("beforeunload", function () {
    localStorage.setItem("scrollPosition", window.scrollY);
});


window.addEventListener("load", function () {
    const scrollPosition = localStorage.getItem("scrollPosition");
    if (scrollPosition) {
        window.scrollTo(0, scrollPosition);
    }
});

function eliminarInterlocutores(id, at) {
    if (confirm("Tem certeza de que deseja eliminar a AT " + at + " ?")) {
        window.location.href = '/indicadores/eliminar_interlocutores/' + encodeURIComponent(id) + "/";
    }
}


function atualizarTabela(resultados) {
    let tabelaBody = $('.tableInterlocutores tbody');
    tabelaBody.empty();

    if (resultados.length > 0) {
        resultados.forEach(item => {
            let row = `<tr>
                <td>${item.at}</td>
                <td>${item.destinatarios}</td>
                <td>${item.cc !== 'nan' ? item.cc : ''}</td>
            </tr>`;
            tabelaBody.append(row);
        });
    }
}

let tabelaOriginalInterlocutores = $('.tableInterlocutores tbody').html();

$(document).on('keyup', '#procurarInterlocutores', function () {
    let query = $(this).val().trim();
    let supervisor = $(this).data('supervisor') === 'True';

    if (query.length > 1) {
        $.ajax({
            url: '/indicadores/pesquisar_interlocutores/',
            data: {
                'pesquisar_at': query
            },
            dataType: 'json',
            success: function (data) {
                atualizarTabela(data.resultados);
            },
            error: function () {
                console.error("Erro ao buscar interlocutores.");
            }
        });
    } else if (query.length === 0) {
         $('.tableInterlocutores tbody').html(tabelaOriginalInterlocutores);
    }

});
