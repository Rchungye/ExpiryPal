import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getFridgeLog } from "../services/fridge"; // Import API function
import { getUserByAuthToken, updateUsername } from "../services/user"; // Import API function

const Log = () => {
  const navigate = useNavigate();
  const [logs, setLogs] = useState([]); //Store fetched logs
  const [loading, setLoading] = useState(true); //Track loading state
  const [username, setUsername] = useState(""); // Store username
  const [isEditing, setIsEditing] = useState(false); // Track edit state
  const fridgeId = 1; // Replace with dynamic fridge ID if necessary  

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [logResponse, userResponse] = await Promise.all([
          getFridgeLog(fridgeId),
          getUserByAuthToken(),
        ]);
        console.log("userResponse:", userResponse.data.username);
        const { logs } = logResponse.data.payload;
        setLogs(logs);

        const  username  = userResponse.data.username;
        setUsername(username);
      } catch (error) {
        console.error("Failed to fetch data:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [fridgeId]);

   // Handle username edit submission
   const handleUsernameUpdate = async () => {
    try {
      const response = await updateUsername(username); // Update username in the backend
      console.log("Username updated:", response);
      setIsEditing(false); // Exit edit mode
    } catch (error) {
      console.error("Failed to update username:", error);
    }
  };

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
            {isEditing ? (
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="border-b border-gray-400 focus:outline-none"
              />
            ) : (
              <span className="font-bold text-[#285D85]">{username}</span>
            )}
            <span
              className="text-[#285D85] ml-1 cursor-pointer"
              onClick={() => (isEditing ? handleUsernameUpdate() : setIsEditing(true))}
            >
              {isEditing ? "✓" : "✎"}
            </span>
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
