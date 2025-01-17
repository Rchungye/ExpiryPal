import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import NavBar from "./NavBar";
import ItemModal from "./ItemModal";
import { getItemsByFridgeId, deleteItemById } from "../services/items";
import { getNotificationPreferences } from "../services/notificationService";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBell, faX, faBars } from "@fortawesome/free-solid-svg-icons";
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import { generateToken } from "../notifications/firebase";
import { getCookies, saveNotificationPreferences } from "../services/api"; // Adjust the import path as necessary
import { checkUserLink, checkIfCMFToken } from "../services/api";

function Groceries() {

  const [navBarOpen, setNavBarOpen] = useState(false); //Tracks navbar visibility
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [items, setItems] = useState([]);
  const [isVerified, setIsVerified] =  useState(false);
  const [notificationModalOpen, setNotificationModalOpen] = useState(false);

  const [notificationPreferences, setNotificationPreferences] = useState({
    expiration: 3,
    unusedItem: 7
  });

  const navigate = useNavigate();

  const fridgeId = 1;
  const [sortOption, setSortOption] = useState("newest");
  const [searchQuery, setSearchQuery] = useState(""); //State for search query

  const modalStyle = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: '90%',
    maxWidth: 800,
    maxHeight: '80vh',
    bgcolor: 'background.paper',
    borderRadius: '8px',
    boxShadow: 24,
    p: 4,
    overflow: 'auto'
  };
  useEffect(() => {
    // Si ya está verificado, no hacer nada
    if (isVerified) return;

    const fetchCookies = async () => {
      console.log("Getting cookies...");
      try {
        const response = await getCookies();
        console.log("Cookies:", response);
        if (response['status'] === 200) {
          setIsVerified(true);
        } else {
          setIsVerified(false);
        }
      } catch (error) {
        console.error("Error getting cookies:", error);
      }
    };
    const checkCMFToken = async () => {
      try {
        const response = await checkIfCMFToken();
        console.log("isCMFToken:", response);

        if (response.status === 200) {
          console.log("CMF Token exists:", response.data);
          // Usuario autenticado y linkeado
        }
      } catch (error) {
        // Axios atrapa los errores aquí para códigos no 2xx
        if (error.response) {
          // Manejar errores del servidor
          if (error.response.status === 404) {
            console.log("CMF Token not found, generating a new one...");
            generateToken();
          } else {
            console.error(
              "Unhandled error from the server:",
              error.response.data
            );
          }
        } else if (error.request) {
          // No hubo respuesta del servidor
          console.error("No response received from the server:", error.request);
        } else {
          // Error en la configuración de la solicitud
          console.error("Error in setting up the request:", error.message);
        }
      }
    };

    const checkAuthToken = async () => {
      try {
        const response = await checkUserLink();
        console.log("isLinked:", response);
        if (response.status === 200) {
          // Usuario autenticado y linkeado
          setIsVerified(true); // Marcar como verificado
        } else {
          // Usuario no autenticado, redirigir a welcome o login
          navigate("/");
          setIsVerified(false);
        }
      } catch (error) {
        console.error("Error verifying user link:", error);
        setIsVerified(false);
        navigate("/"); // Manejar casos de error redirigiendo a una página segura
      }
    };

    // Ejecutar ambas funciones de verificación
    fetchCookies();
    checkAuthToken();
    checkCMFToken();
  }, [isVerified, navigate]); // Dependencias: isVerified y navigate



  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await getItemsByFridgeId(fridgeId);
        const transformedItems = response.data.payload.map((item) => ({
          id: item.id,
          name: item.name || `Item ${item.id}`,
          image: item.imageURL || "/items/default.png",
          dateExp: formatDateToDDMMYY(item.expirationDate),
          dateAdded: formatDateToDDMMYY(item.addedDate),
        }));
        setItems(transformedItems);
      } catch (error) {
        console.error("Failed to fetch items:", error);
      }
    };

    const fetchNotificationPreferences = async () => {
      try {
        const response = await getNotificationPreferences(fridgeId);
        console.log("response in fetchNotificationsPreferences", response);
        if (response.status === 200) {
          if (response.expiration && response.unusedItem) {
            setNotificationPreferences({
              expiration: response.expiration,
              unusedItem: response.unusedItem,
            });
          }
        } else {
          // Si no hay respuesta o datos, asigna los valores predeterminados
          const response = await saveNotificationPreferences({
            fridge_id: fridgeId,
            expiration: 3,
            unusedItem: 7
          })
          setNotificationPreferences({
            expiration: 3,
            unusedItem: 7
          })
          console.log("Notification preferences saved:", response);
        }
      } catch (error) {
        console.error("Failed to fetch notification preferences:", error);
        // En caso de error, también puedes establecer los valores predeterminados
        setNotificationPreferences({
          expiration: 3,
          unusedItem: 7
        });
      }
    };

    // Llamar a la función para obtener las preferencias de notificación
    fetchNotificationPreferences();
    fetchItems();
  }, [fridgeId]);


  const toggleNavBar = () => {
    setNavBarOpen((prev) => !prev);
  };

  const sortItems = (items, option) => {
    const sortedItems = [...items];
    switch (option) {
      case "newest":
        return sortedItems.sort(
          (a, b) =>
            new Date(formatToISO(b.dateAdded)) -
            new Date(formatToISO(a.dateAdded))
        );
      case "oldest":
        return sortedItems.sort(
          (a, b) =>
            new Date(formatToISO(a.dateAdded)) -
            new Date(formatToISO(b.dateAdded))
        );
      case "expiry-soon":
        return sortedItems.sort(
          (a, b) =>
            new Date(formatToISO(a.dateExp)) - new Date(formatToISO(b.dateExp))
        );
      default:
        return sortedItems;
    }
  };

  const formatToISO = (ddmmyy) => {
    if (!ddmmyy) return null;
    const [day, month, year] = ddmmyy.split("/");
    return `20${year}-${month}-${day}`;
  };

  const handleSortChange = (e) => {
    setSortOption(e.target.value);
  };

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value.toLowerCase());
  };

  //Filter and sort items
  const filteredAndSortedItems = sortItems(
    items.filter((item) => item.name.toLowerCase().includes(searchQuery)),
    sortOption
  );

  //Sets the selected item and opens the modal
  const handleItemClick = (item) => {
    setSelectedItem(item);
    setModalOpen(true);
  };

  //Handle item updates
  const handleUpdateItem = (updatedItem) => {
    setItems((prevItems) =>
      prevItems.map((item) => (item.id === updatedItem.id ? updatedItem : item))
    );
  };

  //Handle item removal
  const handleRemoveItem = (itemId) => {
    setItems((prevItems) => prevItems.filter((item) => item.id !== itemId));
    deleteItemById(itemId);

  };

  const calculateDaysLeft = (expDate) => {
    if (!expDate) return null;
    const [day, month, year] = expDate.split("/").map(Number);
    const expiration = new Date(2000 + year, month - 1, day);
    const today = new Date();

    expiration.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);

    const diffTime = expiration - today;
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  };

  const isItemNew = (dateAdded) => {
    if (!dateAdded) return false;
    const [day, month, year] = dateAdded.split("/").map(Number);
    const addedDate = new Date(2000 + year, month - 1, day);
    const today = new Date();

    addedDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);

    return addedDate.getTime() === today.getTime();
  };

  const calculateDaysSinceAdded = (dateAdded) => {
    if (!dateAdded) return null;
    const [day, month, year] = dateAdded.split("/").map(Number);
    const addedDate = new Date(2000 + year, month - 1, day);
    const today = new Date();

    addedDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);

    const diffTime = today - addedDate;
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  };

  const formatDateToDDMMYY = (dateString) => {
    if (!dateString) return "";
    const date = new Date(dateString);
    const day = String(date.getUTCDate()).padStart(2, "0");
    const month = String(date.getUTCMonth() + 1).padStart(2, "0");
    const year = String(date.getUTCFullYear()).slice(-2);
    return `${day}/${month}/${year}`;
  };


  const getNotificationItems = () => {
    return items.filter(item => {
      const daysLeft = calculateDaysLeft(item.dateExp);
      const daysSinceAdded = calculateDaysSinceAdded(item.dateAdded);

      return (
        (daysLeft !== null && daysLeft <= notificationPreferences.expiration) ||
        (daysSinceAdded !== null && daysSinceAdded >= notificationPreferences.unusedItem)
      );
    });
  };

  return (
    <div className="bg-gray-100 min-h-screen font-roboto relative overflow-hidden">
      <header className="bg-blue-main text-white">
        <div className="max-w-[1024px] mx-auto p-4 flex justify-between items-center">
          <h1 className="text-3xl">ALL ITEMS</h1>

          <div className="flex justify-center relative">
            <FontAwesomeIcon icon={faBell} className="h-8 cursor-pointer hover:text-gray-200"
              onClick={() => setNotificationModalOpen(true)} />
            {getNotificationItems().length > 0 && (
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                {getNotificationItems().length}
              </span>
            )}
          </div>

          <button onClick={toggleNavBar} className="text-3xl cursor-pointer menu-button">
            {navBarOpen ? <FontAwesomeIcon icon={faX} /> : <FontAwesomeIcon icon={faBars} />}
          </button>
        </div>
      </header>

      {/* Notifications Modal */}
      <Modal open={notificationModalOpen} onClose={() => setNotificationModalOpen(false)}
        aria-labelledby="notification-modal-title">
        <Box sx={modalStyle}>
          <div className="flex justify-between items-center mb-4">
            <Typography variant="h4" component="h2">
              Notifications
            </Typography>
            <button onClick={() => setNotificationModalOpen(false)}
              className="text-2xl font-bold hover:text-gray-700">
              <FontAwesomeIcon icon={faX} />
            </button>
          </div>

          <div className="grid gap-4">
            {getNotificationItems().map((item) => {
              const daysLeft = calculateDaysLeft(item.dateExp);
              const daysSinceAdded = calculateDaysSinceAdded(item.dateAdded);
              const expired = daysLeft !== null ? daysLeft < 0 : false;

              return (
                <div key={item.id} className="flex items-center bg-white p-4 rounded-lg shadow">
                  <img src={item.image} alt={item.name}
                    className="w-16 h-16 object-contain mr-4" />
                  <div className="flex-grow">
                    <h3 className="font-bold text-lg">{item.name}</h3>
                    <p className="text-sm text-gray-600">
                      Added: {item.dateAdded}
                      {daysSinceAdded >= notificationPreferences.unusedItem && (
                        <span className="text-blue-600 ml-2">
                          (Unused for {daysSinceAdded} days)
                        </span>
                      )}
                    </p>
                    <p className={`text-sm ${expired ? 'text-red-600' :
                      daysLeft <= notificationPreferences.expiration ? 'text-orange-600' :
                        'text-gray-600'
                      }`}>
                      {expired
                        ? `Expired ${Math.abs(daysLeft)} days ago` : daysLeft === 0
                          ? "Expires today" : `Expires in ${daysLeft} days`}
                    </p>
                  </div>
                </div>
              );
            })}
            {getNotificationItems().length === 0 && (
              <Typography className="text-center text-gray-500 py-4">
                No pending notifications
              </Typography>
            )}
          </div>
        </Box>
      </Modal>

      <div className="max-w-[1024px] mx-auto p-4">
        {/*Dropdown and Search Bar*/}
        <div className="flex items-end px-4 py-2 bg-gray-100 space-x-4">
          <div className="flex flex-col">
            <label htmlFor="sort" className="text-lg font-bold text-gray-700 mb-1"            >
              Sort by:
            </label>
            <select id="sort" className="border rounded px-3 py-2 bg-white shadow-sm focus:outline-none"
              value={sortOption} onChange={handleSortChange} >
              <option value="newest">Newest</option>
              <option value="oldest">Oldest</option>
              <option value="expiry-soon">Expiring Soon</option>
            </select>
          </div>

          {/*Search Bar*/}
          <div className="flex-grow max-w-[300px]">
            <input type="text" placeholder="Search items..." value={searchQuery} onChange={handleSearchChange}
              className="border rounded px-3 py-2 bg-white shadow-sm focus:outline-none w-full" />
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 p-4"
          style={{ minHeight: "300px" }} >
          {filteredAndSortedItems.map((item) => {
            //Calculate daysLeft and expired dynamically
            const daysLeft = calculateDaysLeft(item.dateExp);
            const expired = daysLeft !== null ? daysLeft < 0 : false;

            //Determine warnings
            let warning = "";
            if (expired) {
              warning = "red";
            } else if (daysLeft !== null && daysLeft >= 0 && daysLeft <= 2) {
              warning = "orange";
            }
            const isNew = isItemNew(item.dateAdded);
            const daysSinceAdded = calculateDaysSinceAdded(item.dateAdded);
            const blueWarning = daysSinceAdded !== null && daysSinceAdded > 5;

            return (
              <div
                key={item.id}
                onClick={() => handleItemClick(item)}
                className={`bg-white rounded-lg shadow p-4 relative text-center cursor-pointer max-w-52 item h-[210px] ${expired
                  ? "border border-red-400" : warning === "orange"
                    ? "border border-orange-400" : blueWarning
                      ? "border border-blue-400" : ""
                  }`}
              >
                {isNew && (
                  <div className="absolute top-2 left-2 bg-green-500 text-white text-xs font-bold px-2 py-1 rounded">
                    NEW
                  </div>
                )}
                {warning === "red" && (
                  <div className="absolute top-2 right-2 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">
                    !
                  </div>
                )}
                {warning === "orange" && !expired && (
                  <div className="absolute top-2 right-2 bg-orange-500 text-white text-xs font-bold px-2 py-1 rounded">
                    !
                  </div>
                )}
                {blueWarning && (
                  <div
                    className={`absolute ${warning === "red"
                      ? "top-2 right-8" : warning === "orange"
                        ? "top-2 right-8" : "top-2 right-2"
                      } bg-blue-500 text-white text-xs font-bold px-2 py-1 rounded`}
                  >
                    !
                  </div>
                )}
                <img src={item.image} alt={item.name} className="w-full h-24 object-contain rounded mb-3" />
                <p className="font-semibold">{item.name}</p>
                <span className="text-gray-500 text-sm block">
                  Added: {item.dateAdded}
                </span>
                <span className={`text-sm font-semibold ${expired
                  ? "text-red-600" : warning === "orange"
                    ? "text-orange-600" : "text-gray-600"}`} >
                  Exp: {daysLeft !== null
                    ? daysLeft === 0
                      ? "Expires today" : `${Math.abs(daysLeft)} days ${expired ? "ago" : "left"}`
                    : "N/A"}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/*Sliding NavBar*/}
      <div
        className={`fixed top-0 right-0 h-full w-full bg-white transform transition-transform 
          duration-300 ease-in-out ${navBarOpen ? "translate-x-0" : "translate-x-full"}`} >
        <NavBar onBackToItems={toggleNavBar} />
      </div>

      {/*Item Modal*/}
      {modalOpen && (
        <ItemModal item={selectedItem} onClose={() => setModalOpen(false)}
          onUpdateItem={handleUpdateItem} onRemoveItem={handleRemoveItem} />
      )}
    </div>
  );
}

export default Groceries;
