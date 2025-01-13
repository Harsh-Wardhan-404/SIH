async function fetchAPIData() {
  const url = "https://gemini.incois.gov.in/OceanDataAPI/api/wqns/Vizag/currentDirection";
  const response = await fetch(url, {
    'headers': { 'Authorization': '446d183e64e64e8eb4bca1407ab02a89' },
  });
  if (response.status == 200) {
    const responseJson = await response.json();
    console.log(responseJson);
    console.log(typeof (responseJson));
  } else {
    console.log("Error");
  }
}

fetchAPIData()