document.getElementById("uploadForm").addEventListener("submit", function(event) {
            event.preventDefault();

            // Show loading message
            document.getElementById("loading").style.display = "block";

            // Reset output
            document.getElementById("thumbnailContainer").innerHTML = "";

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

                // // Display selected file name
                // var selectedFileName = document.getElementById("selectedFileName").textContent;
                // var selectedFileElement = document.createElement("p");
                // selectedFileElement.textContent = "Selected File: " + selectedFileName;
                // document.getElementById("response").appendChild(selectedFileElement);

                // Display thumbnail images
                var thumbnailContainer = document.getElementById("thumbnailContainer");

                data.thumbnail_paths.forEach((thumbnailPath, index) => {
                    var thumbnailImage = document.createElement("img");
                    thumbnailImage.src = thumbnailPath;
                    thumbnailImage.alt = "Thumbnail";
                    thumbnailImage.classList.add("thumbnail");

                    // Add click event to open the image in a new window or tab
                    thumbnailImage.addEventListener("click", function() {
                        // Ensure that the index is within the bounds of data.file_paths
                        if (index < data.file_paths.length) {
                            window.open(data.file_paths[index], "_blank");
                        } else {
                            console.error("Corresponding file path not found for thumbnail at index:", index);
                        }
                    });

                    thumbnailContainer.appendChild(thumbnailImage);
                });

                // end thumbnails
            })
            .catch(error => console.error("Error:", error));
        });

        document.getElementById("resetButton").addEventListener("click", function() {
            // Hide response
            document.getElementById("response").style.display = "none";

            // Clear file input
            document.getElementById("fileInput").value = "";
            // Reset selected file name display
            document.getElementById("selectedFileName").textContent = "";
            // Reset choose file text
            document.getElementById("chooseFileText").textContent = "Choose File";
        });

        document.getElementById("fileInput").addEventListener("change", function() {
            var fileName = this.value.split("\\").pop();
            document.getElementById("selectedFileName").textContent = fileName;
            document.getElementById("chooseFileText").textContent = "Change File";
        });