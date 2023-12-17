chrome.browserAction.onClicked.addListener(function(tab) {
	// Default behavior when clicking the browser action button
	// You can choose to implement this or leave it empty
	console.log("Default behavior");
  });
  
  document.getElementById('buttonFlag1').addEventListener('click', function() {
	runScriptWithFlag(1);
  });
  
  document.getElementById('buttonFlag2').addEventListener('click', function() {
	runScriptWithFlag(2);
  });
  
  function runScriptWithFlag(flag) {
	// Make an HTTP request to the Python server with the specified flag
	fetch(`http://localhost:5000/run-script?flag=${flag}`)
	  .then(response => response.text())
	  .then(result => {
		console.log(result);
	  })
	  .catch(error => {
		console.error(error);
	  });
  }
  