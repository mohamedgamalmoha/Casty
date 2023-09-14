
function createChartContainer(chartID, title){
    var parent = document.createElement('div');
    parent.className = 'col-6';
    parent.style.maxHeight = '400px';
    parent.style.overFlow = 'auto';

    parent.style.paddingBottom = '40px';

    if (chartID != '1' || chartID != '2'){
        parent.style.paddingTop = '60px';
    }

    var span = document.createElement('span');
    span.className = 'text';
    span.appendChild(document.createTextNode(title));

    var canvas = document.createElement('canvas');
    canvas.id = chartID;

    parent.appendChild(span);
    parent.appendChild(canvas);

    return parent;
}

function createChart(ctx, type, title, labels, data){
    var chart = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: title,
                data: data,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

async function callAPI(url, token){
    try {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `JWT ${token}`
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();

    } catch (error) {
        console.error("Fetch error:", error);
        return undefined;
    }
}

async function displayChartContainer(url, token, parent, label, value, id, title, type){
    const data = await callAPI(url, token);

    var ctx = createChartContainer(id, title);
    parent.append(ctx);

    createChart(
        ctx.querySelector('canvas'),
        type,
        title,
        data.results.map(item => item[label]),
        data.results.map(item => item[value])
    );
}

window.onload = async () => {
    const parent = document.querySelector('.card-body > .row');
    const token = JSON.parse(document.getElementById('token').textContent);

    await displayChartContainer('/api/stats/users/daily-count/', token, parent, 'date', 'count', 1, 'Registered User Daily Count', 'line');
    await displayChartContainer('/api/stats/users/role-count/', token, parent, 'label', 'count', 2, 'Registered User Role Percentage', 'pie');

    await displayChartContainer('/api/stats/reports/daily-count/', token, parent, 'date', 'count', 3, 'Reports Daily Count', 'line');
    await displayChartContainer('/api/stats/reports/type-count/', token, parent, 'label', 'count', 4, 'Reports Type Percentage', 'pie');

    await displayChartContainer('/api/stats/rates/daily-count/', token, parent, 'date', 'count', 5, 'Rates Daily Count', 'line');
    await displayChartContainer('/api/stats/rates/daily-sum/', token, parent, 'date', 'sum', 6, 'Rates Daily Sum', 'line');
    await displayChartContainer('/api/stats/rates/rate-count/', token, parent, 'label', 'count', 7, 'Rates Percentage', 'pie');

    await displayChartContainer('/api/stats/contracts/daily-count/', token, parent, 'label', 'count', 8, 'Contracts Daily Count', 'line');
    await displayChartContainer('/api/stats/contracts/offer-sum/', token, parent, 'date', 'sum', 9, 'Contracts Offer Sum', 'line');

    await displayChartContainer('/api/stats/solo-contracts/daily-count/', token, parent, 'label', 'count', 8, 'Solo Contracts Daily Count', 'line');
    await displayChartContainer('/api/stats/solo-contracts/offer-sum/', token, parent, 'date', 'sum', 9, 'Solo Contracts Offer Sum', 'line');
}
