from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any


app = FastAPI(title="Expenses Management API")

expenses: Dict[int, Dict[str, Any]] = {}
# 1: {"id": 1, "description": "خرید مواد غذایی", "amount": 150000.0},
next_id: int = 1


@app.get("/")
def root():
    return {"message": "hello world"}


@app.post("/expense/add/", status_code=status.HTTP_201_CREATED)
def created_expense(expense: Dict[str, Any]):
    global next_id
    if "description" not in expense or not isinstance(expense["description"], str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="add description"
        )
    if "amount" not in expense or not isinstance(expense["amount"], (int, float)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="add amount"
        )

    new_expense = {
        "id": next_id,
        "description": expense["description"],
        "amount": float(expense["amount"]),
    }

    expenses[next_id] = new_expense
    next_id += 1

    return JSONResponse(content=new_expense, status_code=status.HTTP_201_CREATED)


@app.get("/expenses/", status_code=status.HTTP_200_OK)
def get_all_expenses() -> list[Dict[str, Any]]:
    return list(expenses.values())


@app.get("/expense/{expense_id}/", status_code=status.HTTP_200_OK)
def get_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="add id")
    return expenses[expense_id]


@app.post("/update/{expense_id}")
def update_expense(expense_id: int, expense: Dict[str, Any]):
    if expense_id not in expenses:
        raise HTTPException(status_code=404, detail="Expense not found")

    if "description" not in expense or not isinstance(expense["description"], str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="add description"
        )
    if "amount" not in expense or not isinstance(expense["amount"], (int, float)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="add amount"
        )

    updated_expense = {
        "id": expense_id,
        "description": expense["description"],
        "amount": float(expense["amount"]),
    }

    expenses[expense_id] = updated_expense
    return updated_expense


@app.delete("/expense/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int):
    if expense_id not in expenses:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    del expenses[expense_id]
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT, content="deleted successfully"
    )
