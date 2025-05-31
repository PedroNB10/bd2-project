import { useState, useEffect } from "react";

interface Rocket {
  id: string;
  name: string;
  height: number;
  mass: number;
  cost_per_launch: number;
}

export function Rockets() {
  const [rockets, setRockets] = useState<Rocket[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRockets = async () => {
      try {
        const response = await fetch("/api/rockets");
        if (!response.ok) {
          throw new Error("Failed to fetch rockets");
        }
        const data = await response.json();
        setRockets(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchRockets();
  }, []);

  if (loading) {
    return <div className="loading">Loading rockets...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="rockets-container">
      <h2>SpaceX Rockets</h2>
      <div className="rockets-grid">
        {rockets.map((rocket) => (
          <div key={rocket.id} className="rocket-card">
            <h3>{rocket.name}</h3>
            <div className="rocket-details">
              <p>
                <strong>Height:</strong> {rocket.height} meters
              </p>
              <p>
                <strong>Mass:</strong> {rocket.mass} kg
              </p>
              <p>
                <strong>Cost per Launch:</strong> $
                {rocket.cost_per_launch.toLocaleString()}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
