import os
import subprocess
import sys
import threading

project_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_directory)

def install_requirements():
    """Устанавливает зависимости из requirements.txt, если файл существует."""
    if os.path.exists("requirements.txt"):
        print("Устанавливаю зависимости из requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print("Файл requirements.txt не найден. Пропускаю установку зависимостей.")

def run_backend():
    """Запускает backend."""
    print("Запускаю backend...")
    backend_path = project_directory + "\\backend.py"
    subprocess.run([sys.executable, backend_path])

def run_frontend():
    """Запускает frontend с использованием Streamlit."""
    print("Запускаю frontend (Streamlit)...")
    frontend_path = project_directory + "\\demo.py"
    subprocess.run([sys.executable, "-m", "streamlit", "run", frontend_path, "--server.port", "4080", "--server.address", "localhost", "secret_key"])

def main():
    # Установка зависимостей
    install_requirements()

    # Запуск backend в отдельном потоке
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.start()

    # Запуск frontend в основном потоке
    frontend_thread = threading.Thread(target=run_frontend)
    frontend_thread.start()

    # Ожидание завершения работы обоих потоков
    backend_thread.join()
    frontend_thread.join()

if __name__ == "__main__":
    main()
    os.system("pause")