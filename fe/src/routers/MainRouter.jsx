import { Routes, Route } from "react-router-dom";
import Welcome from "../components/Welcome";
import Groceries from "../components/Groceries";
import Item from "../components/Item";
import Log from "../components/Log";

const MainRouter = () => {
    return (
        <Routes>
            <Route path="/" element={<Welcome />} />
            <Route path="/fridge/groceries" element={<Groceries />} />
            <Route path="/fridge/item/:id" element={<Item />} />
            <Route path="/fridge/log" element={<Log />} />
        </Routes>
    );
};

export default MainRouter;
