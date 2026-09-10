from PIL import Image

from pathlib import Path
from time import sleep
import asyncio

from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool




#Простая фоновая задача
@celery_instance.task
def test_task():
    sleep(5)
    print("я молодец")


#сделать N размеры для изображения
@celery_instance.task
def resize_image(image_path: str):


    output_dir: str = "src/static/images"
    widths: tuple = (size for size in range(100, 1000))

    """
    Масштабирует изображение до заданных ширин с сохранением пропорций
    и сохраняет их в указанную директорию.
    """
    src_path = Path(image_path)
    if not src_path.is_file():
        raise FileNotFoundError(f"Файл не найден: {src_path}")

    dest_dir = Path(output_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []

    with Image.open(src_path) as img:
        orig_width, orig_height = img.size

        for width in widths:
            # Вычисляем высоту с сохранением пропорций
            ratio = width / orig_width
            new_height = int(orig_height * ratio)

            # Качественный ресайз с фильтром Lanczos
            resized_img = img.resize((width, new_height), Image.Resampling.LANCZOS)

            # Формируем имя файла вида: filename_1000w.jpg
            new_filename = f"{src_path.stem}_{width}w{src_path.suffix}"
            save_path = dest_dir / new_filename

            # Параметры сохранения в зависимости от формата
            save_kwargs = {}
            ext = src_path.suffix.lower()

            if ext in (".jpg", ".jpeg"):
                # Для JPEG убираем альфа-канал, если он был
                if resized_img.mode in ("RGBA", "P"):
                    resized_img = resized_img.convert("RGB")
                save_kwargs = {"quality": 85, "optimize": True}
            elif ext == ".png":
                save_kwargs = {"optimize": True}
            elif ext == ".webp":
                save_kwargs = {"quality": 85}

            resized_img.save(save_path, **save_kwargs)
            saved_files.append(save_path)
    print("конец создания изображений")



#Фоновая задача выполняющаяся каждые n-секунд
async def send_emails_to_users_with_today_checkin_helper():
    print("Я ЗАПУСКАЮСЬ")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checking()
        print(f"{bookings=}")
    

@celery_instance.task(name="booking_today_checking")
def send_emails_to_users_with_today_checkin():
    asyncio.run(send_emails_to_users_with_today_checkin_helper())