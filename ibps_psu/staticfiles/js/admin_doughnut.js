document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById('keywordsDoughnutChart').getContext('2d');
  
    // Extract labels and data from the extractedKeywords object
    var labels = Object.keys(extractedKeywords);
    var data = Object.values(extractedKeywords);
  
    // Create the Doughnut Chart
    var doughnutChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: [
            '#ffb6c1', '#ffcc66', '#98fb98', '#dda0dd', '#87ceeb',
            '#f08080', '#98fb98', '#f0e68c', '#afeeee', '#d2b48c',
            '#ff7f50', '#dda0dd', '#add8e6', '#ff6347', '#ff69b4'
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false  // Set to false to hide the legend
            }
        }
      }
    });
  });
  