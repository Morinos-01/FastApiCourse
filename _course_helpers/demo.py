# def demo_decorator(func):
#     def wrapper(*args, **kwargs):
#         def inner():
#             res = func(*args, **kwargs)
#             num = 3 * res
#             return num

#         return inner()

#     return wrapper


# # Решение задачи
# from functools import wraps


# """ А я вообще правильно передал аргументы в сам декоратор? 
#     Будто тоже бессмысленная хуйня, множно было бы явно указать аргументы min_total и discount_percent
#     А в задаче сказано, что декоратор должен принимать ваще всё.
# """
# def apply_discount(*args, **kwargs):
#     # Выглядит тоже очень дебильно
#     min_total = kwargs["min_total"]
#     discount_percent = kwargs["discount_percent"]
#     if discount_percent > 100 or discount_percent < 0:
#         raise ValueError("Ошибка")

#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#                 price = func(*args, **kwargs)
#                 # стоит дебильная проверка, потому что впадлу проверять условие в котором могут в аргументы положить True 
#                 if price <= min_total or kwargs != {}:
#                     return price

#                 price_with_discount = price * (1 - (discount_percent / 100))
#                 return price_with_discount
#         return wrapper
#     return decorator


# @apply_discount(min_total=5000, discount_percent=10)
# def calculate_order_total(
#     price: float,
#     quantity: int,
#     is_promo: bool = True, # Я чет не понял, зачем нужен этот аргумент. Если дефолт значение будет False, как мы можем повлиять на работу внешней функции
# ) -> float:
#     return price * quantity


# res = calculate_order_total(1000, 6)
# # 3000


# print(res)






from functools import wraps


def apply_decorator(min_total: int=1000, discount_percent: int=10):
    if not (0 <= discount_percent <= 100):
        raise ValueError('Процент должен быть в диапазоне больше [0, 100]')
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
                res = func(*args, **kwargs)
                is_promo = kwargs.get("is_promo", None)
                if is_promo is None:
                    if len(args) > 2:
                       is_promo = args[2]
                    else:
                        is_promo = True
                if is_promo and res >= min_total:
                    return res * (100 - discount_percent) / 100
                return res
        return wrapper
    return inner


@apply_decorator(min_total=5000, discount_percent=10)
def calculate_order_total(
    price: float,
    quantity: int,
    is_promo: bool = False, 
) -> float:
    return price * quantity


res = calculate_order_total(1000, 6)
# 6000
print(res)