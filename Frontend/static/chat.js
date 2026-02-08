async function sendMessage() {
  const msg = document.getElementById("msg").value;

  const res = await fetch("/chat", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({message: msg})
  });

  const data = await res.json();
  document.getElementById("chatbox").innerHTML += `<p><b>You:</b> ${msg}</p>`;
  document.getElementById("chatbox").innerHTML += `<p><b>Teacher:</b> ${data.reply}</p>`;

  speak(data.reply);
}
