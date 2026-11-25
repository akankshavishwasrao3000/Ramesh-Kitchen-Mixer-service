(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const price = document.getElementById("price");
    const quantity = document.getElementById("quantity");
    const total = document.getElementById("order-live-total");
    if (!price || !quantity || !total) return;

    const formatCurrency = new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 2
    });

    const updatePreview = () => {
      const unitPrice = Number.parseFloat(price.value);
      const count = Number.parseInt(quantity.value, 10);
      total.textContent = Number.isFinite(unitPrice) && Number.isFinite(count) && count > 0
        ? formatCurrency.format(unitPrice * count)
        : "—";
    };

    quantity.addEventListener("input", updatePreview);
    updatePreview();
  });
})();
