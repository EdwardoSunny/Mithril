import React, { useState } from 'react';
import "./App.sass";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowUpFromBracket } from "@fortawesome/free-solid-svg-icons";
import Visualization from "./Visualization";

function App() {
  const [uploadProgress, setUploadProgress] = useState(null); // Track upload progress
  const [file, setFile] = useState(null); // Track the selected file

  // Handle file selection
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      // Simulate an upload - replace this with actual upload logic
      setUploadProgress('100%'); // Assume file is immediately uploaded for demo purposes
    }
  };

  // Trigger the hidden file input when the upload area is clicked
  const handleClick = () => {
    document.getElementById('fileInput').click();
  };

  // Handle the upload process to your endpoint
  const handleUpload = async () => {
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
    
      try {
        const response = await fetch('http://127.0.0.1:5000/upload', {
          method: 'POST',
          body: formData,
        });
  
        if (response.ok) {
          console.log('Upload successful');
          // Handle successful upload here
        } else {
          // If response is not ok, attempt to parse the error message from the response body
          let errorMessage;
          try {
            const errorData = await response.json();
            errorMessage = errorData.message; // Assuming the server sends error messages in a 'message' field
          } catch (error) {
            errorMessage = 'Unknown error occurred'; // Fallback message if parsing fails
          }
  
          console.error('Upload failed:', errorMessage);
          // Handle upload error here
        }
      } catch (error) {
        console.error('Error:', error);
        // Handle network errors here
      }
    }
  };
  

  return (
    <>
      <div className="page upload" style={{ padding: "22px 390px" }}>
        <h2 style={{ textAlign: "center" }}>Upload Images to Analyze</h2>
        <div className="upload-contain" onClick={handleClick}>
          <div className="upload-box">
            <div className="upload-text">
              <div className="icon-contain" style={{display:"flex", justifyContent: "center" }}>
                <FontAwesomeIcon
                  icon={faArrowUpFromBracket}
                  style={{ fontSize: "32px", textAlign: "center" }}
                />
              </div>
              <p>Click to Drop Images</p>
              <input type="file" id="fileInput" style={{ display: 'none' }} onChange={handleFileChange} accept=".zip" />
            </div>
          </div>
        </div>
        <div className="loading-contain">
          <h3>{uploadProgress ? 'Files have been uploaded' : 'Click above to upload files'}</h3>
          {uploadProgress && <p>{uploadProgress} uploaded</p>}
        </div>
        <button className="primary" onClick={handleUpload}>Analyze data</button>
      </div> 

      <Visualization />
    </>
  );
}

export default App;
