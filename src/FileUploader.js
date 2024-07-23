import React, { useState } from 'react';
import axios from 'axios';

function FileUploadForm() {
  const [file, setFile] = useState(null);
  const [prompt, setPrompt] = useState('');
  const [address, setAddress] = useState('');
  const [response, setResponse] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handlePromptChange = (event) => {
    setPrompt(event.target.value);
  };

  const handleAddressChange = (event) => {
    setAddress(event.target.address);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    formData.append('prompt', prompt);
    formData.append('address', address)

    try {
      const response = await axios.post('http://localhost:8000/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response.data);
      // Handle response...
    } catch (error) {
      console.error('Error uploading file', error);
      // Handle error...
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" onChange={handleFileChange} />
      <input type="text" value={prompt} onChange={handlePromptChange} />
      <button type="submit">Upload and Generate</button>
    </form>
  );
}

export default FileUploadForm;
