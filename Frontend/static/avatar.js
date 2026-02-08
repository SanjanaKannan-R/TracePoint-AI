function speak(text) {
  fetch("/tts", {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({text})
  }).then(() => {
    const audio = new Audio("/static/voice.mp3");
    audio.play();
  });
}
