//attempt to use api for stocks, not actually fetching data from the api... 
const BASE_URL = "https://www.alphavantage.co/query?apikey=468Y3C9SB2C35045&function=TIME_SERIES_MONTHLY_ADJUSTED&datatype=json&symbol=";
API = { get };
function get(url) {
return fetch(url)
.then(response => response.json())
.then(data => formatData(data))     
};


function formatData(stockData) {
    options.title.text = stockData["Meta Data"]["2. Symbol"];
    let solution = [];
    Object.entries(stockData["Monthly Adjusted Time Series"]).forEach(
    ([month, monthlyPrices]) => {
    let obj = {};
    obj.x = new Date(month);
    let prices = [];
    prices.push(monthlyPrices["1. open"]);
    prices.push(monthlyPrices["2. high"]);
    prices.push(monthlyPrices["3. low"]);
    prices.push(monthlyPrices["4. close"]); 
    obj.y = prices;
    solution.push(obj);
    },
    );
    options.series[0].data = solution.sort((a, b) => a.x - b.x);
    }


const form = document.querySelector("#search-stock");
form.addEventListener("submit", handleSubmit); 

function handleSubmit() {
    event.preventDefault();
    let symbol = event.target.symbol.value;
    API.get(`${BASE_URL}${symbol}`);
}