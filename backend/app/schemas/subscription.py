from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SubscriptionBase(BaseModel):
    subscription_type: str = "email"
    endpoint: Optional[str] = None


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionResponse(SubscriptionBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    last_sent_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
