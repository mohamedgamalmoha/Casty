
function createChartContainer(chartID, title){
    var parent = document.createElement('div');
    parent.className = 'col-6';

    var span = document.createElement('span');
    span.className = 'text';
    span.appendChild(document.createTextNode(title));

    var canvas = document.createElement('canvas');
    canvas.id = chartID;

    parent.appendChild(span);
    parent.appendChild(canvas);

    return parent;
}

function createChart(ctx, title, labels, data){
    var chart = new Chart(ctx, {
        type: 'pie',  // or bar, pie, etc.
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

window.onload = () => {
    var parent = document.querySelector('.card-body > .row');
    for (let i = 0; i < 5; i++) {
        var labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'];
        var data = [12, 19, 3, 5, 2, 3];
        var ctx = createChartContainer(i, 'Chat');
        parent.appendChild(ctx);
        createChart(ctx.querySelector('canvas'), 'Chart', labels, data);
    }
}
