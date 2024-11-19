import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import items from "./ItemsData";

const SingleItem = () => {
  const { id } = useParams(); //Get the item ID from the URL
  const navigate = useNavigate();
  const item = items.find((item) => item.id === parseInt(id)); //Find the item by ID

  const [expirationDate, setExpirationDate] = useState(item?.date || "");

  if (!item) {
    return <div>Item not found</div>; //Make solution for no item
  }

  const handleSave = () => {
    alert("Changes saved!");
  };

  const handleRemove = () => {
    alert("Item removed!");
    navigate("/items");
  };

  return (
    <div className="bg-gray-100 min-h-screen font-roboto">
      {/* Header */}
      <header className="bg-blue-main text-white p-4 relative flex items-center">
        <button
          onClick={() => navigate("/items")}
          className="absolute left-4 text-3xl cursor-pointer"
        >
          ←
        </button>

        <h1 className="text-3xl mx-auto">ITEM</h1>
      </header>

      {/* Content */}
      <div className="p-4 text-center">
        <div className="flex justify-center items-center mb-4">
          <h2 className="text-2xl font-bold">{item.name}</h2>
          <span className="text-blue-main text-xl ml-2 cursor-pointer">✎</span>
        </div>

        {/* Item Image */}
        <div
          className={`bg-white rounded-lg shadow p-4 relative inline-block ${
            item.expired ? "border border-red-400" : ""
          }`}
        >
          <img
            src={item.image}
            alt={item.name}
            className="w-40 h-40 object-contain mx-auto mb-3"
          />

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
        </div>

        {/* Expiration Status */}
        {item.warning === "red" && (
          <p className="text-red-500 mt-2">Item has expired!</p>
        )}
        {item.warning === "orange" && (
          <p className="text-orange-500 mt-2">Item is about to expire</p>
        )}
        {item.warning === "blue" && (
          <p className="text-blue-500 mt-2">
            Item has not been used in a while
          </p>
        )}

        {/* Dates */}
        <div className="mt-6">
          <div className="mb-4">
            <label className="block text-gray-700 font-bold mb-2">
              Date added:
            </label>
            <input
              type="text"
              value={item.date}
              readOnly
              className=" cursor-not-allowed bg-gray-100 text-gray-500 border rounded px-3 py-2 text-center w-50"
            />
            <p className="text-sm text-gray-500">(8 days ago)</p>
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 font-bold mb-2">
              Expiration date:
            </label>
            <input
              type="date"
              value={expirationDate}
              onChange={(e) => setExpirationDate(e.target.value)}
              className="border rounded px-3 py-2 text-center w-50"
            />
            <p className="text-sm text-gray-500">(in 2 days)</p>
          </div>
        </div>

        {/* Buttons */}
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
  );
};

export default SingleItem;
