// contentScript.js

// Listen for messages from the Next.js frontend
window.addEventListener('message', (event) => {
  if (event.source !== window) return;

  if (event.data.action === 'getBookmarks') {
    // Send a message to the Chrome extension's background script
    chrome.runtime.sendMessage({ action: 'getBookmarks' }, (response) => {
      // Send the bookmarks back to the Next.js app
      window.postMessage(
        { action: 'bookmarksResponse', bookmarks: response.bookmarks },
        '*'
      );
    });
  }
});
