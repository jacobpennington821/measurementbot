document.onload = function(){
    document.getElementById("convertButton").addEventListener("click", function(e){
        convertValue(document.getElementById("valueEntry").value, $("#unitEntry").val());
    });
}

function convertValue(value, unit){
    console.log("Value: " + value + ", unit: " + unit);
    $.ajax({
        url: "/bum",
        dataType: "json",
        data: {
            value: value,
            unit: unit,
        },
        success: function(data){
            document.getElementById("thiccLoad").innerHTML = data;
            console.log(data);
        },
    })
}