function createDynamicPieChart(data) {
    const ctx = document.getElementById(data.canvasId).getContext('2d');

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Burned Out', 'Overextended', 'Disengaged', 'Ineffective', 'Overextended and Disengaged', 'Overextended and Ineffective', 'Disengaged and Ineffective', 'Engaged'],
            datasets: [
                {
                    data: [data.profile1, data.profile2, data.profile3, data.profile4, data.profile5, data.profile6, data.profile7, data.profile8],
                    backgroundColor: ['#FA9189', '#FCAE7C', '#D1BDFF', '#E2CBF7', '#FFE699', '#B3F5BC', '#F9FFB5', '#D6F6FF'],
                },
            ],
        },
        options: {
            plugins: {
                legend: {
                    display: false,
                    position: 'right',
                },
                datalabels: {
                    display: true, // Display the data labels
                    color: 'black',
                    formatter: (value) => `${value}%`,
                },
            },
        },
    });
}

const colleges = [
    {
        canvasId: 'percentageChart1',
        profile1: 20,
        profile2: 15,
        profile3: 30,  // Replaced "engaged" with "profile3"
        profile4: 5,
        profile5: 10,
        profile6: 5,
        profile7: 5,
        profile8: 10
    },
    {
        canvasId: 'percentageChart2',
        profile1: 10,
        profile2: 25,
        profile3: 15,  // Replaced "engaged" with "profile3"
        profile4: 20,
        profile5: 10,
        profile6: 5,
        profile7: 5,
        profile8: 10
    },
    {
        canvasId: 'percentageChart3',
        profile1: 10,
        profile2: 25,
        profile3: 15,  // Replaced "engaged" with "profile3"
        profile4: 20,
        profile5: 10,
        profile6: 5,
        profile7: 5,
        profile8: 10
    },
    {
        canvasId: 'percentageChart4',
        profile1: 10,
        profile2: 25,
        profile3: 15,  // Replaced "engaged" with "profile3"
        profile4: 20,
        profile5: 10,
        profile6: 5,
        profile7: 5,
        profile8: 10
    },
    {
        canvasId: 'percentageChart5',
        profile1: 10,
        profile2: 25,
        profile3: 15,  // Replaced "engaged" with "profile3"
        profile4: 20,
        profile5: 10,
        profile6: 5,
        profile7: 5,
        profile8: 10
    },
    {
        canvasId: 'percentageChart6',
        profile1: 10,
        profile2: 25,
        profile3: 15,  // Replaced "engaged" with "profile3"
        profile4: 20,
        profile5: 10,
        profile6: 5,
        profile7: 5,
        profile8: 10
    },
    {
        canvasId: 'percentageChart7',
        profile1: 10,
        profile2: 25,
        profile3: 15,  // Replaced "engaged" with "profile3"
        profile4: 20,
        profile5: 10,
        profile6: 5,
        profile7: 5,
        profile8: 10
    },
    {
        canvasId: 'percentageChart8',
        profile1: 10,
        profile2: 25,
        profile3: 15,  // Replaced "engaged" with "profile3"
        profile4: 20,
        profile5: 10,
        profile6: 5,
        profile7: 5,
        profile8: 10
    },
];

// Create charts for each college
colleges.forEach(function (college) {
    createDynamicPieChart(college);
});