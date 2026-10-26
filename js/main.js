function process() {
    document.getElementById("resultsID").value = "";
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var result = new TextDecoder("utf-8").decode(new Uint8Array(this.response));
            document.getElementById("resultsID").value = result;
        }
    }
    xhr.responseType = "arraybuffer";

    var baseUrl = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
        ? 'http://localhost:8080/'
        : 'https://bba5v6kp7pshugtkd9ii.containers.yandexcloud.net/';
    xhr.open("POST", baseUrl  + document.getElementById("actionID").value);
    xhr.setRequestHeader("percent", document.getElementById("percentID").value);
    xhr.setRequestHeader("prefix", document.getElementById("prefixID").value);
    xhr.setRequestHeader("Content-Type", "text/plain");

    var body = new Object();
    body.component = document.getElementById("componentID").value;
    body.samples = document.getElementById("samplesID").value;
    var jsonBody = JSON.stringify(body);

    xhr.send(jsonBody);
}

function toggleFields() {
    const action = document.getElementById("actionID").value;
    const needsComponent = (action === "subtract" || action === "add" || action === "group_average");
    const needsPercent = (action === "subtract" || action === "add");

    const percentField = document.getElementById("percentID");
    const componentField = document.getElementById("componentID");

    percentField.disabled = !needsPercent;
    percentField.style.backgroundColor = needsPercent ? "white" : "#f0f0f0";

    componentField.disabled = !needsComponent;
    componentField.style.backgroundColor = needsComponent ? "white" : "#f0f0f0";
}

window.onload = toggleFields;