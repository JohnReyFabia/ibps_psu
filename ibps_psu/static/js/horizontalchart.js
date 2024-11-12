// Get the canvas element
var ctx = document.getElementById('horizontalMultiBarChart').getContext('2d');

// Sample data for the grouped multi-bar chart
var data = {
  labels: ['Label 1', 'Label 2', 'Label 3', 'Label 4', 'Label 5', 'Label 6', 'Label 7', 'Label 8'],
  datasets: [
    {
      label: 'Male',
      backgroundColor: 'rgba(255, 99, 132, 0.7)',
      data: [30, 40, 20, 50, 25, 35, 45, 30]
    },
    {
      label: 'Female',
      backgroundColor: 'rgba(54, 162, 235, 0.7)',
      data: [20, 30, 15, 40, 30, 25, 35, 20]
    },
  ]
};

// Grouped multi-bar chart configuration
var options = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: 'y',
  scales: {
    x: {
      stacked: false
    },
    y: {
      stacked: false
    }
  }
};

// Create the grouped multi-bar chart
var myhorizontalMultiBarChart = new Chart(ctx, {
  type: 'bar',
  data: data,
  options: options
});
