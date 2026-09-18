import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

interface LocalizedText {
  en?: string;
  ar?: string;
}

interface Curriculum {
  id: string;
  title: LocalizedText;
  description: LocalizedText;
  version: string;
}

export const CurriculumBrowser: React.FC = () => {
  const [curricula, setCurricula] = useState<Curriculum[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCurricula = async () => {
      try {
        const token = localStorage.getItem("token");
        const res = await fetch("http://localhost:8000/api/v1/curricula", {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });

        if (!res.ok) {
          throw new Error("Failed to load curricula");
        }

        const data = await res.json();
        setCurricula(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCurricula();
  }, []);

  if (loading) {
    return <div className="p-8 text-center text-gray-500">Loading curriculum...</div>;
  }

  if (error) {
    return <div className="p-8 text-center text-red-500">{error}</div>;
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Curriculum Browser</h2>
      <p className="text-gray-600">Browse available educational curricula and learning objectives.</p>
      
      {curricula.length === 0 ? (
        <div className="p-6 bg-gray-50 rounded-xl border border-gray-100 text-center text-gray-500">
          No curricula found. Please seed the database.
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {curricula.map((curr) => (
            <div key={curr.id} className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {curr.title.en || curr.title.ar}
              </h3>
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                {curr.description?.en || curr.description?.ar || "No description provided."}
              </p>
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium bg-blue-50 text-blue-700 px-2.5 py-1 rounded-full">
                  v{curr.version}
                </span>
                <button className="text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors">
                  View Details &rarr;
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
