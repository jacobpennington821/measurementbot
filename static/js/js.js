$(document).ready(function(){
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

function convertValue(value){
    $.ajax({
        url: "api/querystring",
        dataType: "json",
        data: {
            query: value,
        },
        cache: false,
        success: (data) => {
            displayReading(data);
        },
        error: (data) => {
            displayError(data);
        }
    })
}

function displayReading(reading){
    document.getElementById("outputBox").style.display = "block";
    document.getElementById("outputBox").innerHTML = reading + ".";
}

function displayError(error){
    if(error.status == 400){
        displayReading(error.responseText);
    } else {
        console.log(error);
    }
}
