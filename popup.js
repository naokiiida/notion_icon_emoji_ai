document.getElementById('buttonFlag1').addEventListener('click', function() {
	chrome.runtime.connect({ name: "popup" }).postMessage({ action: "runScriptWithFlag", flag: 1 });
  });

  document.getElementById('buttonFlag2').addEventListener('click', function() {
	chrome.runtime.connect({ name: "popup" }).postMessage({ action: "runScriptWithFlag", flag: 2 });
  });

