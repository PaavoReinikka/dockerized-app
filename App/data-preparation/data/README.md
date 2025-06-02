### Folder for web extracted xslx and csv files

Primarily, these should not be needed on git. The data-preparation service automatically fetches and cleans the data, and then either loads them into database directly (or via migrations).

You can add new scripts in `../scripts` if you have some further data you want to populate before launching the app.
