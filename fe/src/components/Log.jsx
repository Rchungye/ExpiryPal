import React from "react";
import { useNavigate } from "react-router-dom";

const Log = () => {
  const navigate = useNavigate();

  const logs = [
    { id: 1, user: "Petar2", action: 'changed item1 to "CocaCola"' },
    { id: 2, user: "Petar2", action: "changed item1 expiration date" },
    { id: 3, user: "SleepyStudent", action: 'changed item2 to "Milk"' },
    { id: 4, user: "SleepyStudent", action: "changed item2 expiration date" },
    { id: 5, user: "Bingo", action: "changed item 5 expiration date" },
    { id: 6, user: "Siri", action: "changed item 3 expiration date" },
  ];

  return (
    <div className="bg-gray-100 min-h-screen font-roboto">
      <header className="bg-[#285D85] text-white p-4 relative flex items-center">
        <button
          onClick={() => navigate("/fridge/groceries")}
          className="absolute left-4 text-3xl cursor-pointer"
        >
          ←
        </button>
        <h1 className="text-3xl mx-auto">FRIDGE LOG</h1>
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
          {logs.map((log) => (
            <div
              key={log.id}
              className="bg-white p-3 rounded shadow text-sm text-gray-700"
            >
              <span className="font-bold text-[#285D85]">{log.user}</span>{" "}
              {log.action}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Log;
