// Delete Confirmation Modal

const deleteModal = document.getElementById("deleteModal");

const cancelDelete = document.getElementById("cancelDelete");

const confirmDelete = document.getElementById("confirmDelete");

const deleteTaskName = document.getElementById("deleteTaskName");

let selectedForm = null;


// Open Modal

document.querySelectorAll(".delete-btn").forEach(button => {

    button.addEventListener("click", function () {

        selectedForm = this.closest(".delete-form");

        deleteTaskName.textContent = this.dataset.taskTitle;

        deleteModal.classList.add("active");

    });

});


// Close Modal

cancelDelete.addEventListener("click", function () {

    deleteModal.classList.remove("active");

    selectedForm = null;

});


// Confirm Delete

confirmDelete.addEventListener("click", function () {

    if (selectedForm) {
        selectedForm.submit();
    }

});


// Close when clicking outside

deleteModal.addEventListener("click", function (event) {

    if (event.target === deleteModal) {

        deleteModal.classList.remove("active");

        selectedForm = null;

    }

});


// Close with Escape key

document.addEventListener("keydown", function (event) {

    if (event.key === "Escape") {

        deleteModal.classList.remove("active");

        selectedForm = null;

    }

});