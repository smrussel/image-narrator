const upload_button = document.querySelector("#upload");
const result_container = document.querySelector("#result");

upload_button.addEventListener("click", () => {
    const file_input = document.createElement("input");
    file_input.type = "file";
    file_input.accept = "image/*";
    file_input.click();

    file_input.addEventListener("change", () => {
        loading();

        const file = file_input.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imageContainer = document.getElementById('imageContainer');
                imageContainer.innerHTML = `<img src="${e.target.result}" class="image-preview" alt="Uploaded Image">`;
            }
            reader.readAsDataURL(file);
        }

        const fd = new FormData();
        fd.append("image", file);

        fetch("/upload", {
            method: "POST",
            body: fd
        }).then(response => response.json())
        .then(data => {
            stop_loading();
            result_container.textContent = data.result.overall_explanation
        });
    });
});




function loading() {
    document.querySelector("#upload").style.display = "none";
    document.querySelector("#result").style.display = "none";
    document.querySelector("#spinner").style.display = "block";
}

function stop_loading() {
    document.querySelector("#spinner").style.display = "none";
    document.querySelector("#upload").style.display = "block";
    document.querySelector("#result").style.display = "block";
}


