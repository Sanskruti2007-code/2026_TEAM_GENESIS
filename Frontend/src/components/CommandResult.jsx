export default function CommandResult({
  result,
  error,
}) {
  if (!result && !error) return null;

  return (
    <div
      className={`command-result ${
        error ? "error-box" : "success-box"
      }`}
    >
      {error ? (
        <p>{error}</p>
      ) : (
        <>
          <small>Transcript</small>
          <p>{result.transcript}</p>
          <strong>{result.message}</strong>
        </>
      )}
    </div>
  );
}