import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { QrReader } from "react-qr-reader";
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
  const qrRef = useRef(null);
  const [stream, setStream] = useState(null);

  // Verifica el auth_token al montar el componente
  useEffect(() => {
    console.log("Welcome mounted, user link check...");
    const checkAuthToken = async () => {
      console.log("Checking auth token...");
      try {
        const response = await checkUserLink(); // Llama al nuevo endpoint
        console.log("Check link response:", response.data);

        if (response.status === 200 && response.data.isLinked) {
          handleCloseModal(); // Detiene la cámara si está abierta
          navigate("/fridge/groceries"); // Redirige al sistema si está vinculado
        }
      } catch (error) {
        console.error("Error verifying user link:", error);
        // No hacemos nada si no está vinculado, simplemente dejamos al usuario escanear el QR
      }
    };

    checkAuthToken();
  }, [navigate]);

  const stopCamera = () => {
    if (stream) {
      const tracks = stream.getTracks();
      tracks.forEach((track) => {
        if (track.readyState === "live") {
          track.stop();
        }
      });
      setStream(null);
    }
  
    const videos = document.getElementsByTagName("video");
    Array.from(videos).forEach((video) => {
      if (video.srcObject) {
        const tracks = video.srcObject.getTracks();
        tracks.forEach((track) => {
          if (track.readyState === "live") {
            track.stop();
          }
        });
        video.srcObject = null;
      }
    });
  };
  

  const handleOpenModal = async () => {
    try {
      // Obtener acceso a la cámara
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" },
      });
      setStream(mediaStream);
      setOpenModal(true);
    } catch (err) {
      console.error("Error accessing camera:", err);
      alert(
        "Camera access is required to scan QR codes. Please enable camera access and try again."
      );
    }
  };

  const handleCloseModal = () => {
    stopCamera();
    setOpenModal(false);
    setDebugText('');
    setIsProcessing(false); // Restablece el procesamiento
    setIsLinked(false); // Reinicia el estado de enlace
  };

  let lastScannedCode = null;

  const handleScan = async (result, error) => {
    if (!result || isProcessing || isLinked) return;
    
    const urlPattern = /[?&]code=([^&]+)/;
    const match = result.text.match(urlPattern);
    let code = match ? match[1] : result.text;

    // this is to prevent duplicate scans
    if (code === lastScannedCode && !isLinked) {
      console.log("Duplicate scan detected, skipping...");
      return;
    }

    lastScannedCode = code; // Almacena el último código procesado
    setIsProcessing(true);
    try {
      if (code && !isLinked) {
        const response = await linkUserToFridge(code);
        console.log("Link user to fridge response:", response);
        
        if (response.status === 200) {
          setIsLinked(true);
          stopCamera();
          handleCloseModal();
          navigate("/fridge/groceries");

        } else {
          alert(response.data.error || "Failed to link with fridge");
        }
      } else {
        alert("Invalid QR code format.");
      }
    } catch (err) {
      console.error("Error linking fridge:", err);
    } finally {
      setIsProcessing(false);
    }
  
    if (error && error.name !== "NotFoundException") {
      console.error("QR Scan Error:", error.message);
      setDebugText("Error scanning QR code. Please try again.");
    }
  };
  

  // Cleanup cuando el componente se desmonta
  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  // Cleanup cuando el modal se cierra
  useEffect(() => {
    if (!openModal) {
      stopCamera();
    }
  }, [openModal]);

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
            {stream && openModal && (
              <QrReader
                ref={qrRef}
                constraints={{
                  facingMode: "environment",
                  aspectRatio: 1,
                }}
                videoId="qr-video"
                scanDelay={3000}
                onResult={handleScan}
                className="w-full"
                videoStyle={{ width: "100%" }}
                ViewFinder={() => (
                  <div className="border-2 border-blue-500 absolute top-0 left-0 right-0 bottom-0 z-10 pointer-events-none"></div>
                )}
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
