import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

const BACKEND_URL = 'http://localhost:8080';

function App() {
  const [urls, setUrls] = useState([]);
  const [errorMessage, setErrorMessage] = useState(null);

  const getBookmarksFromExtension = () => {
    if (typeof window !== 'undefined') {
      // Send a message to the content script to fetch bookmarks
      window.postMessage({ action: 'getBookmarks' }, '*');
    }
  };

  let fetch_urls = () => {
    getBookmarksFromExtension(); // Call the function to fetch bookmarks from the extension

    return fetch(`${BACKEND_URL}/extension/store_urls`, {
      method: 'POST', // Ensure the request is POST
      headers: {
        'Content-Type': 'application/json', // Set the request headers
      },
      body: JSON.stringify({
        urls,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        console.log('URLs successfully received from the Flask server:', data);
        return data; // Assuming the data is a list of URLs
      })
      .catch((error) => {
        console.error('Error retrieving URLs from the Flask server:', error);
        return []; // Return an empty list in case of an error
      });
  };

  useEffect(() => {
    fetch_urls().then((urls) => {
      setUrls(urls); // Set the fetched URLs into state
    });
  }, []); // Empty array ensures this runs once when component mounts

  useEffect(() => {
    const handleMessage = (event) => {
      if (event.data.action === 'bookmarksResponse') {
        if (event.data.bookmarks) {
          setUrls(event.data.bookmarks); // Keep updating state with received bookmarks
          console.log('Bookmarks retrieved:', event.data.bookmarks); // Log them for debugging
          setErrorMessage(null); // Clear error message if successful
        } else {
          setErrorMessage('Failed to retrieve bookmarks.');
        }
      }
    };

    window.addEventListener('message', handleMessage);

    return () => {
      window.removeEventListener('message', handleMessage);
    };
  }, []);

  return (
    <div className='App'>
      <header className='App-header'>
        <img src={logo} className='App-logo' alt='logo' />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className='App-link'
          href='https://reactjs.org'
          target='_blank'
          rel='noopener noreferrer'
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
