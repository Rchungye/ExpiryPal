import React from 'react'
import { useNavigate } from "react-router-dom";
import itemsData from '../assets/jsons/items.json';

function Item() {

  const navigate = useNavigate();

  return (
    <div className="bg-gray-100 min-h-screen font-roboto relative overflow-hidden">
      {/* Header */}
      <header className="bg-blue-main text-white flex justify-between items-center p-4">
        <button onClick={() => navigate("/fridge/groceries")} className="absolute left-4 text-3xl cursor-pointer">
          ←
        </button>
        <h1 className="text-3xl mx-auto">ITEM</h1>
      </header>

      {/* Items Grid */}
      <div className="grid grid-cols-2 gap-4 p-4">
        {itemsData.items.map((item) => (
          <div key={item.id} className={`bg-white rounded-lg shadow p-4 relative text-center 
            ${item.expired ? "border border-red-400" : ""}`}>
            {/* New Badge */}
            {item.isNew && (
              <div className="absolute top-2 left-2 bg-green-500 text-white text-xs font-bold px-2 py-1 rounded">
                NEW
              </div>
            )}
            {/* Warning Badges */}
            {item.warning === "red" && (
              <div className="absolute top-2 right-2 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">
                !
              </div>
            )}
            {item.warning === "orange" && (
              <div className="absolute top-2 right-2 bg-orange-500 text-white text-xs font-bold px-2 py-1 rounded">
                !
              </div>
            )}
            {item.warning === "blue" && (
              <div className="absolute top-2 right-2 bg-blue-500 text-white text-xs font-bold px-2 py-1 rounded">
                !
              </div>
            )}
            <img src={item.image} alt={item.name} className="w-full h-24 object-contain rounded mb-3" />
            <p className="font-semibold">{item.name}</p>
            <span className="text-gray-500 text-sm block">{item.date}</span>
            <span className={`text-sm font-semibold ${item.expired ? "text-red-600" : "text-gray-600"}`}>
              {item.daysLeft} days left
            </span>
          </div>
        ))}
      </div>

    </div>
  )
}

export default Item