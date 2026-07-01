@echo off
echo Mengatur environment variables untuk TensorFlow...
set TF_ENABLE_ONEDNN_OPTS=0
set TF_CPP_MIN_LOG_LEVEL=2

echo Menjalankan Aplikasi Catur Magnus...
python -m streamlit run frontend/app.py
pause
