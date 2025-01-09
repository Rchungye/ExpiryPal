import { useEffect, useRef } from "react";
import PropTypes from "prop-types";
import { BrowserQRCodeReader } from "@zxing/browser";

const QRScanner = ({ onScan, onError }) => {
  const videoRef = useRef(null);
  const controlsRef = useRef(null);

  useEffect(() => {
    const codeReader = new BrowserQRCodeReader();

    codeReader
      .decodeFromVideoDevice(null, videoRef.current, (result, err) => {
        if (result) {
          onScan(result.text);
          if (controlsRef.current) {
            controlsRef.current.stop(); // Detener la cámara tras el escaneo
          }
        }
        if (err) {
          onError(err);
        }
      })
      .then((controls) => {
        controlsRef.current = controls;
      })
      .catch((err) => {
        onError(err);
        console.error("Error initializing QR Reader:", err);
      });

    return () => {
      if (controlsRef.current) {
        controlsRef.current.stop(); // Detener la cámara al desmontar
      }
    };
  }, [onScan, onError]);

  return <video ref={videoRef} style={{ width: "100%" }} />;
};

QRScanner.propTypes = {
  onScan: PropTypes.func.isRequired,
  onError: PropTypes.func.isRequired,
};

export default QRScanner;
