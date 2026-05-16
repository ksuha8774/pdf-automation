import os
from session import create_anonymous_session
from pdf_api import upload_pdf, wait_for_processing, download_processed_pdf
from db import save_to_db
from logger import setup_logger
from forward import send_to_another_site

def main():
    logger = setup_logger()
    logger.info("Запуск скрипта")

    PDF_FILE = "document.pdf"   
    API_BASE = "http://localhost:8080/api/v1"
    UPLOAD_URL = f"{API_BASE}/upload"
    STATUS_URL = f"{API_BASE}/status"
    DOWNLOAD_URL = f"{API_BASE}/download"
    TARGET_URL = "https://httpbin.org/post"

    if not os.path.exists(PDF_FILE):
        logger.error("PDF файл не найден")
        print("Файл document.pdf не найден в текущей папке")
        return

    session = create_anonymous_session()
    logger.info("Сессия создана")

    try:
        task_id = upload_pdf(session, PDF_FILE, UPLOAD_URL)
        logger.info(f"Загружен, task_id={task_id}")

        if wait_for_processing(session, task_id, STATUS_URL):
            processed_data = download_processed_pdf(session, task_id, DOWNLOAD_URL)
            logger.info(f"Скачан, размер={len(processed_data)}")

            record_id = save_to_db(os.path.basename(PDF_FILE), processed_data)
            logger.info(f"Сохранён в БД, id={record_id}")

            forward_resp = send_to_another_site(session, processed_data, TARGET_URL)
            logger.info(f"Отправлен на другой сайт, ответ={forward_resp}")

            print("Всё выполнено успешно!")
        else:
            logger.error("Таймаут обработки")
            print("Обработка не завершилась")
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()