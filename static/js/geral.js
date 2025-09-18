let intervaloPausa = null;


function iniciarAtualizacaoPausa() {
    if (intervaloPausa) clearInterval(intervaloPausa);

    const elementos = document.querySelectorAll('.tempo-decorrido-pausa');
    if (elementos.length === 0) return; // não faz nada se não houver pausas

    intervaloPausa = setInterval(atualizarTempoPausa, 1000);
}

function pararAtualizacaoPausa() {
    if (intervaloPausa) {
        clearInterval(intervaloPausa)
        intervaloPausa = null
    }
}


document.addEventListener('DOMContentLoaded', function () {
    const tooggleBtn = document.getElementById("theme-toggle");
    const body = document.body;
    const togglerIcon = document.querySelector(".navbar-toggler-icon");

    // verificar a preferencia guardada
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        body.classList.add("dark-mode");
        tooggleBtn.textContent = "☀️ Claro"
       
        
    } else if (savedTheme === "light") {
        body.classList.remove("dark-mode");
        tooggleBtn.textContent = "🌙 Escuro"
      
            
    } else {
      if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
        body.classList.add("dark-mode");
        tooggleBtn.textContent = "☀️ Claro" 
      }
    }

    tooggleBtn.addEventListener("click", function() {
      console.log("clicou")
       
      if(body.classList.contains("dark-mode")){
            body.classList.remove("dark-mode");
            tooggleBtn.textContent = "🌙 Escuro"
            localStorage.setItem("theme", "light");
            window.location.reload();
            
      } else {
            body.classList.add("dark-mode");
            tooggleBtn.textContent = "☀️ Claro"
            localStorage.setItem("theme", "dark");
            window.location.reload();
      }
        
    });
    function atualizarTempoBO() {
        document.querySelectorAll('.tempo-decorrido-bo').forEach(function (element) {
            const id = element.getAttribute('data-id');
            fetch(`/backoffice/tempo_bo/${id}/`)
                .then(response => {
                    if (!response.ok) {
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
    atualizarSelectTurno();

    function atualizarTempoPausa() {
        document.querySelectorAll('.tempo-decorrido-pausa').forEach(function (element) {
            const id = element.getAttribute('data-id');

            if (!id) {
                console.warn("Ignorado: elemento sem data-id", element);
                return;
            }

            if (!id || id === "undefined") {
                console.warn("Ignorado: elemento sem data-id válido", element);
                return;
            }

            fetch(`/pausas/calcular_tempo_pausa/${id}/`)
                .then(r => r.json())
                .then(data => {
                    element.innerHTML = `<b>${data.calcular_tempo_pausa_ao_segundo}</b>`;
                })
                .catch(err => {
                    console.error('Erro nas pausas ', err);
                    element.textContent = "Erro ao carregar";
                });
        });
    }


    function atualizarPagina() {
        console.log('Atualizando a página...');
        fetch(window.locationHomePage, {
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na requisição: ' + response.statusText);
                }
                return response.text();
            })
            .then(data => {
                const content = document.getElementById("content-dynamic");

                // Criar um elemento temporário com o HTML novo
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = data;

                // Lista dos blocos que queremos comparar/atualizar
                const blocos = [
                    "box-pausa",
                    "box-backOffice",
                    "box-segunda-pausa",
                    "box-primeira-pausa",
                    "box-bo-manha",
                    "box-bo-tarde"
                ];

                blocos.forEach(id => {
                    const oldEl = content.querySelector(`#${id}`);
                    const newEl = tempDiv.querySelector(`#${id}`);

                    if (oldEl && newEl) {
                        const oldClean = oldEl.innerHTML.trim();
                        const newClean = newEl.innerHTML.trim();
                        if (oldClean !== newClean) {
                            // Só troca se realmente mudou
                            oldEl.innerHTML = newClean;
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Erro na requisição: ', error);
            });
        atualizarSelectTurno();
    }

    // Atualiza o tempo de cada elemento a cada segundo
    setInterval(atualizarTempoBO, 1000);
    setInterval(atualizarTempoPausa, 1000);
    setInterval(atualizarPagina, 10000);

})


function atualizarSelectTurno() {
    const filterTurno = document.getElementById("filterTurno");
    if (filterTurno) {
        fetch(`/usuarios/turno_funcionario/`)
            .then(r => r.json())
            .then(data => {
                filterTurno.value = data.turno === "manha" ? "True" : "False";
            })
            .catch(err => console.error("Erro ao buscar turno:", err));
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


function atualizarSelectMaximo() {
    const intervalos = document.getElementById('num-1')
    const intervalos2 = document.getElementById('num-2')
    const boManha = document.getElementById('num-bo')
    const boTarde = document.getElementById('num-bo-tarde')

    if (intervalos && intervalos2 && boManha && boTarde) {
        fetch(`/backoffice/maximos_autorizados/`)
            .then(response => response.json())
            .then(data => {
                intervalos.value = data.maximo_intervalos1,
                    intervalos2.value = data.maximo_intervalos2,
                    boManha.value = data.maximo_bo_manha,
                    boTarde.value = data.maximo_bo_tarde

            })
    }



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

window.addEventListener("scroll", function () {
    localStorage.setItem("scrollPosition", window.scrollY);
});


window.addEventListener('popstate', function (event) {
    this.location.reload();
})
$(document).on('click', '.link-ajax', function (e) {
    e.preventDefault();
    const url = $(this).attr('href');

    $.ajax({
        url: url,
        success: function (data) {
            // Atualiza o conteúdo dinâmico
            $('#content-dynamic').html(data);

            // Atualiza o URL do browser
            window.history.pushState(null, null, url);
        }
    });
});



const container = document.getElementById("content-dynamic");

const observer = new MutationObserver(() => {
    atualizarCores();
    atualizarSelectTurno();
});

observer.observe(container, { childList: true, subtree: true });

document.title = "Alto Valor";