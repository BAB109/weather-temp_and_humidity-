//import {info} from './weather.py';
function data(){
    let city=document.getElementById("city").value;
    let country_code=document.getElementById("country_code").value;
    let event=document.getElementById("b");
    document.getElementById("b").addEventListener("click", () => {
    const city = document.getElementById("city").value;
    const country = document.getElementById("country_code").value;

    fetch(`/weather?city=${city}&country=${country}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("temp").innerText =
                `Temperature: ${data.temperature} °C`;

            document.getElementById("humidity").innerText =
                `Humidity: ${data.humidity}%`;
        })
        .catch(err => console.error(err));
    });
}
data()