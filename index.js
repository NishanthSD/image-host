const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();
const port = 3000;

// Serve static files (images)
app.use(express.static(path.join(__dirname, 'public')));
app.use('/images', express.static(path.join(__dirname, 'res_images')));

// Function to get folder structure
function getFolderStructure(dir) {
  let structure = [];
  const items = fs.readdirSync(dir);

  items.forEach(item => {
    const fullPath = path.join(dir, item);
    const stats = fs.statSync(fullPath);

    if (stats.isDirectory()) {
      structure.push({
        name: item,
        type: 'folder',
        subfolders: getFolderStructure(fullPath),
        images: []
      });
    } else if (stats.isFile() && /\.(jpg|jpeg|png|gif)$/i.test(item)) {
      // Adjust the path to remove 'res_images' from the URL
      const relativePath = path.relative(path.join(__dirname, 'res_images'), fullPath);
      //console.log(`Image path generated: /images/${relativePath.replace(/\\/g, '/')}`); // Debugging the path

      structure.push({
        name: item,
        type: 'image',
        path: `/images/${relativePath.replace(/\\/g, '/')}`
      });
    }
  });

  //console.log("Folder Structure:", JSON.stringify(structure, null, 2)); // Debugging the entire folder structure
  return structure;
}

// Route to serve the gallery
app.get('/', (req, res) => {
  const folderStructure = getFolderStructure(path.join(__dirname, 'res_images'));
  
  res.render('index', { folderStructure });
});

// Set view engine to EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Start the server
app.listen(port, () => {
});
