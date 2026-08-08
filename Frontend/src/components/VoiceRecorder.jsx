import { useRef, useState } from "react";
import { Mic, Square } from "lucide-react";
import { api } from "../services/api";
import { speakMarathi } from "../services/speech";
import CommandResult from "./CommandResult";
import LoadingIndicator from "./LoadingIndicator";

export default function VoiceRecorder({
  onDemoCommand,
}) {
  const [recording, setRecording] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const recorderRef = useRef(null);
  const chunksRef = useRef([]);

  const showResult = (data) => {
    const normalized = {
      transcript:
        data.transcript || "Voice command received",
      message:
        data.message ||
        data.response ||
        "Command completed.",
    };

    setResult(normalized);
    speakMarathi(normalized.message);
  };

  const runDemo = (intent) => {
    try {
      setError("");
      showResult(onDemoCommand(intent));
    } catch (err) {
      setError(err.message);
    }
  };

  const startRecording = async () => {
    try {
      setError("");
      setResult(null);

      const stream =
        await navigator.mediaDevices.getUserMedia({
          audio: true,
        });

      const recorder = new MediaRecorder(stream);

      recorderRef.current = recorder;
      chunksRef.current = [];

      recorder.ondataavailable = (event) => {
        chunksRef.current.push(event.data);
      };

      recorder.onstop = async () => {
        stream
          .getTracks()
          .forEach((track) => track.stop());

        const blob = new Blob(chunksRef.current, {
          type: "audio/webm",
        });

        if (
          import.meta.env.VITE_DEMO_MODE === "true"
        ) {
          showResult(
            onDemoCommand("TODAY_REPORT")
          );
          return;
        }

        try {
          setProcessing(true);
          const response =
            await api.processVoice(blob);

          showResult(response);
        } catch (err) {
          setError(err.message);
        } finally {
          setProcessing(false);
        }
      };

      recorder.start();
      setRecording(true);
    } catch {
      setError(
        "Microphone permission was denied or is unavailable."
      );
    }
  };

  const stopRecording = () => {
    recorderRef.current?.stop();
    setRecording(false);
  };

  return (
    <section className="voice-card">
      <div>
        <span className="eyebrow gold">
          VyaparSaathi Voice
        </span>

        <h2>
          Speak. We’ll handle the business.
        </h2>

        <p>
          Give Marathi commands to add stock,
          record a sale or request today’s report.
        </p>
      </div>

      <button
        className={`mic-button ${
          recording ? "recording" : ""
        }`}
        onClick={
          recording ? stopRecording : startRecording
        }
      >
        {recording ? <Square /> : <Mic />}
      </button>

      <p className="mic-label">
        {recording
          ? "Listening… tap to stop"
          : "Tap the microphone to begin"}
      </p>

      <div className="demo-actions">
        <button
          onClick={() => runDemo("ADD_STOCK")}
        >
          Demo: Add Stock
        </button>

        <button
          onClick={() => runDemo("RECORD_SALE")}
        >
          Demo: Record Sale
        </button>

        <button
          onClick={() => runDemo("TODAY_REPORT")}
        >
          Demo: Daily Report
        </button>
      </div>

      {processing && (
        <LoadingIndicator text="Understanding command..." />
      )}

      <CommandResult
        result={result}
        error={error}
      />
    </section>
  );
}