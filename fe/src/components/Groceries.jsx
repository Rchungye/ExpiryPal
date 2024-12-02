import React, { useState } from "react";
import NavBar from "./NavBar";
import ItemModal from "./ItemModal";
import itemsData from "../assets/jsons/items.json";

function Groceries() {
  const [navBarOpen, setNavBarOpen] = useState(false);
  const [modalOpen, setModalOpen] = useState(false); //Controls modal visibility
  const [selectedItem, setSelectedItem] = useState(null); //Stores the item to display via modal
  const [items, setItems] = useState(itemsData.items); //Managing the list of items

  const toggleNavBar = () => {
    setNavBarOpen((prev) => !prev);
  };

  //Sets the selected item and opens the modal
  const handleItemClick = (item) => {
    setSelectedItem(item);
    setModalOpen(true);
  };

  //Handle item updates
  const handleUpdateItem = (updatedItem) => {
    setItems((prevItems) =>
      prevItems.map((item) => (item.id === updatedItem.id ? updatedItem : item))
    );
  };
  //Handle item removal
  const handleRemoveItem = (itemId) => {
    setItems((prevItems) => prevItems.filter((item) => item.id !== itemId));
  };

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

  return (
    <div className="bg-gray-100 min-h-screen font-roboto relative overflow-hidden">
      <header className="bg-blue-main text-white flex justify-between items-center p-4">
        <h1 className="text-3xl">ALL ITEMS</h1>
        <button onClick={toggleNavBar} className="text-3xl cursor-pointer">
          {navBarOpen ? "×" : "☰"}
        </button>
      </header>

      <div className="grid grid-cols-2 gap-4 p-4">
        {items.map((item) => {
          //Calculate daysLeft and expired dynamically
          const daysLeft = calculateDaysLeft(item.dateExp);
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
          //blue warning left to calculate

          return (
            <div
              key={item.id}
              onClick={() => handleItemClick(item)}
              className={`bg-white rounded-lg shadow p-4 relative text-center ${
                expired
                  ? "border border-red-400"
                  : warning === "orange"
                  ? "border border-orange-400"
                  : ""
              } cursor-pointer`}
            >
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
              {warning === "orange" && (
                <div className="absolute top-2 right-2 bg-orange-500 text-white text-xs font-bold px-2 py-1 rounded">
                  !
                </div>
              )}
              {/* 'blue' warning cannot be calculated now */}

              <img
                src={item.image}
                alt={item.name}
                className="w-full h-24 object-contain rounded mb-3"
              />
              <p className="font-semibold">{item.name}</p>

              <span className="text-gray-500 text-sm block">
                {item.dateExp ? item.dateExp : "Expiration N/A"}
              </span>

              <span
                className={`text-sm font-semibold ${
                  expired
                    ? "text-red-600"
                    : warning === "orange"
                    ? "text-orange-600"
                    : "text-gray-600"
                }`}
              >
                {daysLeft !== null
                  ? daysLeft === 0
                    ? "Expires today"
                    : `${Math.abs(daysLeft)} days ${expired ? "ago" : "left"}`
                  : "N/A"}
              </span>
            </div>
          );
        })}
      </div>

      {/* Sliding NavBar */}
      <div
        className={`fixed top-0 right-0 h-full w-full bg-white transform transition-transform duration-300 ease-in-out ${
          navBarOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <NavBar onBackToItems={toggleNavBar} />
      </div>

      {/* Item Modal */}
      {modalOpen && (
        <ItemModal
          item={selectedItem}
          onClose={() => setModalOpen(false)}
          onUpdateItem={handleUpdateItem}
          onRemoveItem={handleRemoveItem}
        />
      )}
    </div>
  );
}

export default Groceries;
