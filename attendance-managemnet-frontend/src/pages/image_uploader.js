import React, { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';

const ImageUploader = () => {
  const [uploadedImage, setUploadedImage] = useState(null);

  const onDrop = async (acceptedFiles) => {
    const formData = new FormData();
    formData.append('image', acceptedFiles[0]);
//try catch block
    try {
      const response = await axios.post('/api/upload-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log(response.data);

      setUploadedImage(URL.createObjectURL(acceptedFiles[0]));
    } catch (error) {
      console.error('There was Error when you are  uploading image:', error);
    }
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <div>
      <div {...getRootProps()} className="dropzone">
        <input {...getInputProps()} />
        <p>Drag & drop an image file here, or click to select one</p>
      </div>
      {uploadedImage && (
        <div>
          <h2>Uploaded Image:</h2>
          <img src={uploadedImage} alt="Uploaded" width="300" />
        </div>
      )}
    </div>
  );
};

export default ImageUploader;
