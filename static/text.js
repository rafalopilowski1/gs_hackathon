document.addEventListener("DOMContentLoaded", () => {
  const inputField = document.getElementById("link");
  const textOne = "Please type your OpenAPI spec URL..."; // Tekst do wyświetlenia
  let indexOne = 0; // Aktualna pozycja litery

  const apikeyField = document.getElementById("apikey");
  const textTwo = "Please type your API key..."; // Tekst do wyświetlenia
  let indexTwo = 0; // Aktualna pozycja litery

  typeEffect(inputField, textOne, indexOne); // Uruchomienie efektu
  typeEffect(apikeyField, textTwo, indexTwo); // Uruchomienie efektu
});

const typeEffect = (inputField, text, index) => {
  inputField.placeholder = text.substring(0, index); // Wyświetlanie kolejnych liter
  index++;

  if (index > text.length) {
    // Restart procesu po pełnym wyświetleniu tekstu
    index = 0;
    setTimeout(typeEffect, 1000, inputField, text, index); // Krótkie opóźnienie przed ponownym startem
  } else {
    setTimeout(typeEffect, 150, inputField, text, index); // Szybkość pojawiania się liter
  }
};
