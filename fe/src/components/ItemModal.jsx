import React, { useState, useEffect, useRef } from "react";
import Swal from "sweetalert2";

import PropTypes from "prop-types";
import { updateItemName, updateItemExpirationDate } from "../services/api"; //API functions

function ItemModal({ item, onClose, onUpdateItem, onRemoveItem }) {
  const [expirationDate, setExpirationDate] = useState(item.dateExp || ""); //edit expiration date

  const [itemName, setItemName] = useState(item.name || "Item" + item.id); //edit item name
  const [isEditingName, setIsEditingName] = useState(false); //is the name being edited
  const modalRef = useRef();

  //Function to calculate days left
  const calculateDaysLeft = (expDate) => {
    if (!expDate) {
      return null;
    }

    const [day, month, year] = expDate.split("/").map(Number);
    const expiration = new Date(2000 + year, month - 1, day);
    const today = new Date();

    expiration.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);

    const diffTime = expiration - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    return diffDays;
  };
  //Function to check if the item was added today
  const isItemNew = (dateAdded) => {
    if (!dateAdded) {
      return false;
    }
    const [day, month, year] = dateAdded.split("/").map(Number);
    const addedDate = new Date(2000 + year, month - 1, day);
    const today = new Date();

    addedDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);

    return addedDate.getTime() === today.getTime();
  };

  //Calculate daysLeft and expired dynamically
  const daysLeft = calculateDaysLeft(expirationDate);
  let expired = daysLeft !== null ? daysLeft < 0 : false;
  //Calculate isNew
  const isNew = isItemNew(item.dateAdded);

  //Determine warning
  let warning = "";
  if (expired) {
    warning = "red";
  } else if (daysLeft !== null && daysLeft >= 0 && daysLeft <= 2) {
    warning = "orange";
  }

  //Close modal on click outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        modalRef.current &&
        !modalRef.current.contains(event.target) &&
        !event.target.classList.contains("edit-icon")
      ) {
        onClose();
      }
    };
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [onClose]);

  const formatDateToISO = (ddmmyy) => {
    if (!ddmmyy) {
      return "";
    }

    const [day, month, year] = ddmmyy.split("/");

    return `20${year}-${month}-${day}`;
  };

  const formatDateToDDMMYY = (isoDate) => {
    if (!isoDate) {
      return "";
    }

    const [year, month, day] = isoDate.split("-");
    return `${day}/${month}/${year.slice(-2)}`;
  };
  const handleDateChange = (e) => {
    const newDate = e.target.value;
    const formattedDate = formatDateToDDMMYY(newDate);
    setExpirationDate(formattedDate);
  };

  const handleNameClick = () => {
    setIsEditingName(true);
  };

  const handleNameChange = (e) => {
    setItemName(e.target.value);
  };
  const handleNameBlur = () => {
    setIsEditingName(false);
  };

  const handleSave = async () => {
    try {
      //Update the item name in the database
      await updateItemName(item.id, 1, itemName); //PLACEHOLDER USER
      //Update the expiration date in the database
      console.log(
        "Sending expiration date to API:",
        formatDateToISO(expirationDate)
      );
      await updateItemExpirationDate(
        item.id,
        1, //PLACEHOLDER USER
        formatDateToISO(expirationDate)
      );

      //Update the item data
      const updatedItem = {
        ...item,
        name: itemName,
        dateExp: expirationDate,
      };
      //Call the update function
      onUpdateItem(updatedItem);

      Swal.fire({
        title: "Success!",
        text: "Changes saved!",
        icon: "success",
        confirmButtonColor: "#285D85",
      }).then(() => {
        onClose();
      });
    } catch (error) {
      console.error("Failed to update item:", error);
      Swal.fire({
        title: "Error",
        text: "Failed to save changes.",
        icon: "error",
        confirmButtonColor: "#285D85",
      });
    }
  };

  const handleRemove = () => {
    //Call the remove function
    onRemoveItem(item.id);
    Swal.fire({
      title: "Success!",
      text: "Item removed!",
      icon: "success",
      confirmButtonColor: "#285D85",
    }).then(() => {
      onClose();
    });
  };

  //Determine warning message
  let warningMessage = "";
  if (warning === "red") {
    warningMessage = "Item has expired!";
  } else if (warning === "orange") {
    warningMessage =
      daysLeft === 0 ? "Item expires today!" : "Item is about to expire";
  }
  //Function to calculate days since the item was added
  const calculateDaysSinceAdded = (dateAdded) => {
    if (!dateAdded) {
      return null;
    }
    const [day, month, year] = dateAdded.split("/").map(Number);
    const addedDate = new Date(2000 + year, month - 1, day);
    const today = new Date();

    addedDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);

    const diffTime = today - addedDate;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    return diffDays;
  };

  const daysSinceAdded = calculateDaysSinceAdded(item.dateAdded);

  //To dermine if blue warning should be
  const blueWarning = daysSinceAdded !== null && daysSinceAdded > 5;
  //Blue warning message
  let blueWarningMessage = "";
  if (blueWarning) {
    blueWarningMessage = `Item has not been used in ${daysSinceAdded} days`;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div
        ref={modalRef}
        className="bg-white rounded-lg shadow-lg w-11/12 md:w-1/2 lg:w-1/3 p-6 relative"
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-gray-600 hover:text-gray-800 text-2xl font-bold"
        >
          ×
        </button>

        {/* Content */}
        <div className="text-center">
          <div className="flex justify-center items-center mb-4">
            {isEditingName ? (
              <input
                type="text"
                value={itemName}
                onChange={handleNameChange}
                onBlur={handleNameBlur}
                className="text-2xl font-bold border-b-2 border-gray-300 focus:border-blue-main focus:outline-none"
                autoFocus
              />
            ) : (
              <>
                <h2
                  className="text-2xl font-bold cursor-pointer"
                  onClick={handleNameClick}
                >
                  {itemName}
                </h2>

                <span
                  className="text-blue-main text-xl ml-2 cursor-pointer edit-icon"
                  onClick={handleNameClick}
                >
                  ✎
                </span>
              </>
            )}
          </div>
          {/* Image and Basic Info */}
          <div
            className={`bg-white rounded-lg shadow p-4 relative inline-block ${
              expired
                ? "border border-red-400"
                : warning === "orange"
                ? "border border-orange-400"
                : blueWarning
                ? "border  border-blue-400"
                : ""
            }`}
          >
            <img
              src={item.image}
              alt={itemName}
              className="w-40 h-40 object-contain mx-auto mb-3"
            />

            {/* New Badge */}
            {isNew && (
              <div className="absolute top-2 left-2 bg-green-500 text-white text-xs font-bold px-2 py-1 rounded">
                NEW
              </div>
            )}

            {/* Warning Badges */}
            {warning === "red" && (
              <div className="absolute top-2 right-2 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">
                !
              </div>
            )}
            {warning === "orange" && !expired && (
              <div
                className="absolute top-2 right-2
                     bg-orange-500 text-white text-xs font-bold px-2 py-1 rounded"
              >
                !
              </div>
            )}
            {blueWarning && (
              <div
                className={`absolute ${
                  warning === "red"
                    ? "top-2 right-8"
                    : warning === "orange"
                    ? "top-2 right-8"
                    : "top-2 right-2"
                } bg-blue-500 text-white text-xs font-bold px-2 py-1 rounded`}
              >
                !
              </div>
            )}
          </div>
          {/* Warning Message */}
          {warningMessage && (
            <p className={`mt-2 text-${warning}-600`}>{warningMessage}</p>
          )}
          {blueWarningMessage && (
            <p className={`mt-2 text-blue-600`}>{blueWarningMessage}</p>
          )}
          {/*Item Info */}
          <div className="mt-4">
            <label className="block text-gray-700 font-bold mb-2">
              Date added:
            </label>

            <input
              type="text"
              value={item.dateAdded || "N/A"}
              readOnly
              className="cursor-not-allowed text-gray-500 border rounded px-3 py-2 text-center w-50"
            />
          </div>
          {/* Expiration Date */}
          <div className="mt-6">
            <label className="block text-gray-700 font-bold mb-2">
              Expiration date:
            </label>
            <input
              type="date"
              value={formatDateToISO(expirationDate)}
              onChange={handleDateChange}
              className="border rounded px-3 py-2 text-center w-50"
            />
          </div>
          <p className="text-sm text-gray-500">
            {daysLeft !== null
              ? daysLeft === 0
                ? `(expires today)`
                : daysLeft > 0
                ? `(in ${daysLeft} days)`
                : `(${Math.abs(daysLeft)} days ago)`
              : `(Expiration N/A)`}
          </p>
          {/* Actions */}
          <div className="flex justify-between mt-12">
            <button
              onClick={handleRemove}
              className="bg-red-500 text-white px-6 py-3 rounded-lg shadow-md hover:bg-red-700"
            >
              Remove Item
            </button>
            <button
              onClick={handleSave}
              className="bg-blue-main text-white px-6 py-3 rounded-lg shadow-md hover:bg-blue-800"
            >
              Save changes
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
//Validate component props to catch errors

ItemModal.propTypes = {
  item: PropTypes.object.isRequired,
  onClose: PropTypes.func.isRequired,
  onUpdateItem: PropTypes.func.isRequired,
  onRemoveItem: PropTypes.func.isRequired,
};

export default ItemModal;
