import cola from "./assets/coca-cola-png-image-10.png";
import eggs from "./assets/eggs.png";
import julmust from "./assets/julmust.png";
import mjolk from "./assets/mjolk.png";
import pesto from "./assets/pesto.png";
import pudding from "./assets/pudding.png";
import pickleJar from "./assets/pickle-jar.png";

const items = [
  {
    id: 1,
    name: "CocaCola",
    image: cola,
    date: "19/08/24",
    daysLeft: 7,
    isNew: true,
  },
  {
    id: 2,
    name: "Eggs",
    image: eggs,
    date: "16/10/2024",
    daysLeft: 4,
    isNew: true,
    warning: "orange",
  },
  {
    id: 3,
    name: "Julmust",
    image: julmust,
    date: "19/08/24",
    daysLeft: 0,
    expired: true,
    warning: "red",
  },
  {
    id: 4,
    name: "Milk",
    image: mjolk,
    date: "19/08/24",
    daysLeft: 4,
    warning: "blue",
  },
  {
    id: 5,
    name: "Pesto",
    image: pesto,
    date: "19/08/24",
    daysLeft: 4,
  },
  {
    id: 6,
    name: "Pudding",
    image: pudding,
    date: "19/08/24",
    daysLeft: 4,
  },
  {
    id: 7,
    name: "Pickles",
    image: pickleJar,
    date: "19/08/24",
    daysLeft: 4,
  },
];

export default items;
