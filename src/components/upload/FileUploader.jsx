import React, { useState } from 'react'; // Import useState hook
import 'react-dropzone-uploader/dist/styles.css';
import Dropzone from 'react-dropzone-uploader';
import axios from 'axios';

const FileUploader = () => {
  const getUploadParams = () => {
    return { url: 'http://localhost:8000/upload_and_summarize' } // Update URL to your Flask endpoint
  };

  const handleChangeStatus = ({ meta, file }, status) => {
    console.log(status, meta);
  };

  const handleSubmit = async (files, allFiles) => {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('file', file.file);
    });

    try {
      const response = await axios.post('http://localhost:8000/upload_and_summarize', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Upload successful', response.data);
      // You can handle the response data here
    } catch (error) {
      console.error('Upload error:', error.response ? error.response.data : error);
    }

    allFiles.forEach(f => f.remove()); // Clear the dropzone
  };

  return (
    <Dropzone
      getUploadParams={getUploadParams}
      onChangeStatus={handleChangeStatus}
      onSubmit={handleSubmit}
      styles={{ dropzone: { minHeight: 200, maxHeight: 250 } }}
      accept="image/*,application/pdf" // Specify the types of files you accept, if needed
    />
  );
};



// export default FileUploader;
