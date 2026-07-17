const fs = require('fs');
const src = 'C:/Users/Admin/Documents/cust/infotec/index-cyber.html';
const dest = 'C:/Users/Admin/Documents/cust/infotec/index.html';
fs.copyFileSync(src, dest);
console.log('Copied', fs.readFileSync(dest, 'utf8').split('\n').length, 'lines');