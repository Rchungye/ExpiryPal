import React, { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import logo from "../assets/Fridge_logo.png";

function Welcome() {
  const navigate = useNavigate();
  const videoRef = useRef(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [error, setError] = useState(null);

  const startCamera = async () => {
    try {
      // Request access to the camera
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" }, // Rear camera
      });

      // Attach the video stream to the video element
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }

      setCameraActive(true); // Show the camera feed
    } catch (err) {
      console.error("Error accessing the camera:", err);
      setError("Unable to access the camera. Please check your permissions.");
    }
  };

  const stopCamera = () => {
    // Stop the camera
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();
      tracks.forEach((track) => track.stop()); // Stop all tracks
    }

    setCameraActive(false);
  };

  return (
    <div className="flex flex-col items-center justify-between h-screen bg-white pb-40">
      {/* Header */}
      <div className="flex flex-col items-center mt-12">
        <img src={logo} alt="Logo" className="h-64 mb-2" />
        <h1 className="text-6xl font-bold text-[#285D85] font-patua mb-1">
          ExpiryPal
        </h1>
        <p className="text-[#285D85] font-poppins text-xl font-bold">
          Stay fresh, Stay cool.
        </p>
      </div>

      {/* Camera Feed or Button */}
      {!cameraActive ? (
        <button
          onClick={startCamera}
          className="bg-[#285D85] text-white font-poppins text-2xl py-5 px-12 rounded-lg shadow-md hover:bg-[#214a68] transition duration-200"
        >
          Tap to Scan QR Code
        </button>
      ) : (
        <div className="flex flex-col items-center">
          {/* Video feed */}
          <video
            ref={videoRef}
            className="w-full max-w-md rounded-md shadow-lg"
            style={{ border: "2px solid #285D85" }}
          />

          {/* Cancel Button */}
          <button
            onClick={stopCamera}
            className="bg-red-500 mt-4 text-white font-poppins text-xl py-3 px-8 rounded-lg shadow-md hover:bg-red-700 transition duration-200"
          >
            Cancel
          </button>
        </div>
      )}

      {/* Error Message */}
      {error && <p className="text-red-500 mt-4">{error}</p>}
    </div>
  );
}

export default Welcome;
