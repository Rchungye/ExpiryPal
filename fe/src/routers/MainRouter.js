    import React from "react";
    import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
    import Welcome from "../components/Welcome";
    import Groceries from "../components/Groceries";
    import Item from "../components/Item";
    import Log from "../components/Log";

    const MainRouter = () => {
        return (
            <Router>
                <Routes>
                    <Route path="/" element={<Welcome />} />
                    <Route path="fridge/groceries" element={<Groceries />} />
                    <Route path="fridge/item" element={<Item />} />
                    <Route path="fridge/log" element={<Log />} />
                </Routes>
            </Router>
        );
    };

    export default MainRouter;