from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import InventoryItem, Order, Staff, Recommendation
from agent import ShopMindAgent
import uuid

app = FastAPI(title="ShopMind API", version="0.0.1")

# Enable CORS because frontend is on a different port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow everyone for hackathon!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = ShopMindAgent()

# --- MOCK DATABASE ---
# Pre-populating some data so it doesn't look empty
inventory_db = [
    InventoryItem(id="1", name="Wireless Headphones", quantity=4, price=59.99, category="Electronics", low_stock_threshold=5),
    InventoryItem(id="2", name="Ergonomic Mouse", quantity=15, price=29.99, category="Electronics"),
    InventoryItem(id="3", name="Mechanical Keyboard", quantity=2, price=120.00, category="Electronics", low_stock_threshold=3),
    InventoryItem(id="4", name="Laptop Stand", quantity=20, price=25.00, category="Accessories"),
]

orders_db = [
    Order(id="o1", customer_name="Alice", items=["1"], status="pending", total_amount=59.99),
    Order(id="o2", customer_name="Bob", items=["3"], status="processing", total_amount=120.00),
    Order(id="o3", customer_name="Charlie", items=["2", "4"], status="pending", total_amount=54.99),
]

staff_db = [
    Staff(id="s1", name="Rahul", role="Manager", status="available"),
    Staff(id="s2", name="Priya", role="Packer", status="busy", current_task="Packing Order #o2"),
    Staff(id="s3", name="Vikram", role="Delivery", status="offline"),
]

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"message": "ShopMind Backend is Running! 🚀"}

@app.get("/inventory", response_model=List[InventoryItem])
def get_inventory():
    return inventory_db

@app.get("/orders", response_model=List[Order])
def get_orders():
    return orders_db

@app.get("/staff", response_model=List[Staff])
def get_staff():
    return staff_db

@app.get("/recommendations", response_model=List[Recommendation])
def get_recommendations():
    """
    Triggers the AI Agent to analyze current state and return advice.
    """
    recs = agent.analyze(inventory_db, orders_db, staff_db)
    return recs

# Simple actions to make the demo interactive

@app.post("/orders/{order_id}/complete")
def complete_order(order_id: str):
    for order in orders_db:
        if order.id == order_id:
            order.status = "completed"
            return {"message": "Order completed"}
    raise HTTPException(status_code=404, detail="Order not found")

@app.post("/inventory/{item_id}/restock")
def restock_item(item_id: str, amount: int = 10):
    for item in inventory_db:
        if item.id == item_id:
            item.quantity += amount
            return {"message": f"Restocked {item.name}"}
    raise HTTPException(status_code=404, detail="Item not found")

