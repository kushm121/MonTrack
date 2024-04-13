const sideLinks = document.querySelectorAll('.sidebar .side-menu li a:not(.logout)');

sideLinks.forEach(item => {
    const li = item.parentElement;
    item.addEventListener('click', () => {
        sideLinks.forEach(i => {
            i.parentElement.classList.remove('active');
        })
        li.classList.add('active');
    })
});

const menuBar = document.querySelector('.content nav .bx.bx-menu');
const sideBar = document.querySelector('.sidebar');

menuBar.addEventListener('click', () => {
    sideBar.classList.toggle('close');
});

const searchBtn = document.querySelector('.content nav form .form-input button');
const searchBtnIcon = document.querySelector('.content nav form .form-input button .bx');
const searchForm = document.querySelector('.content nav form');

searchBtn.addEventListener('click', function (e) {
    if (window.innerWidth < 576) {
        e.preventDefault;
        searchForm.classList.toggle('show');
        if (searchForm.classList.contains('show')) {
            searchBtnIcon.classList.replace('bx-search', 'bx-x');
        } else {
            searchBtnIcon.classList.replace('bx-x', 'bx-search');
        }
    }
});

window.addEventListener('resize', () => {
    if (window.innerWidth < 768) {
        sideBar.classList.add('close');
    } else {
        sideBar.classList.remove('close');
    }
    if (window.innerWidth > 576) {
        searchBtnIcon.classList.replace('bx-x', 'bx-search');
        searchForm.classList.remove('show');
    }
});

const toggler = document.getElementById('theme-toggle');

toggler.addEventListener('change', function () {
    if (this.checked) {
        document.body.classList.add('dark');

    } else {
        document.body.classList.remove('dark');
    }
    initCharts(contextData);
});
// Function to initialize the charts
function initCharts(contextData) {
    var isDark = document.body.classList.contains('dark');
    var labelColor = isDark ? '#fff' : '#000'; // Define label color based on theme
    ApexCharts.exec('bar-chart', 'destroy');
    ApexCharts.exec('pie-chart', 'destroy');
    var optionsArea = {
        chart: {
            id: 'bar-chart',
            height: 380,
            type: 'area',
            stacked: false,
            foreColor: isDark ? '#fff' : '#000',
        },
        stroke: {
            curve: 'straight'
        },
        series: [{
            name: "Expenses",
            data: contextData.exp2
        },
        {
            name: "Income",
            data: contextData.exp3
        }
        ],
        xaxis: {
            categories: contextData.month,
        },

        tooltip: {
            followCursor: true
        },
        fill: {
            opacity: 1,
        },
    };


    var chartArea = new ApexCharts(document.querySelector("#bar-chart"), optionsArea);
    chartArea.render();
    var colorPalette = ['#00D8B6','#008FFB',  '#FEB019', '#FF4560', '#775DD0'];
    var optionDonut = {
        chart: {
            id: 'pie-chart',
            type: 'pie',
            width: '100%',
            height: 400,
            foreColor: isDark ? '#fff' : '#000',
        },
        dataLabels: {
            enabled: false,
        },
        plotOptions: {
            pie: {
                customScale: 0.8,
                donut: {
                    size: '75%',
                },
                offsetY: 20,
            },
            stroke: {
                colors: undefined
            }
        },
        colors: colorPalette,
        title: {
            style: {
                fontSize: '18px',
                // color: labelColor
            }
        },
        series: contextData.exp,
        labels: contextData.category,
        legend: {
            position: 'left',
            offsetY: 80,
            colorPalette: colorPalette
        },
    };
    var donut = new ApexCharts(document.querySelector("#pie-chart"), optionDonut);
    donut.render();



     var optionsHeatmap = {
        series: [
            {
                name: "Expenses",
                data: contextData.exp2
            },
            {
                name: "Income",
                data: contextData.exp3
            }
        ],
        chart: {
            id: 'heatmap-chart',
            height: 450,
            type: 'heatmap',
            theme : {
                mode: isDark ? 'dark' : 'light'
            },
            foreColor: isDark ? '#fff' : '#000',
            colorScale: {
          ranges: [{
              from: -30,
              to: 5,
              color: '#00A100',
              name: 'low',
            },
            {
              from: 6,
              to: 20,
              color: '#128FD9',
              name: 'medium',
            },
            {
              from: 21,
              to: 45,
              color: '#FFB200',
              name: 'high',
            }
          ]
        }

        },
        dataLabels: {
            enabled: false
        },
        // colors: colorPalette,
        xaxis: {
            type: 'category',
            categories: contextData.month,
        },
        grid: {
            padding: {
                right: 20
            }
        },
    };

    var chartHeatmap = new ApexCharts(document.querySelector("#heatmap-chart"), optionsHeatmap);
    chartHeatmap.render();


     var optionsRadialBar = {
        series: contextData.data_per,
        chart: {
            id: 'radial-bar-chart',
            height: 350,
            type: 'radialBar',
            foreColor: isDark ? '#fff' : '#000'
        },
        plotOptions: {
            radialBar: {
                dataLabels: {
                    name: {
                        fontSize: '22px',
                    },
                    value: {
                        fontSize: '16px',
                    },
                    total: {
                        show: true,
                        label: 'Total',
                    },
                }
            }
        },
        labels: contextData.category,
    };

    var chartRadialBar = new ApexCharts(document.querySelector("#radial-bar-chart"), optionsRadialBar);
    chartRadialBar.render();
}




