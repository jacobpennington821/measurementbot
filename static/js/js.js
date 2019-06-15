$(document).ready(function(){
    document.getElementById("convertButton").addEventListener("click", function(e){
        convertValue(document.getElementById("valueEntry").value, $("#unitEntry").val());
    });
});

function convertValue(value, unit){
    console.log("Value: " + value + ", unit: " + unit);
    $.ajax({
        url: "api/bum",
        dataType: "json",
        data: {
            value: value,
            unit: unit,
        },
        cache: false,
        success: function(data){
            displayReading(data);
        },
    })
}

function displayReading(reading){
    document.getElementById("thiccLoad").innerHTML = reading + ".";
}