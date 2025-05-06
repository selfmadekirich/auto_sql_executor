import inspect
from functools import wraps


def proccess_password(
        crypt: bool
):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            func_signature = inspect.signature(func)
            bound_args = func_signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            encoder = bound_args.arguments.get("crypt_service")

            if crypt:
                data = bound_args.arguments.get("data")
                data.json_props.password = encoder.encode_str(
                    data.json_props.password
                )

            result = await func(*args, **kwargs)

            if not crypt:
                result.json_props["password"] = encoder.decode_str(
                    result.json_props.get("password")
                )
            return result
        return wrapper
    return decorator


def proccess_tokens(
        crypt: bool
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            func_signature = inspect.signature(func)
            bound_args = func_signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            encoder = bound_args.arguments.get("crypt_service")

            if crypt:
                data = bound_args.arguments.get("data")
                data.auth_token = encoder.encode_str(
                    data.auth_token
                )

            result = await func(*args, **kwargs)

            if not crypt:
                result.auth_token = encoder.decode_str(
                    result.auth_token
                )
            return result
        return wrapper
    return decorator


def check_logic(
        check_function,
        exception: Exception
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            func_signature = inspect.signature(func)
            bound_args = func_signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            print(bound_args.arguments.keys())
            data = bound_args.arguments.get("data")

            check_result = check_function(data)
            if not check_result:
                raise exception

            return await func(*args, **kwargs)
        return wrapper
    return decorator
