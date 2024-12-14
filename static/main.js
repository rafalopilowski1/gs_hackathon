const form = document.getElementById("data-form");

form.addEventListener("submit", async (event) => {
  event.preventDefault(); // Zapobiegamy domyślnemu odświeżeniu strony
  const baseUrl = window.location.origin;
  const linkInput = document.getElementById("link").value;
  window.location.assign(`${baseUrl}/api/process?url=${linkInput}`);
});


