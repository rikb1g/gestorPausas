function renderNpsTable(data) {
    let tbody = $('#nps-table tbody');
    tbody.empty(); // apaga linhas antigas

    for (let mes in data.nps_por_mes) {
        let row = `
            <tr>
                <th>${data.meses[mes]}</th>
                <td>${data.promotores_mes[mes]}</td>
                <td>${data.neutros_mes[mes]}</td>
                <td>${data.detratores_mes[mes]}</td>
                <td>${data.nps_por_mes[mes]}</td>
            </tr>
        `;
        tbody.append(row);
    }
}

let chartInstance = null;

function initCharts(data) {
    const labels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];

    if (chartInstance) {
        chartInstance.destroy();
    }
    // Exemplo para Assistente
    const ctx = document.getElementById('npsChart').getContext('2d');

    chartInstance = new Chart(ctx, {
    type: "bar",
    data: {
        labels: labels,
        datasets: [
            { 
                label: "NPS Individual", 
                data: Object.values(data.nps_por_mes).map(v => Number(v) || 0),
                backgroundColor: "rgba(54, 162, 235, 0.2)", 
                borderColor: "rgba(54, 162, 235, 1)", 
                borderWidth: 1 
            },
            { 
                label: "NPS Global", 
                data: Object.values(data.nps_global_por_mes || {}).map(v => Number(v) || 0),
                backgroundColor: "rgba(255, 99, 132, 0.2)", 
                borderColor: "rgba(255, 99, 132, 1)", 
                borderWidth: 1 
            },
            { 
                label: "NPS Equipa", 
                data: Object.values(data.nps_equipa_por_mes || {}).map(v => Number(v) || 0),
                backgroundColor: "rgba(75, 192, 192, 0.2)", 
                borderColor: "rgba(75, 192, 192, 1)", 
                borderWidth: 1 
            }
        ]
    },
    options: {
        responsive: false,
        maintainAspectRatio: false,
        scales: { y: { beginAtZero: true, max: 100 } }
    }
});
}

function alternarNpsFilter(el){
    let userId = $(el).val();
        let url = new URL(window.NPSJsonUrl, window.location.origin);
        url.searchParams.set('utilizador', userId); 
        
        fetch(url, {
            headers: {
                'X-CSRFToken': getCSRFToken(),
            }
        })
        .then(response => response.json())
        .then(data => {
            renderNpsTable(data);
            initCharts(data);
        })
        .catch(error => console.error("Erro na requisição:", error));
}


function initNpsPage() {
    let npsTable = document.getElementById('nps-table');
    if (npsTable) {
        let userId = npsTable.dataset.userId;
        fetch(`${window.NPSJsonUrl}?utilizador=${userId}`, {
            headers: {
                'X-CSRFToken': getCSRFToken(),
            }
        })
            .then(response => response.json())
            .then(data => {
                renderNpsTable(data);
                initCharts(data);
            })
            .catch(error => console.error("Erro na requisição:", error));
    }
}

$(document).ready(function () {
    initNpsPage();
});


