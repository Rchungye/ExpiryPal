import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import Swal from "sweetalert2";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBell } from "@fortawesome/free-solid-svg-icons";
import {
  getNotificationPreferences,
  saveNotificationPreferences,
} from "../services/notificationService";

const NavBar = ({ onBackToItems }) => {
  const [expirationDays, setExpirationDays] = useState(3);
  const [unusedDays, setUnusedDays] = useState(7);
  const fridgeId = 1; //PLACEHOLDER FRIDGE

  useEffect(() => {
    // etch current notification preferences from the backend
    const fetchPreferences = async () => {
      try {
        const response = await getNotificationPreferences(fridgeId);
        const preferences = response.data;

        if (preferences) {
          setExpirationDays(preferences.expiration || 3);
          setUnusedDays(preferences.unusedItem || 7);
        } else {
          console.log("No preferences found for this fridge.");
        }
      } catch (error) {
        console.error("Failed to fetch notification preferences:", error.message);
      }
    };

    fetchPreferences();
  }, [fridgeId]);

  const handleSaveChanges = async () => {
    const payload = {
      expiration: expirationDays,
      unusedItem: unusedDays,
      fridge_id: fridgeId,
    };

    try {
      await saveNotificationPreferences(payload); //Save preferences to backend
      Swal.fire({
        title: "Success!",
        text: "Notification changes saved!",
        icon: "success",
        confirmButtonColor: "#285D85",
      });
    } catch (error) {
      Swal.fire({
        title: "Error",
        text: "Failed to save changes.",
        icon: "error",
        confirmButtonColor: "#285D85",
      });
    }
  };

  return (
    <div className="bg-gray-100 min-h-screen font-roboto sliding-menu">
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
          <FontAwesomeIcon 
            icon={faBell} 
            className="h-8 text-[#285D85]"
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
            value={expirationDays}
            onChange={(e) => setExpirationDays(parseInt(e.target.value, 10))}
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
            value={unusedDays}
            onChange={(e) => setUnusedDays(parseInt(e.target.value, 10))}
          />
          days.
        </p>
      </div>

      {/* Save Changes Button */}
      <div className="flex justify-center mt-6">
        <button
          className="bg-[#285D85] text-white font-poppins text-xl py-4 px-8 rounded-lg shadow-md hover:bg-[#214a68] transition duration-200"
          onClick={handleSaveChanges}
        >
          Save changes
        </button>
      </div>

      {/* Fridge Log Section */}
      <div className="mt-8 text-center">
        <h3 className="text-blue-main font-bold mb-8">View the Fridge Log</h3>
        <Link
          to="/fridge/log"
          className="log-button bg-[#285D85] text-white font-poppins text-xl py-4 px-8 rounded-lg shadow-md hover:bg-[#214a68] transition duration-200"
        >
          Fridge Log
        </Link>
      </div>
    </div>
  );
};

NavBar.propTypes = {
  onBackToItems: PropTypes.func.isRequired,
};

export default NavBar;