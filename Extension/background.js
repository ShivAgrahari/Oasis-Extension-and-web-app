chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
      if (request.action === 'checkURL') {
        // Send the URL to the Flask API
        fetch("http://127.0.0.1:9000//check", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ url: request.url }),
        })
          .then(response => response.json())
          .then(data => {
            sendResponse(data);
          })
          .catch(error => {
            console.error('Error:', error);
            sendResponse({ result: 'Error', prob: 0 });
          });
  
        return true; // Indicates that sendResponse will be called asynchronously
      }
    }
  );
  