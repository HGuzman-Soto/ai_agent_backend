import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

const BACKEND_URL = 'http://localhost:8080';

function App() {
  const [urls, setUrls] = useState([]);

  let fetch_urls = () => {
    return fetch(`${BACKEND_URL}/extension/receive_urls`, {
      method: 'POST', // Ensure the request is POST
      headers: {
        'Content-Type': 'application/json', // Set the request headers
      },
      body: JSON.stringify({
        // Example data to send with the POST request
        param1: 'value1',
        param2: 'value2',
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
