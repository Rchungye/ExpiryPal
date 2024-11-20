CREATE DATABASE ExpiryPal;
GO

USE ExpiryPal;
GO

CREATE TABLE User (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    unusedItemsPreference INT, /* number of days after which an item is considered unused */
    ExpiryDatePreference INT /* number of days before the expiration date that the user wants to be notified */
);
GO

CREATE TABLE Fridge (
    id INT PRIMARY KEY AUTO_INCREMENT,
    model VARCHAR(50),
    brand VARCHAR(50),
    code VARCHAR(50), /* this is the code that the user will use to connect to the fridge */
);
GO

/* M:N RELATIONSHIP: even if now were connecting n users to 1 fridge, in the future we may want to add more fridges to a user.*/
CREATE TABLE FridgeUser (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    fridge_id INT,

    FOREIGN KEY (user_id) REFERENCES User (id),
    FOREIGN KEY (fridge_id) REFERENCES Fridge (id)
);
GO

CREATE TABLE Camera (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_fridge INT,
    model VARCHAR(50),
    brand VARCHAR(50),
    accessURL VARCHAR(2048) /* chrome's url char limit  */

    FOREIGN KEY (id_fridge) REFERENCES Fridge (id)
);
GO

CREATE TABLE Item (
    id INT PRIMARY KEY AUTO_INCREMENT,
    fridge_id INT,
    name VARCHAR(50),
    addedDate DATE,
    expirationDate DATE,

    FOREIGN KEY (fridge_id) REFERENCES Fridge (id)
);
GO

CREATE TABLE Notification (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    item_id INT,
    notificationDate DATETIME, /* this is the date when the user will receive the notification */
    message TEXT, /* this will be the message that the user will receive */

    FOREIGN KEY (user_id) REFERENCES User (id),
    FOREIGN KEY (item_id) REFERENCES Item (id)
);
GO

CREATE TABLE fridgeLog (
    id INT PRIMARY KEY AUTO_INCREMENT,
    item_id INT,
    user_id INT,
    changeDescription TEXT,

    FOREIGN KEY (item_id) REFERENCES Item (id),
    FOREIGN KEY (user_id) REFERENCES User (id)
);
GO
