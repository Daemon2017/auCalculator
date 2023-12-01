function subtract() {
    document.getElementById("resultsID").value = "";
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var result = String.fromCharCode.apply(null, new Uint8Array(this.response));
            document.getElementById("resultsID").value = result;
        }
    }
    xhr.responseType = "arraybuffer";

    xhr.open("POST", "https://bba5v6kp7pshugtkd9ii.containers.yandexcloud.net/subtract");
    xhr.setRequestHeader("percent", document.getElementById("percentID").value);
    xhr.setRequestHeader("Content-Type", "text/plain");

    var body = new Object();
    body.component = document.getElementById("componentID").value;
    body.samples = document.getElementById("samplesID").value;
    var jsonBody= JSON.stringify(body);

    xhr.send(jsonBody);
}