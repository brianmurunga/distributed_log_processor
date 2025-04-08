function renderChart(logLevels, logCounts) {
    const ctx = document.getElementById('logChart').getContext('2d');
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: logLevels,
        datasets: [{
          label: "Count",
          data: logCounts,
          backgroundColor: "rgba(54, 162, 235, 0.6)",
          borderColor: "rgba(54, 162, 235, 1)",
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  }
  
  function validateDates() {
    const start = document.getElementById('start_date').value;
    const end = document.getElementById('end_date').value;
    if (start && end && start > end) {
      alert("End date must be after start date");
      document.getElementById('end_date').value = "";
    }
  }
  