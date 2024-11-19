import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import IntroPage from "./IntroPage";
import ItemsPage from "./ItemsPage";
import FridgeLog from "./FridgeLog";

const App = () => {
  return (
    <Router>
      <Routes>
        {/* IntroPage */}
        <Route path="/" element={<IntroPage />} />

        {/* ItemsPage */}
        <Route path="/items" element={<ItemsPage />} />

        {/* FridgeLog */}
        <Route path="/fridgelog" element={<FridgeLog />} />
      </Routes>
    </Router>
  );
};

export default App;
