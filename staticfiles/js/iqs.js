function submeterIqsFO(event, iqs) {
    event.preventDefault();
    fetch('/iqs/novo_iqs_fo/?iqs=' + iqs, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            carregarConteudo(window.pausasList);
            
        } else {
            alert(data.message);
        }
    });
}

function novoIqsFO(event,iqs, dia) {
    event.preventDefault();
    fetch('/iqs/novo_iqs_fo/?dia=' + encodeURIComponent(dia) + '&iqs=' + encodeURIComponent(iqs), {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            carregarConteudo(window.taxasList);
            
        } else {
            alert(data.message);
        }
    });
}

function novoIqsBO(event,iqs,dia) {
    event.preventDefault();
    fetch('/iqs/novo_iqs_bo/?dia=' + encodeURIComponent(dia) + '&iqs=' + encodeURIComponent(iqs), {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            carregarConteudo(window.taxasList);
            
        } else {
            alert(data.message);
        }
    });
}

function eliminarIqsBO(event,iqs,dia){
    event.preventDefault();
    fetch('/iqs/anular_iqs_bo/?dia=' + encodeURIComponent(dia) + '&iqs=' + encodeURIComponent(iqs), {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            carregarConteudo(window.taxasList);
            
        } else {
            alert(data.message);
        }
    });
}

function anularIQSFO(event, iqs,dia){
    event.preventDefault();
    fetch('/iqs/anular_iqs_fo/?dia=' + encodeURIComponent(dia) + '&iqs=' + encodeURIComponent(iqs), {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            carregarConteudo(window.taxasList);
            
        } else {
            alert(data.message);
        }
    });
}


function anularIqsFO(event, iqs) {
    event.preventDefault();
    fetch('/iqs/anular_iqs_fo/?iqs=' + iqs, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            carregarConteudo(window.pausasList);
           
            
        } else {
            alert(data.message);
        }
    });
}


function submeterIqsBO(event, iqs) {
    event.preventDefault();
    fetch('/iqs/novo_iqs_bo/?iqs=' + iqs, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            carregarConteudo(window.pausasList);
            
        } else {
            alert(data.message);
        }
    });
}

function anularIqsBO(event, iqs) {
    event.preventDefault();
    fetch('/iqs/anular_iqs_bo/?iqs=' + iqs, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            carregarConteudo(window.pausasList);
            
        } else {
            alert(data.message);
        }
    });
}

function atualizarCores() {
  let totalDiaTransferido = document.getElementById("total-dia-transferido");
  let totalDiaNaoTransferido = document.getElementById("total-dia-nao-transferido");
  let taxaDiaFo = document.getElementById("taxa-dia-fo");
  let iqsFaltaMes = document.getElementById("iqs-falta-mes");
  let taxaMesFo = document.getElementById("taxa-mes-fo");
  let taxaRespostaGeral = document.getElementById("taxa-resposta-geral");
  let totalDiaTransferidoBO = document.getElementById("total-dia-transferido-bo")
  let taxaMesBO = document.getElementById("taxa-mes-bo")
  let totalDiaNaoTransferidoBo = document.getElementById("total-dia-nao-transferido-bo")
  let taxaRespostaBo = document.getElementById("taxa-resposta-geral-bo")
  let iqsFaltaMesBo = document.getElementById("iqs-falta-mes-bo")
  let taxaDiaBo = document.getElementById("taxa-dia-bo")


  if (totalDiaTransferidoBO) {
    let valor = parseInt(totalDiaTransferidoBO.textContent) || 0;
    totalDiaTransferidoBO.style.color = valor > 0 ? "green" : "gray";
  }

  if (totalDiaNaoTransferidoBo) {
    let valor = parseInt(totalDiaNaoTransferidoBo.textContent) || 0;
    totalDiaNaoTransferidoBo.style.color = valor > 0 ? "red" : "gray";
  }

  if (taxaDiaBo) {
    let valor = parseFloat(taxaDiaBo.textContent) || 0;
    taxaDiaBo.style.color = valor >= 40 ? "green" : "red";
  }

  if (iqsFaltaMesBo) {
    let valor = parseInt(iqsFaltaMesBo.textContent) || 0;
    iqsFaltaMesBo.style.color = valor >= 0 ? "red" : "green";
  }

  if (taxaMesBO) {
    let valor = parseFloat(taxaMesBO.textContent) || 0;
    taxaMesBO.style.color = valor >= 40 ? "green" : "red";
  }

  if (taxaRespostaBo) {
    let valor = parseFloat(taxaRespostaBo.textContent) || 0;
    taxaRespostaBo.style.color = valor >= 60 ? "green" : "red";
  }



  if (totalDiaTransferido) {
    let valor = parseInt(totalDiaTransferido.textContent) || 0;
    totalDiaTransferido.style.color = valor > 0 ? "green" : "gray";
  }

  if (totalDiaNaoTransferido) {
    let valor = parseInt(totalDiaNaoTransferido.textContent) || 0;
    totalDiaNaoTransferido.style.color = valor > 0 ? "red" : "gray";
}

if (taxaDiaFo) {
    let valor = parseFloat(taxaDiaFo.textContent) || 0;
    taxaDiaFo.style.color = valor >= 80 ? "green" : "red";
}

if (iqsFaltaMes) {
    let valor = parseInt(iqsFaltaMes.textContent) || 0;
    iqsFaltaMes.style.color = valor >= 0 ? "green" : "red";
}

if (taxaMesFo) {
    let valor = parseFloat(taxaMesFo.textContent) || 0;
    taxaMesFo.style.color = valor >= 80 ? "green" : "red";
}

if (taxaRespostaGeral) {
    let valor = parseFloat(taxaRespostaGeral.textContent) || 0;
    taxaRespostaGeral.style.color = valor >= 60 ? "green" : "red";
}


}
document.addEventListener("DOMContentLoaded", atualizarCores);

// Observer para reagir a mudanças no texto
["total-dia-transferido", "total-dia-nao-transferido"].forEach(id => {
  let target = document.getElementById(id);
  if (target) {
    const observer = new MutationObserver(() => atualizarCores());
    observer.observe(target, { childList: true, characterData: true, subtree: true });
  }
});
