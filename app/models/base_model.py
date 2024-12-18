import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import (
    Column,
    DateTime
)
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4
    )

    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    @classmethod
    async def list(cls, db: AsyncSession, filters: dict = None):
        q = select(cls)
        if filters:
            q = q.filter_by(**filters)
        res = await db.execute(q)
        return res.scalars().all()
    
    @classmethod
    async def insert(cls, db: AsyncSession, **kwargs):
        ins = cls(**kwargs)
        db.add(ins)

        await db.flush()

        await db.commit()
        await db.refresh(ins)
        return ins
    
    @classmethod
    async def get_one(cls, db: AsyncSession, filters: dict, **kwargs):
        res = await db.execute(select(cls).filter_by(**filters))
        ins = res.scalar_one_or_none()
        return ins
    
    @classmethod
    async def update(cls, db: AsyncSession, filters: dict, **kwargs):
        q = select(cls).filter_by(**filters)
        res = await db.execute(q)
        ins = res.scalar_one_or_none()
        
        if not ins:
            return None
        
        for k, v in kwargs.items():
            if hasattr(ins, k):
                setattr(ins, k, v)
        await db.commit()
        await db.flush()
        return ins
    
    @classmethod
    async def delete(cls, db: AsyncSession, filters: dict):

        if not filters:
            raise Exception("no filters specified for deletion")
        
        q = select(cls).filter_by(**filters)
        res = await db.execute(q)
        ins = res.scalar_one_or_none()

        if not ins:
            return None
        
        await db.delete(ins)
        await db.commit()
        await db.flush()
        return ins

