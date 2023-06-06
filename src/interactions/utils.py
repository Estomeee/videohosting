from src.entrypoint_db import get_async_session
from src.user.authorization.model import User, AsyncSession
from fastapi import Depends
from src.user.authorization.current_user import current_active_user
from sqlalchemy import insert
from src.interactions.model import view as view_table


def add_view(id_video: int,
             id_user: int,
             user: User = Depends(current_active_user),
             db_session: AsyncSession = Depends(get_async_session)):


    queue = insert(view_table).values(id_video=id_video,
                                      id_user=id_user)

    comment = Comment(comment=comment_text, video_id=video_id, user_id=user.id)
    db_session.add(comment)
    await db_session.commit()
    return CommentInfo(comment_id=comment.comment_id,
                       username=user.username,
                       video_id=video_id,
                       create_at=comment.create_at,
                       comment=comment_text)
