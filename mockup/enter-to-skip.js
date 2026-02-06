// Una cazzata che ho fatto per fare le interfacce di creazione più carine - Rodrigo Mamani Yupanqui

const campi = document.querySelectorAll(
  'input[type="text"], input[type="number"], input[type="date"], select, textarea'
); // Aggiornare opzioni se un campo non viene segnalato.

campi.forEach((campo, index) => {
  campo.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();

      const seguente = campi[index + 1];
      if (seguente) {
        seguente.focus();
      }
    }
  });
});
