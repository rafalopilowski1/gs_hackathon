document.addEventListener("DOMContentLoaded", function () {
    const inputField = document.getElementById("link");
    const text = "Please type your URL..."; // Tekst do wyświetlenia
    let index = 0; // Aktualna pozycja litery
  
    function typeEffect() {
        inputField.placeholder = text.substring(0, index); // Wyświetlanie kolejnych liter
        index++;
  
        if (index > text.length) {
            // Restart procesu po pełnym wyświetleniu tekstu
            index = 0;
            setTimeout(typeEffect, 1000); // Krótkie opóźnienie przed ponownym startem
        } else {
            setTimeout(typeEffect, 150); // Szybkość pojawiania się liter
        }
    }
  
    typeEffect(); // Uruchomienie efektu
  });