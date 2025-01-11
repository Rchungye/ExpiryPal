[33md6db00b[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mvictor[m[33m)[m cookies fixed! now user doesn't need to log in every time todo: manage to send push notifications to the user when the expiration date is near
[33m156528f[m cookies fixed todo: manage to send push notifications to the user when the expiration date is near
[33m4aa1769[m[33m ([m[1;31morigin/victor[m[33m)[m to do: fix cookies, not working yet. functions are in FridgeController.py and fridge_routes.py commiting in case someone need the code.
[33m4a4e9f3[m updated requirements.txt
[33mc2268dc[m changes made to app.py, item_routes and ItemController. added_items are now being saved to the database and cloudinary
[33m0dac1ff[m fixed groceries page, now listing items
[33mcbe96a3[m Refactor: Implemented item comparison logic and improved fridge item handling
[33mf630661[m Fixed camera bug: link to fridge working need to be tested on https (secure) connection to see if the cookies are working properly
[33mad42c18[m a
[33m057f147[m Merge branch 'Petar' of https://github.com/RchungyeUTP/ExpiryPal into victor
[33m330bf05[m Backend connected to the model. Items are updated automatically
[33m21f85a4[m small changes for testing, tests are gitignored
[33mdefb980[m notification preferences dynamic updating
[33m57c4e59[m Logs update dynamically, can edit item name and expiration date dynamically
[33ma31106a[m Groceries dynamic data from database, AND sorting functonallity
[33m4a03400[m Merge branch 'Victor' into Petar
[33m5b9e2cf[m uploaded requirements.txt files
[33m30ae857[m linked backend with model there is a problem with the response of the model in the backend The image from the fridge is uploaded to cloudinary Then the image is sent to the model The model upload the fragmented pictures to cloudinary the POST request to the model should return an list of items (item routes) But it has an error that I have to fix.
[33m4ab190b[m added scheculer and camera routes
[33mb7e19f3[m connected to fly.io and cloudinary
[33me9bc633[m notification preferences connection to front fix
[33mae049cc[m fixing
[33me0615c9[m Merge branch 'victor' of https://github.com/RchungyeUTP/ExpiryPal into victor
[33m3166bd3[m Added: fridge log model, controller and routes. Modified: .env File and other controllers, models and routes.
[33m479e684[m Update requirements.txt
[33maac29f6[m add: home_assistant_test script
[33m16c48ae[m Create test.py
[33m9cd9edf[m[33m ([m[1;31morigin/Petar[m[33m, [m[1;32mmain[m[33m)[m Update api.config.js
[33mb365f01[m Merge branch 'Petar'
[33m301b1e8[m Merge branch 'test' into Rchungye
[33mb16c257[m Merge branch 'victor' into test
[33m69e96f8[m merge corrections
[33m01892b1[m Merge branch 'victor' of https://github.com/RchungyeUTP/ExpiryPal into victor
[33m01c59e9[m Merge branch 'victor' into test
[33m40c7f14[m name corrections
[33md1d826f[m Update requirements.txt
[33m6404d2d[m Update requirements.txt
[33m13f9f07[m update req, __init__ and config
[33mb276701[m requierements update
[33m07bf168[m Update requirements.txt
[33mb6ad055[m updated: controllers, models, routes, services, and schemas the middleware/secure.py file was added, still have to work on it tested: notification preferences route, now we can update notification preferences directly from frontend endpoint created for bringing items by a fridge_id endpoint created for pairing a fridge with a user. This one returns a token that will be used to pair the fridge with the user note: the notification.js file was deleted and replaced by notificationService.js
[33me9faff0[m delete __pycache__
[33mc40b3a1[m update requirements
[33m58a2623[m Merge branch 'main' into Rchungye
[33m03f64df[m add readme, edit contollers and .env url
[33mc0d06ac[m ML flask v1
[33m50896e4[m addded remaining configurations, now we can bring fridge notification preferences from the db tested locally
[33m18e62a9[m changed the entire structure of the project to make it more modular and easier to maintain thanks rafa :)
[33m07c5fdb[m add blue warning, add responsivness, small fixes
[33m98fe2ae[m be structure part 3
[33mcca6988[m add basic resposivness, replace alert with a swal alert, add item name in case there is no provided name
[33m2e0e0cc[m implement item modal, add warning signs, add dynamic expiration calculation
[33m3858fc0[m be structure part 2 and material ui
[33m5708e69[m Merge branch 'victor' of https://github.com/RchungyeUTP/ExpiryPal into victor
[33mb26ad92[m updated camera routes, now get and post are working
[33mde51151[m be requierements update
[33m9a5bab1[m be structure part 1
[33m8662e10[m Merge branch 'Rchungye'
[33m1494bd4[m bugs fixed fridge, item and user POST/GET routes now working correctly
[33m43c15a8[m added item route file
[33m67e147d[m added fridge routes
[33m5966d97[m  Structure of the project has been updated.  POST and GET requests have been implemented for the user model.
[33mfd7861f[m first commi
[33m9823e99[m item part 3
[33me00a90c[m single item part 2
[33m356a2d6[m single item part 1
[33ma35f67f[m tailwind fix
[33m365e704[m components content
[33m4dd7cef[m initial components and services
[33mb7abf82[m Frontend React Initial Set Up
[33m30f4250[m Initial commit
