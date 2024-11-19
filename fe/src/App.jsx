import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import IntroPage from "./IntroPage";
import ItemsPage from "./ItemsPage";
import FridgeLog from "./FridgeLog";
import SingleItem from "./SingleItem";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<IntroPage />} />
        <Route path="/items" element={<ItemsPage />} />
        <Route path="/fridgelog" element={<FridgeLog />} />
        <Route path="/item/:id" element={<SingleItem />} />
      </Routes>
    </Router>
  );
};

export default App;
