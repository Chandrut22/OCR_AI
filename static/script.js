document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    let fileInput = document.getElementById("fileInput");
    let resultDiv = document.getElementById("result");

    if (!fileInput.files.length) {
        resultDiv.innerHTML = "<p style='color: red;'>Please select a file.</p>";
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        } else {
            resultDiv.innerHTML = `<p><strong>Extracted Text:</strong> ${data.result}</p>`;
        }
    })
    .catch(error => {
        resultDiv.innerHTML = `<p style="color: red;">Error: ${error}</p>`;
    });
});
