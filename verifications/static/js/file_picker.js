const input = document.getElementById('file-input');
const list = document.getElementById('file-list');

const MAX_FILES = 3;
let files = [];

input.addEventListener('change', () => {
    const selectedFiles = Array.from(input.files);

    if (files.length + selectedFiles.length > MAX_FILES) {
        alert(`Можна завантажити не більше ${MAX_FILES} файлів`);
        input.value = "";
        return;
    }

    files = files.concat(selectedFiles);
    syncInputFiles();
    render();
});

function removeFile(index) {
    files.splice(index, 1);
    syncInputFiles();
    render();
}

function syncInputFiles() {
    const dt = new DataTransfer();
    files.forEach(file => dt.items.add(file));
    input.files = dt.files;
}

function render() {
    list.innerHTML = "";

    files.forEach((file, index) => {
        const li = document.createElement("li");
        li.className =
            "list-group-item d-flex justify-content-between align-items-center";

        li.innerHTML = `
            <span>${file.name}</span>
            <button type="button"
                    class="btn btn-sm btn-outline-danger">
                ✕
            </button>
        `;

        li.querySelector("button").onclick = () => removeFile(index);
        list.appendChild(li);
    });
}
