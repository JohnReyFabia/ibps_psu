// Assuming ageDataPerProfile is a global variable containing the age range data
document.addEventListener('DOMContentLoaded', function () {
  var ctx = document.getElementById('multiBarChart').getContext('2d');

  // Extract labels and data from the ageDataPerProfile object
  var labels = Object.keys(ageDataPerProfile);

  // Extract age range data for each burnout profile
  var ageRangeData = Object.values(ageDataPerProfile);

  // Create the grouped bar chart
  var myGroupedBarChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: '16-20',
          backgroundColor: '#4C7080',
          data: ageRangeData.map(profileData => profileData[0])
        },
        {
          label: '21-25',
          backgroundColor: '#BFD1D9',
          data: ageRangeData.map(profileData => profileData[1])
        },
        {
          label: '26-30',
          backgroundColor: 'rgba(255, 206, 86, 0.7)',
          data: ageRangeData.map(profileData => profileData[2])
        },
        {
          label: '31+',
          backgroundColor: 'rgba(75, 192, 192, 0.7)',
          data: ageRangeData.map(profileData => profileData[3])
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          stacked: false
        },
        y: {
          stacked: false
        }
      }
    }
  });
});
