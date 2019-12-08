$(document).ready(function(){
    document.getElementById("convertButton").addEventListener("click", () => {
        convertValue(document.getElementById("valueEntry").value);
    });

    document.getElementById("valueEntry").addEventListener("keyup", (e) => {
        if(e.keyCode === 13){
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
        success: function(data){
            displayReading(data);
        },
    })
}

function displayReading(reading){
    document.getElementById("thiccLoad").innerHTML = reading + ".";
}