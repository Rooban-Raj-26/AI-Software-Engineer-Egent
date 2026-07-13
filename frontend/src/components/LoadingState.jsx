export default function LoadingState() {
  return (
    <div className="w-full max-w-2xl mx-auto mt-8 text-center">
      <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-gray-600 border-t-indigo-500" />
      <p className="mt-4 text-gray-400">
        Planning, generating, reviewing, and documenting your project — this can take a minute or two.
      </p>
    </div>
  );
}