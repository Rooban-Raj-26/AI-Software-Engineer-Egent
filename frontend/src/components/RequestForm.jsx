export default function RequestForm({ userRequest, setUserRequest, onSubmit, disabled }) {
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit();
      }}
      className="w-full max-w-2xl mx-auto"
    >
      <label className="block text-sm font-medium text-gray-300 mb-2">
        Describe the software you want built
      </label>
      <textarea
        value={userRequest}
        onChange={(e) => setUserRequest(e.target.value)}
        rows={4}
        placeholder="Build a simple to-do list REST API with FastAPI and SQLite."
        className="w-full rounded-lg bg-gray-800 border border-gray-700 text-gray-100 p-4 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
        disabled={disabled}
      />
      <button
        type="submit"
        disabled={disabled || !userRequest.trim()}
        className="mt-4 w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-700 disabled:cursor-not-allowed text-white font-medium py-3 rounded-lg transition-colors"
      >
        {disabled ? "Building..." : "Run AI Software Engineer Agent"}
      </button>
    </form>
  );
}