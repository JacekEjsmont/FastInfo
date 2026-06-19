(() => {
  const synth = window.speechSynthesis;
  const supportsTts = Boolean(synth && "SpeechSynthesisUtterance" in window);
  let activeButton = null;
  let activeUtterance = null;

  function setButtonState(button, state) {
    if (!button) return;
    button.dataset.ttsState = state;
    const playIcon = button.querySelector(".icon--play");
    const pauseIcon = button.querySelector(".icon--pause");
    if (playIcon && pauseIcon) {
      playIcon.hidden = state === "speaking";
      pauseIcon.hidden = state !== "speaking";
    }
  }

  function resetActiveButton() {
    if (activeButton) {
      setButtonState(activeButton, "idle");
    }
    activeButton = null;
    activeUtterance = null;
  }

  function buildSpeechText(item) {
    const title = (item?.dataset.ttsTitle || "").trim();
    const text = (item?.dataset.ttsText || "").trim();
    if (title && text) return `${title}. ${text}`;
    return title || text;
  }

  function speak(item, button) {
    const text = buildSpeechText(item);
    if (!text) return;

    synth.cancel();
    resetActiveButton();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "pl-PL";
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.onend = () => {
      if (activeUtterance === utterance) {
        resetActiveButton();
      }
    };
    utterance.onerror = () => {
      if (activeUtterance === utterance) {
        resetActiveButton();
      }
    };

    activeButton = button;
    activeUtterance = utterance;
    setButtonState(button, "speaking");
    synth.speak(utterance);
  }

  function toggleSpeech(button) {
    const item = button.closest("[data-tts-item]");
    if (!item) return;

    if (activeButton === button && activeUtterance) {
      if (synth.speaking && !synth.paused) {
        synth.pause();
        setButtonState(button, "paused");
        return;
      }

      if (synth.paused) {
        synth.resume();
        setButtonState(button, "speaking");
        return;
      }
    }

    speak(item, button);
  }

  function stopSpeech(button) {
    if (activeButton && activeButton !== button) {
      setButtonState(activeButton, "idle");
    }
    synth.cancel();
    resetActiveButton();
  }

  function disableControls() {
    document.querySelectorAll("[data-tts-button], [data-tts-stop]").forEach((button) => {
      button.disabled = true;
      button.title = "TTS niedostępny w tej przeglądarce";
    });
  }

  document.addEventListener("click", (event) => {
    const speechButton = event.target.closest("[data-tts-button]");
    if (speechButton) {
      event.preventDefault();
      toggleSpeech(speechButton);
      return;
    }

    const stopButton = event.target.closest("[data-tts-stop]");
    if (stopButton) {
      event.preventDefault();
      stopSpeech(stopButton);
    }
  });

  if (!supportsTts) {
    disableControls();
  }
})();
