window.chartColors = {
    red: 'rgb(255,120,149)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(23,100,235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};

var recession_data = [
    {

        "start": -391888800,
        "end": -370893600,
        "start_date": "1957-08-01",
        "end_date": "1958-04-01"
    },
    {
        "start": -307735200,
        "end": -281296800,
        "start_date": "1960-04-01",
        "end_date": "1961-02-01"
    },
    {
        "start": -2656800,
        "end": 26287200,
        "start_date": "1969-12-01",
        "end_date": "1970-11-01"
    },
    {
        "start": 120981600,
        "end": 162882000,
        "start_date": "1973-11-01",
        "end_date": "1975-03-01"
    },
    {
        "start": 315554400,
        "end": 331275600,
        "start_date": "1980-01-01",
        "end_date": "1980-07-01"
    },
    {
        "start": 362811600,
        "end": 404978400,
        "start_date": "1981-07-01",
        "end_date": "1982-11-01"
    },
    {
        "start": 646808400,
        "end": 667807200,
        "start_date": "1990-07-01",
        "end_date": "1991-03-01"
    },
    {
        "start": 983426400,
        "end": 1004594400,
        "start_date": "2001-03-01",
        "end_date": "2001-11-01"
    },
    {
        "start": 1196488800,
        "end": 1243832400,
        "start_date": "2007-12-01",
        "end_date": "2009-06-01"
    }
]

var timeFormat = 'YYYY-MM-DD';
var res;

var app = new Vue({
    el: '#app',
    data: {
        chart: null,
        loading: false
    },
    methods: {
        gets: function (name) {
            {
                this.loading = true
                axios.get("http://localhost:5000/graph", {
                    params: {
                        id: 'Fed_Funds'
                    }
                }).then(response => {
                        res = response.data
                        var ctx = document.getElementById('myChart');
                        var dates = res["Fed_Funds"][0].map(list => {
                            return moment(list, 'YYYY-MM-DD').toDate()
                        });
                        var value = res["Fed_Funds"][1]
                        var annotations = recession_data.map((date, index) => {
                            return {
                                type: 'box',
                                xScaleID: 'x-axis-0',
                                yScaleID: 'y-axis-0',
                                xMin: date.start_date,
                                xMax: date.end_date,
                                yMin: 0,
                                yMax: Math.max.apply(Math, value),
                                backgroundColor: 'rgba(101, 33, 171, 0.5)',
                                borderColor: 'rgb(101, 33, 171)',
                                borderWidth: 1,


                            }

                        });
                        this.chart = new Chart(ctx, f(dates, annotations, value));
                    }
                ).catch(error => {
                    console.log(error);
                    this.errored = true;
                }).finally(() => {
                    this.loading = false
                })
            }
        }
    },
    computed: {
        graph() {
            this.gets('Fed_Funds')
        }
    }
});

function f(arr, annotation, value) {
    var color = Chart.helpers.color;
    var config = {
        type: 'line',
        data: {
            labels: arr,
            datasets: [{
                label: 'Effect Fed Funds Rates',
                backgroundColor: color(window.chartColors.blue).alpha(0).rgbString(),
                borderColor: window.chartColors.blue,
                borderWidth: 1,
                fill: false,
                data: value,
            }]
        },
        options: {
            title: {
                text: 'Effect Fed Funds Rates'
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    time: {
                        format: timeFormat,
                        // round: 'day'
                        tooltipFormat: 'll '
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Date'
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Effect Fed Funds Rates'
                    }
                }]
            },
            annotation: {
                drawTime: 'afterDatasetsDraw',
                label: 'Recession Period',
                events: ['click'],
                annotations: annotation
            }
        }
    }
    return config
}



