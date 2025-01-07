import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import QRScanner from "./scanner";
import logo from "../assets/Fridge_logo.png";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Modal from "@mui/material/Modal";
import { linkUserToFridge, checkUserLink } from "../services/api";

const modalStyle = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: "90%",
  maxWidth: 400,
  bgcolor: "background.paper",
  boxShadow: 24,
  p: 4,
  borderRadius: 2,
};

function Welcome() {
  const navigate = useNavigate();
  const [openModal, setOpenModal] = useState(false);
  const [debugText, setDebugText] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [isLinked, setIsLinked] = useState(false);

  useEffect(() => {
    const checkAuthToken = async () => {
      try {
        const response = await checkUserLink();
        console.log("isLinked:", response);
        if (response.status === 200) {
          navigate("/fridge/groceries");
        }
      } catch (error) {
        console.error("Error verifying user link:", error);
      }
    };
    checkAuthToken();
  }, [navigate]);

  const handleOpenModal = () => {
    setOpenModal(true);
  };

  const handleCloseModal = () => {
    setOpenModal(false);
    setDebugText("");
    setIsProcessing(false);
    setIsLinked(false);
  };

  let lastScannedCode = null;

  const handleScanResult = async (result) => {
    if (!result || isProcessing || isLinked) return;
  
    const urlPattern = /[?&]code=([^&]+)/;
    const match = result.match(urlPattern);
    const code = match ? match[1] : result;
  
    if (code === lastScannedCode) {
      console.log("Duplicate scan detected, skipping...");
      return;
    }
  
    lastScannedCode = code;
    setIsProcessing(true);
  
    try {
      const response = await linkUserToFridge(code);
      if (response.status === 200) {
        setIsLinked(true);
        handleCloseModal();
        navigate("/fridge/groceries");
      } else {
        alert(response.data.error || "Failed to link with fridge");
      }
    } catch (error) {
      console.error("Error linking fridge:", error);
    } finally {
      setIsProcessing(false);
    }
  };
  
  const handleScanError = (error) => {
    // Filtrar NotFoundException para no loguear continuamente
    if (error.name !== "NotFoundException") {
      console.error("QR Scan Error:", error);
      setDebugText("Error scanning QR code. Please try again.");
    }
  };
  

  return (
    <div className="flex flex-col items-center justify-between h-screen bg-white pb-40">
      <div className="flex flex-col items-center mt-12">
        <img src={logo} alt="Logo" className="h-64 mb-2" />
        <h1 className="text-6xl font-bold text-[#285D85] font-patua mb-1">
          ExpiryPal
        </h1>
        <p className="text-[#285D85] font-poppins text-xl font-bold">
          Stay fresh, Stay cool.
        </p>
      </div>

      <button
        onClick={handleOpenModal}
        className="bg-[#285D85] text-white font-poppins text-2xl py-5 px-12 rounded-lg shadow-md hover:bg-[#214a68] transition duration-200"
      >
        Tap to Connect
      </button>

      <Modal
        open={openModal}
        onClose={handleCloseModal}
        aria-labelledby="qr-scanner-modal"
      >
        <Box sx={modalStyle}>
          <Typography
            id="modal-modal-title"
            variant="h6"
            component="h2"
            className="mb-4 text-center"
          >
            Scan Fridge QR Code
          </Typography>

          <div className="w-full">
            {openModal && (
              <QRScanner
              onScan={handleScanResult}
              onError={handleScanError}
            />
            
            )}
            {debugText && (
              <p className="mt-2 text-sm text-gray-600 text-center break-words">
                {debugText}
              </p>
            )}
          </div>

          <Button
            onClick={handleCloseModal}
            variant="contained"
            className="mt-4 bg-[#285D85]"
            fullWidth
          >
            Cancel
          </Button>
        </Box>
      </Modal>
    </div>
  );
}

export default Welcome;
