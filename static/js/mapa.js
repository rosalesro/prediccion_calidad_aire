// Inicialización del mapa
let mapa = L.map('mapa').setView([20, 0], 2);

// Fondo satelital de Esri
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles © Esri — Fuente de imagen: Esri, USGS',
    maxZoom: 19
}).addTo(mapa);

// Etiquetas con nombres
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Labels © Esri',
    maxZoom: 19
}).addTo(mapa);

let marcador = null;
let coordenadasSeleccionadas = null;

// Al hacer clic, colocamos marcador
mapa.on('click', e => {
    if (marcador) mapa.removeLayer(marcador);
    marcador = L.marker(e.latlng).addTo(mapa);
    coordenadasSeleccionadas = e.latlng;
});

// Al presionar el botón, llamamos a la API y pintamos resultados
document.getElementById('predecir').addEventListener('click', () => {
    if (!coordenadasSeleccionadas) {
        return alert('Por favor selecciona una ubicación en el mapa.');
    }

    fetch('/predecir_desde_mapa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            lat: coordenadasSeleccionadas.lat,
            lon: coordenadasSeleccionadas.lng
        })
    })
    .then(res => res.json())
    .then(data => {
        // Mostramos panel de resultados
        const panel = document.getElementById('resultado-prediccion');
        panel.style.display = 'flex';

        if (data.error) {
            document.getElementById('interpretacion').innerText = data.error;
            if (window.grafico) window.grafico.destroy();
            return;
        }

        // Posicionamos marcador en la barra AQI
        const porcentaje = Math.min(Math.max(data.resultado / 500 * 100, 0), 100);
        document.getElementById('marcador-aqi')
                .style.left = `calc(${porcentaje}% )`;

        // Calculamos interpretación localmente
        let textoCat;
        if (data.resultado < 51) textoCat = 'Buena (0–50)';
        else if (data.resultado < 101) textoCat = 'Moderada (51–100)';
        else if (data.resultado < 151) textoCat = 'Dañina para grupos sensibles (101–150)';
        else if (data.resultado < 201) textoCat = 'Dañina (151–200)';
        else if (data.resultado < 301) textoCat = 'Muy dañina (201–300)';
        else textoCat = 'Peligrosa (301–500)';

        // Pintamos interpretación + ubicación + AQI oficial
        document.getElementById('interpretacion').innerHTML = `
            Calidad del aire: <strong>${textoCat}</strong><br>
            📍 Ubicación: ${data.ciudad}, ${data.pais}<br>
            🧾 AQI oficial (IQAir): ${data.aqi_real}
        `;

        // Gráfico de contaminantes
        const etiquetas = Object.keys(data.contaminantes);
        const valores  = Object.values(data.contaminantes);
        const ctx = document.getElementById('graficoContaminantes').getContext('2d');
        if (window.grafico) window.grafico.destroy();
        window.grafico = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: etiquetas,
                datasets: [{
                    label: 'Concentración (μg/m³)',
                    data: valores,
                    borderWidth: 1
                }]
            },
            options: {
                scales: { y: { beginAtZero: true } }
            }
        });
    })
    .catch(err => {
        console.error('Error al enviar solicitud:', err);
        alert('Error al enviar solicitud.');
    });
});








