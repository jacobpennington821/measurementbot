document.addEventListener("DOMContentLoaded", function(event) { 
    document.getElementById("convertButton").addEventListener("click", () => {
        convertValue(document.getElementById("valueEntry").value);
    });

    document.getElementById("valueEntry").addEventListener("keyup", (e) => {
        if(e.key === "Enter"){
            e.preventDefault();
            document.getElementById("convertButton").click();
        }
    });
});

async function convertValue(value){
    const response = await fetch(
        "api/querystring?" + new URLSearchParams({query: value}).toString(),
        {cache: "no-cache"},
    )
    if (!response.ok){
        displayError(response);
    } else {
        displayReading(await response.json());
    }
}

function displayReading(reading){
    document.getElementById("outputBox").style.display = "block";
    document.getElementById("outputBox").innerHTML = reading + ".";
}

async function displayError(error){
    errorText = await error.text();
    if(error.status == 400){
        displayReading(errorText);
    } else {
        console.log(errorText);
    }
}
