from pydantic import BaseModel
from typing import List, Optional, Literal

# OMG I love Pydantic, it makes validation so easy! 😍

class InventoryItem(BaseModel):
    id: str
    name: str
    quantity: int
    price: float
    category: str
    low_stock_threshold: int = 10 # Default alert level

class Order(BaseModel):
    id: str
    customer_name: str
    items: List[str] # List of Item IDs
    status: Literal['pending', 'processing', 'completed', 'cancelled']
    total_amount: float
    priority: Literal['normal', 'high'] = 'normal'

class Staff(BaseModel):
    id: str
    name: str
    role: str
    status: Literal['available', 'busy', 'offline']
    current_task: Optional[str] = None

class Recommendation(BaseModel):
    id: str
    type: Literal['restock', 'staff_allocation', 'promotion', 'alert']
    message: str
    priority: Literal['low', 'medium', 'high', 'critical']
    action_item_id: Optional[str] = None # ID of item/staff involved
    timestamp: str
