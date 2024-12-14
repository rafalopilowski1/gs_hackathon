const form = document.getElementById("data-form");

form.addEventListener("submit", async (event) => {
  event.preventDefault(); // Zapobiegamy domyślnemu odświeżeniu strony
  const baseUrl = window.location.origin;
  const linkInput = document.getElementById("link").value;
  const apikey = document.getElementById("apikey").value;
  if (apikey === "") {
    window.location.assign(`${baseUrl}/api/process?url=${linkInput}&apikey=${apikey}`);
  } else {
    window.location.assign(`${baseUrl}/api/process?url=${linkInput}`);
  }
});


