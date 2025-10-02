import time
from worker import celery_app
from core.config import settings
from model.models import ProductOrder as Order
from sqlmodel import create_engine, select, Session

# Create the engine once at the module level
engine = create_engine(settings.DATABASE_SYNC_URL, echo=True)

STAGES = ["Packaging", "Shipping", "Delivered"]

@celery_app.task
def process_order(order_id: int):
    """
    A Celery task to update the status of an order through
    a series of simulated stages.
    """
    # Use a session context manager to ensure the session is always closed
    with Session(engine) as session:
        # 1. Fetch the order from the database
        order = session.exec(select(Order).where(Order.id == order_id)).first()

        if not order:
            print(f"Order with ID {order_id} not found.")
            return {"error": "Order not found"}

        # 2. Iterate through the stages and update the database
        for stage in STAGES:
            # Simulate a time-consuming operation
            time.sleep(10)
            
            # Update the order's status
            order.status = stage
            
            # Add the updated object to the session
            session.add(order)
            
            # Commit the changes to the database. This happens at each stage.
            session.commit()
            
            # Refresh the object to get the latest state from the database
            session.refresh(order)
            
            print(f"Order {order.id} status updated to: {order.status}")
    
    return {"order_id": order.id, "final_status": order.status}