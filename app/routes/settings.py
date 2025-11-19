from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.models.settings import Settings
from app.schemas.settings_schema import SettingsUpdate, SettingsResponse
from datetime import datetime

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("", response_model=SettingsResponse)
async def get_settings(session: Session = Depends(get_session)):
    statement = select(Settings).where(Settings.user_id == 1)
    settings = session.exec(statement).first()
    
    if not settings:
        settings = Settings(user_id=1)
        session.add(settings)
        session.commit()
        session.refresh(settings)
    
    return settings


@router.put("", response_model=SettingsResponse)
async def update_settings(
    settings_update: SettingsUpdate,
    session: Session = Depends(get_session)
):
    statement = select(Settings).where(Settings.user_id == 1)
    settings = session.exec(statement).first()
    
    if not settings:
        settings = Settings(user_id=1)
        session.add(settings)
    
    update_data = settings_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(settings, key, value)
    
    settings.updated_at = datetime.utcnow()
    
    session.add(settings)
    session.commit()
    session.refresh(settings)
    
    return settings
