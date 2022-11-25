
function myfunction() {
        const a = document.getElementById("a").href;
        const label = document.getElementById("label").value;
        const text = document.getElementById("search").value;
        const dict_values = {a, label, text} //Pass the javascript variables to a dictionary.
        const s = JSON.stringify(dict_values); // Stringify converts a JavaScript object or value to a JSON string
        console.log(s); // Prints the variables to console window, which are in the JSON format
        $.ajax({
            url:"/saveInputAndLabel",
            type:"POST",
            contentType: "application/json",
            data: JSON.stringify(s)})
}




