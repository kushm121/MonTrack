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
        },
        stroke: {
            curve: 'straight'
        },
        series: [{
            name: "Music",
            data: contextData.expenses
        }],
        xaxis: {
            categories: contextData.days,
            labels: {
                style: {
                    colors: labelColor
                }
            }
        },
        yaxis: {
            labels: {
                style: {
                    colors: labelColor
                }
            }
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
            type: 'donut',
            width: '100%',
            height: 400,
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
        series: contextData.data,
        labels: contextData.labels,
        legend: {
            position: 'left',
            offsetY: 80,
            colorPalette: colorPalette
        },
    };
    var donut = new ApexCharts(document.querySelector("#pie-chart"), optionDonut);
    donut.render();

}

// Call the initialize function to start everything
// initCharts(contextData);


// Function to initialize the charts

// var isDark = document.body.classList.contains('dark');
// var labelColor = isdark ? '#fff' : '#000';
// var colorPalette = ['#00D8B6','#008FFB',  '#FEB019', '#FF4560', '#775DD0'];

// var optionsArea = {
//     chart: {
//         height: 380,
//         type: 'area',
//         stacked: false,
//     },
//     stroke: {
//         curve: 'straight'
//     },
//     series: [{
//         name: "Music",
//         data: [11, 15, 26, 20, 33, 27, 56]
//     }],
//     xaxis: {
//         categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
//         labels: {
//             style: {
//                 colors: labelColor
//             }
//         }
//     },
//     yaxis: {
//         labels: {
//             style: {
//                 colors: labelColor
//             }
//         }
//     },
//     tooltip: {
//         followCursor: true
//     },
//     fill: {
//         opacity: 1,
//     },
// };


// var chartArea = new ApexCharts(document.querySelector("#bar-chart"), optionsArea);
// chartArea.render();

// var optionDonut = {
//     chart: {
//         type: 'donut',
//         width: '100%',
//         height: 400,
//     },
//     dataLabels: {
//         enabled: false,
//     },
//     plotOptions: {
//         pie: {
//             customScale: 0.8,
//             donut: {
//                 size: '75%',
//             },
//             offsetY: 20,
//         },
//         stroke: {
//             colors: undefined
//         }
//     },
//     colors: colorPalette,
//     title: {
//         style: {
//             fontSize: '18px',
//             // color: labelColor
//         }
//     },
//     series: [21, 23, 19, 14, 6],
//     labels: ['Clothing', 'Food Products', 'Electronics', 'Kitchen Utility', 'Gardening'],
//     legend: {
//         position: 'left',
//         offsetY: 80,
//     },
// };

// var donut = new ApexCharts(document.querySelector("#pie-chart"), optionDonut);
// donut.render();




  //   var labelcolor = isdark ? '#181a1e': '#fbfbfb';
  //   var optionsArea = {
  //     chart: {
  //       height: 380,
  //       type: 'area',
  //       stacked: false,
  //     },
  //     stroke: {
  //       curve: 'straight'
  //     },
  //     series: [{
  //         name: "Music",
  //         data: [11, 15, 26, 20, 33, 27,56]
  //       },
  //     ],
  //     xaxis: {
  //       categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
  //       labels: {
  //         style: {
  //           colors: labelcolor
  //         }
  //       }
  //     },
  //     yaxis: {
  //       labels: {
  //         style: {
  //           colors: labelcolor
  //         }
  //       }
  //     },
  //     tooltip: {
  //       followCursor: true
  //     },
  //     fill: {
  //       opacity: 1,
  //     },

  //   }

  //   var chartArea = new ApexCharts(
  //     document.querySelector("#bar-chart"),
  //     optionsArea
  //   );

  //   chartArea.render();

  // var colorPalette = ['#00D8B6','#008FFB',  '#FEB019', '#FF4560', '#775DD0']
  // var optionDonut = {
  //     chart: {
  //         type: 'donut',
  //         width: '100%',
  //         height: 400
  //     },
  //     dataLabels: {
  //       enabled: false,
  //     },
  //     plotOptions: {
  //       pie: {
  //         customScale: 0.8,
  //         donut: {
  //           size: '75%',
  //         },
  //         offsetY: 20,
  //       },
  //       stroke: {
  //         colors: undefined
  //       }
  //     },
  //     colors: colorPalette,
  //     title: {
  //       style: {
  //         fontSize: '18px',
  //         color: labelcolor
  //       }
  //     },
  //     series: [21, 23, 19, 14, 6],
  //     labels: ['Clothing', 'Food Products', 'Electronics', 'Kitchen Utility', 'Gardening'],
  //     legend: {
  //       position: 'left',
  //       offsetY: 80,
  //     },
  //   }

  //   var donut = new ApexCharts(document.querySelector("#pie-chart"),optionDonut)
  //   donut.render();

const transactionDateElements = document.querySelectorAll('.transaction-date');

transactionDateElements.forEach((element) => {
    const transactionDate = new Date(element.textContent);
    element.textContent = transactionDate.toLocaleString('en-US', {
        weekday: 'short',
        day: '2-digit',
        month: 'short',
        hour: 'numeric',
        minute: 'numeric',
        hour12: true,
    });
});



