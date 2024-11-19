import React from "react";
import { useNavigate } from "react-router-dom";
import logo from "./Fridge_logo.png";

const IntroPage = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-between h-screen bg-white pb-40">
      <div className="flex flex-col items-center mt-12">
        <img src={logo} alt="Logo" className="h-64 mb-2" />
        <h1 className="text-6xl font-bold text-[#285D85] font-patua mb-1">
          ExpiryPal
        </h1>
        <p className="text-[#285D85] font-poppins text-xl font-bold">
          stay fresh, stay cool
        </p>
      </div>
      <button
        onClick={() => navigate("/items")}
        className="bg-[#285D85] text-white font-poppins text-2xl py-5 px-12 rounded-lg shadow-md hover:bg-[#214a68] transition duration-200"
      >
        Tap to Connect
      </button>
    </div>
  );
};

export default IntroPage;
