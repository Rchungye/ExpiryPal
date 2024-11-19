import React from 'react';
import { Link } from "react-router-dom";

const NavBar = ({ onBackToItems }) => {
  return (
    <div className="bg-gray-100 min-h-screen font-roboto">
      {/* Header */}
      <header className="bg-blue-main text-white flex justify-between items-center p-4 relative">
        <h1 className="text-3xl mx-auto">MENU</h1>
        <button onClick={onBackToItems} className="absolute right-4 text-6xl">
          ×
        </button>
      </header>

      {/* Notification Settings */}
      <div className="p-4 text-center">
        <h2 className="text-xl font-bold text-blue-main mb-2">
          Notification Settings
        </h2>
        <div className="flex justify-center">
          <img
            src="https://img.icons8.com/ios-filled/50/285D85/bell.png"
            alt="Notification Icon"
            className="h-8"
          />
        </div>
      </div>

      {/* Expiration Notification */}
      <div className="bg-white p-4 mt-4 shadow ml-4 mr-4 rounded">
        <h3 className="font-bold text-lg text-gray-800">Expiration:</h3>
        <p className="text-sm text-gray-700">
          Notify me
          <input
            type="number"
            className="mx-2 border rounded px-2 py-1 text-center w-12"
            defaultValue={3}
          />
          days before expiration.
        </p>
      </div>

      {/* Unused Item Notification */}
      <div className="bg-white p-4 mt-4 shadow ml-4 mr-4 rounded">
        <h3 className="font-bold text-lg text-gray-800">Unused item:</h3>
        <p className="text-sm text-gray-700">
          Notify me if the item has not been used in
          <input
            type="number"
            className="mx-2 border rounded px-2 py-1 text-center w-12"
            defaultValue={7}
          />
          days.
        </p>
      </div>

      {/* Save Changes Button */}
      <div className="flex justify-center mt-6">
        <button className="bg-[#285D85] text-white font-poppins text-xl py-4 px-8 rounded-lg shadow-md hover:bg-[#214a68] transition duration-200">
          Save changes
        </button>
      </div>

      {/* Fridge Log Section */}
      <div className="mt-8 text-center">
        <h3 className="text-blue-main font-bold mb-8">View the Fridge Log</h3>
        <Link
          to="/fridge/log"
          className="bg-[#285D85] text-white font-poppins text-xl py-4 px-8 rounded-lg shadow-md hover:bg-[#214a68] transition duration-200"
        >
          Fridge Log
        </Link>
      </div>
    </div>
  );
};

export default NavBar;
