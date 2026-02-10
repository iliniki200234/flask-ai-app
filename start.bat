@echo off
echo ====================================
echo Am(I)Hungry AI Agent - Startup
echo ====================================
echo.

echo [1/3] Initializing database...
python database.py
echo.

echo [2/3] Starting Flask server...
echo Server will be available at: http://localhost:5000
echo Press CTRL+C to stop the server
echo.

python app.py
