import { useState, useEffect } from "react";
import "./App.css";

interface ExampleResponse {
  message?: string;
  timestamp: string;
  status: string;
  received_data?: {
    test: string;
    value: number;
  };
}

function App() {
  const [data, setData] = useState<ExampleResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [postResponse, setPostResponse] = useState<ExampleResponse | null>(
    null
  );

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("/api/example");
        const jsonData = await response.json();
        setData(jsonData);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      }
    };

    fetchData();
  }, []);

  const handlePostTest = async () => {
    try {
      const response = await fetch("/api/example", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ test: "data", value: 123 }),
      });
      const jsonData = await response.json();
      setPostResponse(jsonData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    }
  };

  return (
    <div className="app">
      <h1>React + Flask Example</h1>
      {error && <div className="error">{error}</div>}

      <div className="section">
        <h2>GET Response</h2>
        {data && (
          <div className="data">
            <p>Message: {data.message}</p>
            <p>Timestamp: {data.timestamp}</p>
            <p>Status: {data.status}</p>
          </div>
        )}
      </div>

      <div className="section">
        <h2>POST Test</h2>
        <button onClick={handlePostTest} className="test-button">
          Test POST Request
        </button>
        {postResponse && (
          <div className="data">
            <p>Received Data: {JSON.stringify(postResponse.received_data)}</p>
            <p>Timestamp: {postResponse.timestamp}</p>
            <p>Status: {postResponse.status}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
