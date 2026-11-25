(function () {
  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".product-card").forEach((card, index) => {
      const image = card.querySelector(".product-image-wrap img");
      const description = card.querySelector(".product-description");

      if (image && description) {
        if (!description.id) description.id = `product-description-${index + 1}`;
        image.setAttribute("aria-describedby", description.id);
      }

      card.addEventListener("pointermove", (event) => {
        const bounds = card.getBoundingClientRect();
        card.style.setProperty("--glare-x", `${((event.clientX - bounds.left) / bounds.width) * 100}%`);
        card.style.setProperty("--glare-y", `${((event.clientY - bounds.top) / bounds.height) * 100}%`);
      });
    });
  });
})();
