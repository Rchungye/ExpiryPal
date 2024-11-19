import React, { useState } from "react";
import NavBar from "./NavBar";
import itemsData from '../assets/jsons/items.json';
import { useNavigate } from "react-router-dom";

function Groceries() {
  const [navBarOpen, setNavBarOpen] = useState(false);
  const navigate = useNavigate();

  const toggleNavBar = () => {
    setNavBarOpen((prev) => !prev);
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
        {itemsData.items.map((item) => (
          <div key={item.id} onClick={() => navigate(`/fridge/item/${item.id}`)}
            className={`bg-white rounded-lg shadow p-4 relative text-center ${item.expired ? "border border-red-400" : ""} cursor-pointer`}>
            {item.isNew && (
              <div className="absolute top-2 left-2 bg-green-500 text-white text-xs font-bold px-2 py-1 rounded">
                NEW
              </div>
            )}
            <img src={item.image} alt={item.name}
              className="w-full h-24 object-contain rounded mb-3" />
            <p className="font-semibold">{item.name}</p>
            <span className="text-gray-500 text-sm block">{item.date}</span>
            <span
              className={`text-sm font-semibold ${item.expired ? "text-red-600" : "text-gray-600"
                }`}
            >
              {item.daysLeft} days left
            </span>
          </div>
        ))}
      </div>

      {/* Sliding NavBar */}
      <div className={
        `fixed top-0 right-0 h-full w-full bg-white transform transition-transform duration-300 ease-in-out ${navBarOpen ? "translate-x-0" : "translate-x-full"}`
      }>
        <NavBar onBackToItems={toggleNavBar} />
      </div>
    </div>
  );
}

export default Groceries;
