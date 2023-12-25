document.addEventListener('DOMContentLoaded', function () {
  // Function to send URL to Flask API
  const sendUrlToAPI = (url) => {
    chrome.runtime.sendMessage({ action: 'checkURL', url: url }, function (response) {
      var result = document.getElementById('result');
      result.innerHTML = 'Result: ' + response.result + ' with confidence ' + response.prob + '%';
    });
  };

  // Get the current active tab
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    var url = tabs[0].url;

    // Populate the input field with the URL
    var urlInput = document.getElementById('urlInput');
    urlInput.value = url;

    // Send the URL to the Flask API immediately
    sendUrlToAPI(url);
  });
});
