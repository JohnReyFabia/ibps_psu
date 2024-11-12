document.addEventListener('DOMContentLoaded', function () {
  // Initial AJAX call to fetch keywords and counts
  $.ajax({
      url: '/get_keywords_and_counts/',  // Adjust the URL as needed
      type: 'GET',
      dataType: 'json',
      success: function (data) {
          console.log('Received data:', data);
          // Process the data and update the doughnut chart
          updateDoughnutChart(data);
      },
      error: function (error) {
          console.error('Error fetching keywords and scores:', error.responseText);
      }
  });
});

function updateDoughnutChart(data) {
  // Extract labels and counts from the received data
  const labels = Object.keys(data);
  const counts = Object.values(data);

  // Pastel colors array
  const pastelColors = [
      '#ffb6c1', '#ffcc66', '#98fb98', '#dda0dd', '#87ceeb',
      '#f08080', '#98fb98', '#f0e68c', '#afeeee', '#d2b48c',
      '#ff7f50', '#dda0dd', '#add8e6', '#ff6347', '#ff69b4'
  ];

  // Doughnut chart configuration
  const options = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
          legend: {
              display: false  // Set to false to hide the legend
          }
      }
  };

  // Example using Chart.js
  const ctx = document.getElementById('burnoutChart').getContext('2d');

  // Check if the chart is already created, destroy it before creating a new one
  if (window.myDoughnutChart) {
      window.myDoughnutChart.destroy();
  }

  window.myDoughnutChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
          labels: labels,
          datasets: [{
              data: counts,
              backgroundColor: pastelColors.slice(0, labels.length), // Use pastel colors
          }],
      },
      options: options  // Use the options defined above
  });
}
