import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getFridgeLog } from "../services/api"; // Import API function

const Log = () => {
  const navigate = useNavigate();
  const [logs, setLogs] = useState([]); //Store fetched logs
  const [loading, setLoading] = useState(true); //Track loading state
  const fridgeId = 1; //Replace with dynamic fridge ID if necessary

  useEffect(() => {
    //Fetch logs from the backend
    const fetchLogs = async () => {
      try {
        const response = await getFridgeLog(fridgeId);
        const { logs } = response.data.payload; //Extract logs from payload
        setLogs(logs);
      } catch (error) {
        console.error("Failed to fetch fridge logs:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchLogs();
  }, [fridgeId]);

  if (loading) {
    return <p className="text-center text-gray-500">Loading logs...</p>;
  }
  return (
    <div className="bg-gray-100 min-h-screen font-roboto">
      <header className="bg-blue-main text-white sticky top-0 z-10">
        <div className="max-w-[1024px] flex justify-between items-center p-4 relative mx-auto ">
          <button
            onClick={() => navigate("/fridge/groceries")}
            className="absolute left-4 text-3xl cursor-pointer"
          >
            ←
          </button>
          <h1 className="text-3xl mx-auto">FRIDGE LOG</h1>
        </div>
      </header>

      {/* Unique ID Section */}
      <div className="max-w-[512px] mx-auto p-4">
        <div className="p-4">
          <p className="text-sm text-gray-700">
            Your unique ID:{" "}
            <span className="font-bold text-[#285D85]">Petar2</span>
            <span className="text-[#285D85] ml-1 cursor-pointer">✎</span>
          </p>
        </div>
        {/* Log List */}
        <div className="p-4 space-y-4">
          {logs.map((log, index) => (
            <div
              key={index}
              className="bg-white p-3 rounded shadow text-sm text-gray-700"
            >
              {log}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Log;
