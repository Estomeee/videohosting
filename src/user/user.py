from fastapi import APIRouter

router = APIRouter(
    prefix='/User',
    tags=['User']
)


@router.get('/')
def uu():
    return 'result'

@router.get('/')
def uu():
    return 'result'

@router.get('/')
def uu():
    return 'result'

@router.get('/')
def uu():
    return 'result'
