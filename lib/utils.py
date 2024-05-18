import inspect

async def await_helper(value):
 result = value
 if inspect.iscoroutine(result):
    result = await result
 return result