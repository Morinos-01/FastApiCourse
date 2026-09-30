import json
import logging

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractExchange, AbstractQueue, AbstractConnection
from aio_pika import ExchangeType, DeliveryMode

from src.config import settings


async def connect_rabbitmq()->AbstractConnection:
    logging.info("Начинаю подключение к RabbitMQ")
    connect = await aio_pika.connect_robust(settings.RABBIT_URL)
    logging.info(f"Успешное подключение к RabbitMQ = {connect}")
    return connect


async def declare_exchange(
    channel: AbstractChannel,
    exc_name: str,
    exc_type: ExchangeType = ExchangeType.DIRECT
)->AbstractChannel:
    return await channel.declare_exchange(
        name=exc_name,
        type=exc_type,
        durable=True,
    )


async def declare_queue(
    channel: AbstractChannel, 
    exchange: AbstractExchange,
    queue_name: str,
    routing_key: str
)->AbstractQueue:
    queue = await channel.declare_queue(name=queue_name, durable=True)
    await queue.bind(exchange=exchange, routing_key=routing_key)
    return queue


async def publish_exchange(exchange: AbstractExchange, routing_key: str, data)->None:
    message = aio_pika.Message(body=json.dumps(data, default=str).encode(), delivery_mode=DeliveryMode.PERSISTENT)
    await exchange.publish(message=message, routing_key=routing_key)

