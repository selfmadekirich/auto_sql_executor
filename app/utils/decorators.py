import inspect


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
