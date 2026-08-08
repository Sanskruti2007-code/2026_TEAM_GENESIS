export function speakMarathi(text) {
  if (!text || !("speechSynthesis" in window)) return;

  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);

  utterance.lang = "mr-IN";
  utterance.rate = 0.95;

  window.speechSynthesis.speak(utterance);
}