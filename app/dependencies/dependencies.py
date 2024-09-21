from fastapi import Depends

def common_dependency():
    return {"msg": "This is a common dependency"}
