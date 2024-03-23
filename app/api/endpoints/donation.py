from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB


router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={
        'user_id',
        'invested_amount',
        'fully_invested',
        'close_date',
    },
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):

    new_donation = await donation_crud.create_donation(donation, session, user)

    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
)
async def get_all_donation(session: AsyncSession = Depends(get_async_session)):
    '''Только для суперюзеров.'''
    donation = await donation_crud.get_multi(session)
    return donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={
        'user_id',
        'invested_amount',
        'fully_invested',
        'close_date',
    },
)
async def get_my_donation(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    '''Получает список всех бронирований для текущего пользователя.'''
    reservations = await donation_crud.get_by_user(user, session)
    return reservations
