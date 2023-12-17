chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'updateDetected') {
    // Handle the update notification in the content script
    alert('Notion update detected!');
  }
});
