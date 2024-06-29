document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll("img[name='category']");
    const coordinates = document.querySelectorAll(".coordinates span");

    images.forEach(image => {
        image.addEventListener("click", () => {
            const locationName = image.closest(".project-detail").querySelector("h2[name='location']").innerText;
            const latitude = image.closest(".project-item").querySelector(".coordinates span[name='lattitude']").innerText;
            const longitude = image.closest(".project-item").querySelector(".coordinates span[name='longitude']").innerText;
            alert(`Location: ${locationName}\nCoordinates: ${latitude}, ${longitude}`);
        });
    });

    coordinates.forEach(coordinate => {
        coordinate.addEventListener("click", () => {
            const latitude = coordinate.closest(".coordinates").querySelector("span[name='lattitude']").innerText;
            const longitude = coordinate.closest(".coordinates").querySelector("span[name='longitude']").innerText;
            alert(`Latitude: ${latitude}\nLongitude: ${longitude}`);
        });
    });
});
