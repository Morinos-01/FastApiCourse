docker network create myNetwork

# Postgre
docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume=pg-booking-data:/var/lib/postgresql/data \
    -d postgres:17


# Redis
docker run --name booking_cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:8


# RabbitMQ
docker run --name booking_rabbit \
    -p 5672:5672 \
    -p 15672:15672 \
    --network=myNetwork \
    rabbitmq:3-management


# Backend
docker run --name booking_back \
    -p 7777:8000 \
    --network=myNetwork \
    booking_image


# Celery worker
docker run --name booking_celery_work \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO


# Celery worker Beat
docker run --name booking_celery_beat \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance beat -l INFO



# Создание образа Backend
docker build -t booking_image . 