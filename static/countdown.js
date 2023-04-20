function countdown() {
  // Bind the timer display to the update function
  // via the clock variable and set start at 60
  var clock = document.querySelector('.clock');
  var time = 10;

  function updateClock() {
      // Call to the time flask endpoint
      fetch('/time')
          // Retrieve the number and display it
          .then(response => response.json())
          .then(data => {
              time = data.time;
              clock.textContent = time;
              // At 0 trigger sound function and resets
              if (time == 0) {
                  checkPeople();
                  clearInterval(interval);
                  // countdown();
              }
          });
  }

  updateClock();
  // Call the updateinterval every second
  var interval = setInterval(updateClock, 1000);
}

countdown();