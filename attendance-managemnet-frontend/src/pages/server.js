const express = require('express');
const fileUpload = require('express-fileupload');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 1000;

app.use(cors());

// Enable file upload
app.use(fileUpload());

// Handle image upload
app.post('/api/upload-image', (req, res) => {
  if (!req.files || !req.files.image) {
    return res.status(400).json({ error: 'No image uploaded' });
  }

  const image = req.files.image;

  // Save the uploaded image to a temporary directory (if necessary)
  const imagePath = 'temp/' + image.name;
  image.mv(imagePath, (err) => {
    if (err) {
      return res.status(500).send(err);
    }

    // TODO: Send your Python backend the image path to process.
    // You can use Python subprocess or an HTTP request to connect to the backend here

    res.json({ message: 'Image uploaded successfully', imagePath });
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
