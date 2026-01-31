from typing import List
from models import InventoryItem, Order, Staff, Recommendation
import datetime

class ShopMindAgent:
    """
    This is the BRAIN! 🧠
    It looks at the data and decides what to do.
    """
    def __init__(self):
        # In a real hackathon, I'd put API keys here but I'm broke lol
        pass

    def analyze(self, inventory: List[InventoryItem], orders: List[Order], staff: List[Staff]) -> List[Recommendation]:
        recommendations = []
        now = datetime.datetime.now().isoformat()

        # 1. Check Inventory (The basics)
        for item in inventory:
            if item.quantity < item.low_stock_threshold:
                rec = Recommendation(
                    id=f"rec_restock_{item.id}_{now}",
                    type="restock",
                    message=f"⚠️ Low Stock Alert: {item.name} is down to {item.quantity}! Order more ASAP.",
                    priority="high",
                    action_item_id=item.id,
                    timestamp=now
                )
                recommendations.append(rec)

        # 2. Check Staffing (The manager part)
        active_orders = [o for o in orders if o.status in ['pending', 'processing']]
        available_staff = [s for s in staff if s.status == 'available']
        
        if len(active_orders) > 5 and len(available_staff) == 0:
             rec = Recommendation(
                id=f"rec_staff_{now}",
                type="staff_allocation",
                message="🔥 Too many orders! We need all hands on deck. Call in backup!",
                priority="critical",
                timestamp=now
            )
             recommendations.append(rec)
        elif len(active_orders) > 0 and len(available_staff) > 0:
             # Auto-assign logic (Simulated)
             staff_member = available_staff[0]
             rec = Recommendation(
                id=f"rec_assign_{now}",
                type="staff_allocation",
                message=f"✅ Optimization: Assign {staff_member.name} to Order #{active_orders[0].id}",
                priority="medium",
                action_item_id=staff_member.id,
                timestamp=now
            )
             recommendations.append(rec)

        # 3. Profit Boosting (The CEO part)
        # Simple heuristic: If lots of people buy something, raise price slightly? 😈 (Just kidding, maybe just feature it)
        high_demand_items = [item for item in inventory if item.quantity < 5 and item.price > 50]
        if high_demand_items:
             rec = Recommendation(
                id=f"rec_promo_{now}",
                type="promotion",
                message=f"💰 {high_demand_items[0].name} is selling fast! Consider a 'Best Seller' tag.",
                priority="low",
                action_item_id=high_demand_items[0].id,
                timestamp=now
            )
             recommendations.append(rec)

        return recommendations
