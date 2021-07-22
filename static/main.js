const static = document.getElementById("static");
const video = document.getElementById("video");
const button = document.getElementById("switch");

const SWITCH = true;

button.addEventListener("click", (e) => {
  console.log(e.innerHTML);
  button.innerHTML = SWITCh ? "Switch to Static" : "Switch to Live Stream";
});
