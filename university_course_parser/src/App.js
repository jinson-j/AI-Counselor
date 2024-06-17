import React from 'react';
import './App.css'; // Importing main stylesheet
import TextField from '@mui/material/TextField'; // Importing TextField component from Material-UI
import Button from '@mui/material/Button'; // Importing Button component from Material-UI
import { useState } from 'react'; // Importing useState hook from React
import { MuiFileInput } from 'mui-file-input' // Importing MuiFileInput component for file input handling
import { Stack } from '@mui/material'; // Importing Stack component from Material-UI for layout

// Main App component
function App() {
  // State hooks for managing text output, file selection, and upload status
  const [textOutput, setTextOutput] = useState(["Please Choose a File"]);
  const [file, setFile] = useState("Choose File");
  const [fileUploaded, setFileUploaded] = useState(false);

  // Function to handle form submission
  const handleSubmit = (event) => {
    setTextOutput("This may take a minute. Loading..."); // Updating text output to indicate loading
    const input = document.getElementById("input-field").value; // Retrieving user input
    const options = {
      method: "GET",
      headers: {
        input: input // Setting user input in request headers
      }
    }

    console.log("hello"); // Debugging log

    // Fetch request to backend for processing query
    fetch("http://127.0.0.1:5000/process_query", options)
      .then((response) => response.json())
      .then((data) => {
          console.log(data); // Debugging log
          setTextOutput(data.output); // Updating text output with response from backend
      })

  }

  // Function to handle file upload
  const handleFileUpload = async (event) => {
    const formData = new FormData();
    formData.append('file', file); // Appending selected file to form data

    // Async fetch request to backend for uploading PDF
    await fetch('http://127.0.0.1:5000/upload_pdf', {
            method: 'POST',
            body: formData
    })

    setFileUploaded(!fileUploaded); // Toggling file upload status
    setTextOutput("Please Input Your Query") // Updating text output to prompt user for query
  }
  
  // Rendering the main App component
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
      <h1>AI Counselor</h1> {/* Main heading */}
      <h2>Your own personal counselor to guide you on your academic journey.</h2> {/* Subheading */}
      <div>
        <p>{textOutput}</p> {/* Displaying dynamic text output */}
      </div>
      <Stack spacing={2} direction='row'> {/* Layout container for form elements */}

        {/* Conditional rendering for file input or query input based on upload status */}
        {fileUploaded === false && (<MuiFileInput inputProps={{ accept: '.pdf' }} value={file} onChange={ (newValue) => setFile(newValue)}>Choose File</MuiFileInput>)}
        {fileUploaded === false && ((<Button variant="contained" color="primary" onClick={handleFileUpload}>Submit</Button>))}

        {fileUploaded === true && (<TextField id="input-field" label="Input" variant="outlined" style={{ marginBottom: '20px' }} />)}
        {fileUploaded === true && ((<Button variant="contained" color="primary" onClick={handleSubmit}>Submit</Button>))}
      </Stack>
    </div>
  );
}

export default App; // Exporting App component for use in other parts of the application
