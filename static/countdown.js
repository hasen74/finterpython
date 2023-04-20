function countdown() {
  // Bind the timer display to the update function
  // via the clock variable
  var clock = document.querySelector('.clock');

  // Timer triggers distanciation check
  function CountdownTimer() {
    let countdown = 10;
  
    let intervalId = setInterval(() => {
      if (countdown > 0) {
        countdown -= 1;
        clock.textContent = countdown;
      } else {
        clearInterval(intervalId);
        intervalId = CountdownTimer();
        checkPeople();
      }
    }, 1000);
  
    return intervalId;
  }

  // Launch timer
  intervalId = CountdownTimer();
}

countdown();