
$(document).ready(function() {


fetch('/terminal')
  .then(
    function(response) {
      if (response.status !== 200) {
        console.log('Looks like there was a problem. Status Code: ' +
          response.status);
        return;
      }

      // Examine the text in the response
      response.json().then(function(data) {
        console.log(data);
        document.getElementById("textHolder").innerHTML = data;
      });
    }
  )
  .catch(function(err) {
    console.log('Fetch Error :-S', err);
  });
  });



setInterval(function() {
fetch('/terminal')
  .then(
    function(response) {
      if (response.status !== 200) {
        console.log('Looks like there was a problem. Status Code: ' +
          response.status);
        return;
      }

      // Examine the text in the response
      response.json().then(function(data) {
        console.log(data);
        document.getElementById("textHolder").innerHTML = data;
      });
    }
  )
  .catch(function(err) {
    console.log('Fetch Error :-S', err);
  });},  1000*1);

