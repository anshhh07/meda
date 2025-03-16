// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-app.js";
import {getAuth, signInWithEmailAndPassword,} from "https://www.gstatic.com/firebasejs/11.4.0/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyAb1Jr1IrbVYER3FWVttu2Ari4Zog5VbDM",
    authDomain: "hack-a11dc.firebaseapp.com",
    databaseURL: "https://hack-a11dc-default-rtdb.firebaseio.com",
    projectId: "hack-a11dc",
    storageBucket: "hack-a11dc.firebasestorage.app",
    messagingSenderId: "966520082620",
    appId: "1:966520082620:web:2af820deff76cf2771c0b9",
    measurementId: "G-YN8PMVY3YJ"
  };

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
// submit

const submit = document.getElementById("submit");
submit.addEventListener("click", function (event) {
  event.preventDefault();

  //inputs
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Signed up
      const user = userCredential.user;
      alert("logging in..");
      window.location.href = "index2.html";
      // ...
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      alert(errorMessage);
      // ..
    });
});
