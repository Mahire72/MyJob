const formulaire = document.getElementById("Myform");
const input = document.getElementById("input");
const liste = document.getElementById("liste");


formulaire.addEventListener("submit", function(event){
    event.preventDefault();
    const value = input.value;
    console.log("ok")

    const li =document.createElement("li");
    li.textContent = value;
    liste.appendChild(li);

});