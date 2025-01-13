// console.log("HI");

const fs = require('fs');

// const JSONToFile = (obj, filename) =>
//   fs.writeFileSync(`${filename}.json`, JSON.stringify(obj, null, 2));

// async function fetchAPIData() {
//   const url = "https://gemini.incois.gov.in/incoisapi/rest/hwalatestgeo";
//   const response = await fetch(url, {
//     'headers': { 'Authorization': '446d183e64e64e8eb4bca1407ab02a89' },
//   });
//   if (response.status == 200) {
//     const responseJson = await response.json();
//     JSONToFile(responseJson, 'test');
//     // console.log(responseJson);
//     // console.log(typeof (responseJson));
//   } else {
//     console.log("Failed to fetch: " + response.status);
//   }
// }
// fetchAPIData()

fs.readFile('test.json', 'utf8', (err, data) => {
  if (err) throw err;
  const jsonData = JSON.parse(data);
  const keys = Object.keys(jsonData);
  console.log(keys);
  keys.forEach(key => {
    console.log(`Details of ${key}:`, JSON.stringify(jsonData[key], null, 2));
  });
});

