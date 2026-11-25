(function () {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  function resetTilt(element) {
    element.style.transform = "";
    element.style.setProperty("--tilt-x", "0deg");
    element.style.setProperty("--tilt-y", "0deg");
    element.style.setProperty("--tilt-scale", "1");
    element.style.setProperty("--glare-x", "50%");
    element.style.setProperty("--glare-y", "50%");
  }

  document.addEventListener("DOMContentLoaded", () => {
    const tiltItems = document.querySelectorAll([
      "[data-tilt]",
      ".product-card",
      ".info-card",
      ".step-card",
      ".testimonial-card",
      ".contact-card",
      ".feature-card",
      ".service-card",
      ".stat-card",
      ".update-order-card",
      ".auth-aside"
    ].join(","));
    tiltItems.forEach((element) => {
      if (!element.hasAttribute("data-tilt")) element.setAttribute("data-tilt", "");
      resetTilt(element);

      if (finePointer && !reduceMotion) {
        element.addEventListener("pointermove", (event) => {
          const bounds = element.getBoundingClientRect();
          const x = (event.clientX - bounds.left) / bounds.width;
          const y = (event.clientY - bounds.top) / bounds.height;
          const strength = Number(element.dataset.tiltStrength) || 8;
          const rotateY = (x - 0.5) * strength;
          const rotateX = (0.5 - y) * strength;
          element.style.setProperty("--tilt-y", `${rotateY}deg`);
          element.style.setProperty("--tilt-x", `${rotateX}deg`);
          element.style.setProperty("--tilt-scale", "1.015");
          element.style.setProperty("--glare-x", `${x * 100}%`);
          element.style.setProperty("--glare-y", `${y * 100}%`);
        });
        element.addEventListener("pointerleave", () => resetTilt(element));
      }

    });
  });
})();
