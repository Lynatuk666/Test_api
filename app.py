import fastapi
from database_scripts import get_balance, update_balance
from pydantic import BaseModel
from fastapi import Response

app = fastapi.FastAPI()


@app.get("/api/v1/wallets/{uuid}", status_code=200)
async def show_balance(uuid, response: Response):
    try:
        result = await get_balance(uuid=int(uuid))
        if result:
            return {"message": f"Wallet - {result[0]['uuid']} Balance - {result[0]['balance']}"}
        else:
            response.status_code = 400
            return {"message": "Wallet doesn't exist"}
    except ValueError:
        response.status_code = 400
        return {"message": "Check Wallet UUID"}


class Operation(BaseModel):
    operationType: str
    amount: int


@app.post("/api/v1/wallets/{uuid}/operation", status_code=200)
async def operations(uuid, operation: Operation, response: Response):
    if operation.operationType == "DEPOSIT" or operation.operationType == "WITHDRAW":
        try:
            response.status_code = 200
            return {"message": await update_balance(uuid=uuid,
                                                    operation=operation.operationType,
                                                    amount=operation.amount)}
        except IndexError:
            response.status_code = 400
            return {"message": "ERROR. INCORRECT DATA"}
    else:
        response.status_code = 400
        return {"message": "ERROR. INCORRECT DATA"}
