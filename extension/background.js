// Listen for messages from the frontend
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getBookmarks') {
    console.log('Message received from frontend, fetching bookmarks...');
    chrome.bookmarks.getTree(function (bookmarkTreeNodes) {
      const learningBookmarks = extractLearningBookmarks(bookmarkTreeNodes);
      sendResponse({ bookmarks: learningBookmarks });
    });
    return true; // Keeps the message channel open for async response
  }
});

// Function to extract bookmarks from the "Learning" folder
function extractLearningBookmarks(bookmarks) {
  const learningBookmarks = [];

  function traverseBookmarks(bookmarks) {
    bookmarks.forEach((bookmark) => {
      if (bookmark.title === 'Learning' && bookmark.children) {
        bookmark.children.forEach((child) => {
          if (child.url) {
            learningBookmarks.push({ title: child.title, url: child.url });
          }
        });
      } else if (bookmark.children) {
        traverseBookmarks(bookmark.children);
      }
    });
  }

  traverseBookmarks(bookmarks);
  return learningBookmarks;
}

// Send the URLs to the backend
function sendURLsToBackend(urls) {
  fetch('http://localhost:8080/api/receive_urls', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ urls }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log('URLs successfully sent to the Flask server:', data);
    })
    .catch((error) => {
      console.error('Error sending URLs to the Flask server:', error);
    });
}
