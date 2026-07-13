import { useState } from "react";
import RequestForm from "./components/RequestForm";
import LoadingState from "./components/LoadingState";
import ResultsView from "./components/ResultsView";

const API_BASE_URL = "http://127.0.0.1:8000";

export default function App() {
  const [userRequest, setUserRequest] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function handleSubmit() {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/agents/plan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_request: userRequest }),
      });

      if (!response.ok) {
        const errBody = await response.json();
        throw new Error(errBody.detail || "Request failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 py-12 px-4">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold">AI Software Engineer Agent</h1>
        <p className="text-gray-400 mt-2">
          Autonomous planning, code generation, review, and documentation.
        </p>
      </div>

      <RequestForm
        userRequest={userRequest}
        setUserRequest={setUserRequest}
        onSubmit={handleSubmit}
        disabled={loading}
      />

      {loading && <LoadingState />}

      {error && (
        <div className="w-full max-w-2xl mx-auto mt-6 bg-red-900/40 border border-red-700 text-red-300 rounded-lg p-4 text-sm">
          {error}
        </div>
      )}

      {result && !loading && <ResultsView result={result} />}
    </div>
  );
}