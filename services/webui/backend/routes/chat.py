from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query, Request
import logging

from core.security import get_current_user, get_current_moderator_user, decode_token
from core.websocket import chat_manager
from services.audit import AuditService
from services.chat import ChatService
from services.features import FeatureService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat")

@router.get("/messages")
async def get_messages(
    limit: int = Query(50, le=200),
    current_user: dict = Depends(get_current_user)
):
    """Get chat messages (HTTP fallback)"""
    if not FeatureService.is_enabled('chat'):
        raise HTTPException(status_code=403, detail="Chat is disabled")

    return ChatService.get_recent_messages(limit)

@router.post("/messages")
async def send_message(
    message: str = Query(..., max_length=1000),
    current_user: dict = Depends(get_current_user)
):
    """Send a chat message (HTTP fallback)"""
    if not FeatureService.is_enabled('chat'):
        raise HTTPException(status_code=403, detail="Chat is disabled")

    if current_user.get('is_chat_banned'):
        raise HTTPException(status_code=403, detail="You are banned from chat")

    message = message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    created = ChatService.create_message(current_user['id'], message)
    created['username'] = current_user['username']

    # Broadcast to WebSocket clients
    await chat_manager.broadcast({
        "type": "chat_message",
        "message": created
    })

    return created

@router.delete("/messages/{message_id}")
async def delete_message(
    message_id: str,
    request: Request,
    current_user: dict = Depends(get_current_moderator_user)
):
    """Delete a chat message (moderator+)"""
    msg = ChatService.get_message_by_id(message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")

    ChatService.delete_message(message_id)

    # Broadcast deletion to clients
    await chat_manager.broadcast({
        "type": "message_deleted",
        "message_id": message_id
    })

    # Log message deletion
    AuditService.log(
        user_id=current_user['id'],
        username=current_user['username'],
        action_type='delete',
        category='chat',
        target_type='message',
        target_id=message_id,
        details='Deleted chat message',
        ip_address=request.client.host if request.client else None
    )

    return {"message": "Message deleted"}

@router.delete("/clear")
async def clear_all_chat(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Clear all chat messages (admin only)"""
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")

    count = ChatService.clear_all()

    # Broadcast chat cleared
    await chat_manager.broadcast({
        "type": "chat_cleared"
    })

    # Log chat clear
    AuditService.log(
        user_id=current_user['id'],
        username=current_user['username'],
        action_type='clear',
        category='chat',
        details=f'Cleared all chat messages ({count} messages)',
        ip_address=request.client.host if request.client else None
    )

    return {"message": f"Cleared {count} messages"}

@router.get("/online")
async def get_online_users(current_user: dict = Depends(get_current_user)):
    """Get list of online users"""
    if not FeatureService.is_enabled('online_users'):
        return []

    online_ids = chat_manager.get_online_users()

    return ChatService.get_users_by_ids(online_ids)
