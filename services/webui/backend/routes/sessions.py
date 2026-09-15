from fastapi import APIRouter, Depends, HTTPException, Request, Query
from typing import Optional

from core.security import get_current_user, get_current_moderator_user
from models.session import SessionCreate, SessionUpdate
from services.audit import AuditService
from services.features import FeatureService
from services.session import SessionService

router = APIRouter(prefix="/sessions")

@router.get("")
async def get_sessions(
    status: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """Get all gaming sessions"""
    if not FeatureService.is_enabled('gaming_sessions'):
        raise HTTPException(status_code=403, detail="Gaming sessions are disabled")

    return SessionService.get_sessions(status)

@router.post("")
async def create_session(
    session_data: SessionCreate,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Create a new gaming session"""
    if not FeatureService.is_enabled('gaming_sessions'):
        raise HTTPException(status_code=403, detail="Gaming sessions are disabled")

    session = SessionService.create_session(
        title=session_data.title,
        description=session_data.description,
        orchestrator_id=session_data.orchestrator_id,
        server_uid=session_data.server_uid,
        scheduled_time=session_data.scheduled_time,
        duration_minutes=session_data.duration_minutes,
        created_by=current_user['id']
    )

    # Log session creation
    AuditService.log(
        user_id=current_user['id'],
        username=current_user['username'],
        action_type='create',
        category='session',
        target_type='session',
        target_id=session['id'],
        details=f"Created gaming session: {session_data.title}",
        ip_address=request.client.host if request.client else None
    )

    return session

@router.put("/{session_id}")
async def update_session(
    session_id: str,
    session_data: SessionUpdate,
    request: Request,
    current_user: dict = Depends(get_current_moderator_user)
):
    """Update a gaming session"""
    if not SessionService.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")

    updates = {k: v for k, v in session_data.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No updates provided")

    updated = SessionService.update_session(session_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Session not found")

    # Log session update
    AuditService.log(
        user_id=current_user['id'],
        username=current_user['username'],
        action_type='update',
        category='session',
        target_type='session',
        target_id=session_id,
        details=f"Updated session fields: {', '.join(updates.keys())}",
        ip_address=request.client.host if request.client else None
    )

    return updated

@router.delete("/{session_id}")
async def delete_session(
    session_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Delete a gaming session"""
    session_dict = SessionService.get_session_by_id(session_id)
    if not session_dict:
        raise HTTPException(status_code=404, detail="Session not found")

    # Only creator or moderator/admin can delete
    if session_dict['created_by'] != current_user['id'] and current_user['role'] not in ['admin', 'moderator']:
        raise HTTPException(status_code=403, detail="Not authorized to delete this session")

    SessionService.delete_session(session_id)

    # Log session deletion
    AuditService.log(
        user_id=current_user['id'],
        username=current_user['username'],
        action_type='delete',
        category='session',
        target_type='session',
        target_id=session_id,
        details=f"Deleted gaming session: {session_dict['title']}",
        ip_address=request.client.host if request.client else None
    )

    return {"message": "Session deleted successfully"}

@router.post("/{session_id}/rsvp")
async def rsvp_session(
    session_id: str,
    status: str = Query("attending"),
    current_user: dict = Depends(get_current_user)
):
    """RSVP to a gaming session"""
    if status not in ['attending', 'maybe', 'declined']:
        raise HTTPException(status_code=400, detail="Invalid RSVP status")

    if not SessionService.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")

    SessionService.upsert_rsvp(session_id, current_user['id'], status)

    return {"message": f"RSVP updated to {status}"}

@router.delete("/{session_id}/rsvp")
async def cancel_rsvp(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Cancel RSVP to a gaming session"""
    if not SessionService.cancel_rsvp(session_id, current_user['id']):
        raise HTTPException(status_code=404, detail="RSVP not found")

    return {"message": "RSVP cancelled"}
