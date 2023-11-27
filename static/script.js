document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault();

    // Show loading message
    document.getElementById("loading").style.display = "block";

    // Reset output
    document.getElementById("fileList").innerHTML = "";

    // FormData for file upload
    var formData = new FormData(this);

    // Fetch API to handle file upload
    fetch("/api/upload-file/", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading message
        document.getElementById("loading").style.display = "none";

        // Show response
        document.getElementById("response").style.display = "block";

        // Display file paths in a numbered list
        var fileListElement = document.getElementById("fileList");
        data.file_paths.forEach((filePath, index) => {
            var listItem = document.createElement("li");
            // listItem.textContent = `${index + 1}. ${filePath}`;
            listItem.textContent = `${filePath}`;
            fileListElement.appendChild(listItem);
        });
    })
    .catch(error => console.error("Error:", error));
});
