from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.entrypoint_db import get_async_session
from src.user.authorization.router import get_user
from src.video.router import get_last_videos, get_videos_this_user, get_viewed_videos, get_liked_videos_main, get_video
from src.user.authorization.current_user import current_user, current_active_user
from src.interactions.router import get_comments
from src.pages.utils import get_link_account_img
from src.interactions.utils import check_like, check_sub

router = APIRouter(
    prefix='/page',
    tags=['Page']
)

templates = Jinja2Templates(directory="src/templates")

await_count = 5
await_count_main = 6

links = {
    'main': "http://127.0.0.1:8000/page/main",
    'account': "http://127.0.0.1:8000/page/account",
    'part_link_video': "http://127.0.0.1:8000/page/video_page?id_video=",
    'part_link_user': "http://127.0.0.1:8000/page/user?id_user="
}


@router.get('/main')
async def get_main_page(request: Request,
                        user=Depends(current_user),
                        db_session: AsyncSession = Depends(get_async_session)):

    link_img = get_link_account_img(user)

    videos = await get_last_videos(await_count_main, 0, db_session)

    return templates.TemplateResponse("main/main.html", {"request": request,
                                                         'links': links,
                                                         "videos": videos,
                                                         "link_user_img": link_img,
                                                         "user": user,
                                                         'await_count': await_count_main})


@router.get('/main/more')
async def get_main_fragment(request: Request,
                            offset: int,
                            db_session: AsyncSession = Depends(get_async_session)):

    videos = await get_last_videos(await_count_main, offset, db_session)

    return templates.TemplateResponse("main/fragment.html", {"request": request,
                                                             "videos": videos,
                                                             'plv': links['part_link_video']})


@router.get('/account')
async def get_account_page(request: Request,
                           user=Depends(current_active_user),
                           db_session: AsyncSession = Depends(get_async_session)):

    user_videos = await get_videos_this_user(user.id, await_count, 0, db_session)

    return templates.TemplateResponse("account/account.html", {"request": request,
                                                               'links': links,
                                                               "user": user,
                                                               "user_videos": user_videos,
                                                               "await_count": await_count,
                                                               'plv': links['part_link_video'],
                                                               "_bool": True})


@router.get("/account/my_video")
async def get_account_fragment_my_video(request: Request,
                                        offset: int,
                                        user=Depends(current_active_user),
                                        db_session: AsyncSession = Depends(get_async_session)):

    videos = await get_videos_this_user(user.id, await_count, offset, db_session)

    return templates.TemplateResponse("account/fragment.html", {"request": request,
                                                                "videos": videos,
                                                                'plv': links['part_link_video'],
                                                                '_bool': True})


@router.get("/account/history")
async def get_account_fragment_history(request: Request,
                                       offset: int,
                                       user=Depends(current_active_user),
                                       db_session: AsyncSession = Depends(get_async_session)):

    videos = await get_viewed_videos(await_count, offset, user, db_session)

    return templates.TemplateResponse("account/fragment.html", {"request": request,
                                                                "videos": videos,
                                                                'plv': links['part_link_video']})


@router.get("/account/liked_video")
async def get_account_fragment_liked(request: Request,
                                     offset: int,
                                     user=Depends(current_active_user),
                                     db_session: AsyncSession = Depends(get_async_session)):

    videos = await get_liked_videos_main(await_count, offset, user, db_session)

    return templates.TemplateResponse("account/fragment.html", {"request": request,
                                                                "videos": videos,
                                                                'plv': links['part_link_video']})


@router.get('/user')
async def get_user_page(request: Request,
                        id_user: int,
                        account=Depends(current_user),
                        db_session: AsyncSession = Depends(get_async_session)):

    if account is not None:
        if account.id == id_user:
            return await get_account_page(request, account, db_session)
        else:
            is_sub = await check_sub(id_user, account, db_session)

    user = await get_user(id_user, db_session)

    user_videos = await get_videos_this_user(user.id, await_count, 0, db_session)

    return templates.TemplateResponse("account/user.html", {"request": request,
                                                            'links': links,
                                                            "user": user,
                                                            "user_videos": user_videos,
                                                            "await_count": await_count,
                                                            'plv': links['part_link_video'],
                                                            'is_sub': is_sub})


@router.get("/user/videos")
async def get_user_fragment_videos(request: Request,
                                   offset: int,
                                   id_user: int,
                                   db_session: AsyncSession = Depends(get_async_session)):

    videos = await get_videos_this_user(id_user, await_count, offset, db_session)

    return templates.TemplateResponse("account/fragment.html", {"request": request,
                                                                "videos": videos,
                                                                'plv': links['part_link_video']})


@router.get("/video_page")
async def get_video_page(id_video: str,
                         request: Request,
                         account=Depends(current_user),
                         db_session: AsyncSession = Depends(get_async_session)):

    link_img = get_link_account_img(account)

    video = await get_video(id_video, account, db_session)

    auther = await get_user(video['id_auther'], db_session)

    is_liked = await check_like(id_video, account, db_session)
    is_sub = await check_sub(video['id_auther'], account, db_session)
    print(is_sub)
    print(is_liked)

    comments = await get_comments(await_count, 0, id_video, db_session)

    return templates.TemplateResponse("video/video_page.html", {"request": request,
                                                                'links': links,
                                                                "video": video,
                                                                "auther": auther,
                                                                "comments": comments,
                                                                "link_img": link_img,
                                                                "plu": links['part_link_user'],
                                                                "is_liked": is_liked,
                                                                "is_sub": is_sub,
                                                                "something": account})


@router.get("/video_page/comments")
async def get_video_page_fragment_comments(request: Request,
                                           offset: int,
                                           id_video: str,
                                           db_session: AsyncSession = Depends(get_async_session)):

    comments = await get_comments(await_count, offset, id_video, db_session)

    return templates.TemplateResponse("video/fragment_comments.html", {"request": request,
                                                                       "comments": comments,
                                                                       "plu": links['part_link_user']})
