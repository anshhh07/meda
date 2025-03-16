document.addEventListener("DOMContentLoaded", function () {
  const bookButton = document.querySelector("button");
  bookButton.addEventListener("click", async function () {
      const doctor = document.querySelector("select:nth-of-type(1)").value;
      const timeSlot = document.querySelector("select:nth-of-type(2)").value;
      const patientName = prompt("Enter your name:");

      if (!patientName) {
          alert("Patient name is required.");
          return;
      }

      const response = await fetch("http://127.0.0.1:8000/book-appointment/", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify({ doctor, time_slot: timeSlot, patient_name: patientName })
      });

      const data = await response.json();
      alert(data.message);
  });
});
