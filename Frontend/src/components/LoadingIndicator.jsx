export default function LoadingIndicator({
  text = "Processing...",
}) {
  return (
    <span className="loading">
      <span className="spinner" />
      {text}
    </span>
  );
}