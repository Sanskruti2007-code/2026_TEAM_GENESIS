import { useRef, useState } from "react";
import { Mic, Send, Square } from "lucide-react";
import { api } from "../services/api";
import { speakMarathi } from "../services/speech";
import CommandResult from "./CommandResult";
import LoadingIndicator from "./LoadingIndicator";

export default function VoiceRecorder({
  onDemoCommand,
  onTextCommand,
  onCommandComplete,
}) {
  const [recording, setRecording] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [commandText, setCommandText] = useState("");

  const recorderRef = useRef(null);
  const chunksRef = useRef([]);

  const showResult = (data) => {
    const normalized = {
      transcript: data.transcript || "Command received",
      message: data.message || data.response || "Command completed.",
    };
    setResult(normalized);
    speakMarathi(normalized.message);
  };

  const runCommand = async (callback) => {
    try {
      setError("");
      setProcessing(true);
      const response = await callback();
      if (response?.success === false) {
        throw new Error(response.message || "Command could not be completed.");
      }
      showResult(response);
      await onCommandComplete?.();
    } catch (err) {
      setError(err.message);
    } finally {
      setProcessing(false);
    }
  };

  const runDemo = (intent) => runCommand(() => onDemoCommand(intent));

  const submitText = (event) => {
    event.preventDefault();
    const text = commandText.trim();
    if (!text) return;
    runCommand(() => onTextCommand(text));
  };

  const startRecording = async () => {
    try {
      setError("");
      setResult(null);
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);

      recorderRef.current = recorder;
      chunksRef.current = [];
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) chunksRef.current.push(event.data);
      };

      recorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        await runCommand(() => api.processVoice(blob));
      };

      recorder.start();
      setRecording(true);
    } catch {
      setError("Microphone permission was denied or is unavailable.");
    }
  };

  const stopRecording = () => {
    recorderRef.current?.stop();
    setRecording(false);
  };

  return (
    <section className="voice-card">
      <div>
        <span className="eyebrow gold">VyaparSaathi Voice</span>
        <h2>Speak. We’ll handle the business.</h2>
        <p>
          Marathi, Hindi, Hinglish or English mein stock add karo, sale
          record karo ya aaj ka report pucho.
        </p>
      </div>

      <button
        className={`mic-button ${recording ? "recording" : ""}`}
        onClick={recording ? stopRecording : startRecording}
        disabled={processing}
        aria-label={recording ? "Stop recording" : "Start recording"}
      >
        {recording ? <Square /> : <Mic />}
      </button>

      <p className="mic-label">
        {recording ? "Listening… tap to stop" : "Tap the microphone to begin"}
      </p>

      <form className="command-compose" onSubmit={submitText}>
        <input
          value={commandText}
          onChange={(event) => setCommandText(event.target.value)}
          placeholder="Try: Sell 3 Dettol Soap"
          aria-label="Type a business command"
        />
        <button type="submit" disabled={processing || !commandText.trim()}>
          <Send size={17} />
          Run
        </button>
      </form>

      <div className="demo-actions">
        <button onClick={() => runDemo("ADD_STOCK")} disabled={processing}>
          Add 20 Dettol
        </button>
        <button onClick={() => runDemo("RECORD_SALE")} disabled={processing}>
          Sell 3 Dettol
        </button>
        <button onClick={() => runDemo("TODAY_REPORT")} disabled={processing}>
          Daily Report
        </button>
      </div>

      {processing && <LoadingIndicator text="Understanding command..." />}
      <CommandResult result={result} error={error} />
    </section>
  );
}
