import React, { useState } from 'react';
import "./App.sass";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowUpFromBracket } from "@fortawesome/free-solid-svg-icons";
import Visualization from "./Visualization";
// Assuming DynamicTag component is properly imported
import DynamicTag from "./components/DynamicTag";

function App() {
  const [isVisualizationShown, setIsVisualizationShown] = useState(false);
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

  // Function to handle button click to switch to visualization
  const handleAnalyzeDataClick = () => {
    setIsVisualizationShown(true); // Change state to show the visualization page
  };

  // Trigger the hidden file input when the upload area is clicked
  const handleClick = () => {
    document.getElementById('fileInput').click();
  };

  return (
    <>
      {!isVisualizationShown ? (
        <div className="page upload" style={{ padding: "22px 390px" }}>
          <h2 style={{ textAlign: "center" }}>Upload an image to analyze</h2>
          <div className="upload-contain" onClick={handleClick}>
            <div className="tag-row">
              <DynamicTag condition="primary" tagName="Labeled image"></DynamicTag>
              <DynamicTag condition="" tagName="Unlabeled image"></DynamicTag>
            </div>
            <div className="upload-box">
              <div className="upload-text">
                <div className="icon-contain" style={{display:"flex", justifyContent: "center" }}>
                  <FontAwesomeIcon icon={faArrowUpFromBracket} style={{ fontSize: "32px", textAlign: "center" }}/>
                </div>
                <p>Drop a photograph here</p>
                <input type="file" id="fileInput" style={{ display: 'none' }} onChange={handleFileChange} accept="image/*" />
              </div>
            </div>
            {uploadProgress && (
              <div className="loading-contain">
                <h3>Files have been uploaded</h3>
                <p>{uploadProgress} uploaded</p>
              </div>
            )}
          </div>
          <button className="primary" onClick={handleAnalyzeDataClick}>Analyze data</button>
        </div>
      ) : (
        <Visualization />
      )}
    </>
  );
}

export default App;
