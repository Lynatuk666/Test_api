import fastapi
from database_scripts import get_balance, update_balance
from pydantic import BaseModel

app = fastapi.FastAPI()


@app.get("/api/v1/wallets/{uuid}")
async def show_balance(uuid):
    try:
        result = await get_balance(uuid=int(uuid))
        if result:
            return f"Wallet - {result[0]['uuid']} Balance - {result[0]['balance']}", 200
        else:
            return "Wallet doesn't exist", 400
    except ValueError:
        return "Check Wallet UUID", 400


class Operation(BaseModel):
    operationType: str
    amount: int


@app.post("/api/v1/wallets/{uuid}/operation")
async def operations(uuid, operation: Operation):
    if operation.operationType == "DEPOSIT" or operation.operationType == "WITHDRAW":
        try:
            return await update_balance(uuid=uuid,
                                        operation=operation.operationType,
                                        amount=operation.amount)
        except IndexError:
            return "ERROR. INCORRECT DATA", 400
    else:
        return "ERROR. INCORRECT DATA", 400
