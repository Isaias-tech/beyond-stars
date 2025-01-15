function showFlashMessage(message, type) {
    const categoryClass = {
        success: "success",
        error: "error",
        warning: "warning",
        info: "info",
    }[type] || "info";

    const flashMessage = document.createElement("div");
    flashMessage.className = `flash-message ${categoryClass}`;
    flashMessage.textContent = message;

    const container = document.getElementById("flash-messages-container");
    container.appendChild(flashMessage);

    setTimeout(() => {
        flashMessage.remove();
    }, 3000);
}

if (typeof flashMessages !== "undefined") {
    flashMessages.forEach(({ category, message }) => {
        showFlashMessage(message, category);
    });
}
