import React, { useState, useEffect } from 'react';


const HomePage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [predictedImageUrl, setPredictedImageUrl] = useState(null);

  useEffect(() => {
    const storedImageUrl = localStorage.getItem('selectedImage');
    if (storedImageUrl) {
      setImageUrl(storedImageUrl);
    }
  }, []);

  useEffect(() => {
    const storedFile = localStorage.getItem('selectedFile');
    if (storedFile) {
      setSelectedFile(JSON.parse(storedFile));
    }
  }, []);

    // Event handler for file input change
    const handleFileChange = (event) => {
      const file = event.target.files[0];
      setSelectedFile(file);
  
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          const imageUrl = reader.result;
          setImageUrl(imageUrl);
          localStorage.setItem('selectedFile', JSON.stringify(file));
          localStorage.setItem('selectedImage', imageUrl);
        };
        reader.readAsDataURL(file);
      }
    };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    console.log(selectedFile)
    formData.append('file', selectedFile); // Use selectedFile instead of file

    
    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
      
      })
      console.log(response);
  
      if (response.ok) {
        const blobData = await response.blob();
        const imageUrl = URL.createObjectURL(blobData);
        setPredictedImageUrl(imageUrl);
      } else {
        throw new Error('Request failed with status ' + response.status);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className='Page' style={{ display: "flex", flexDirection: "column" }}>
      <div className='Title' style={{ display: "flex", justifyContent: "center", alignItems: "center" }}>
        <h1>The Tree Recognition App</h1>
      </div>
      <div className='Input field'>
        <label htmlFor="fileInput">
          <span>Choose an image:</span>
          <input
            type="file"
            id="fileInput"
            accept="image/*"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
        </label>
        <button onClick={() => document.getElementById('fileInput').click()}>
          Choose an image
        </button>
      </div>
      {imageUrl && (
        <div className='Display Image' style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
          <h2>Uploaded Image</h2>
          <img src={imageUrl} alt="Uploaded" style={{ maxWidth: '100%' }} />
        </div>
      )}
      {1 && (
        <div className='Display Predicted Image' style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
          <h2>Predicted Image</h2>
          <img src={predictedImageUrl} alt="Predicted" style={{ maxWidth: '100%' }} />
        </div>
      )}
      <div className='Output field'>
        <button onClick={handleSubmit}>
          Predict the output image
        </button>
      </div>
    </div>
  );
};

export default HomePage;

