from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.api.validators import (
    check_name_duplicate,
    check_charity_project_exists,
    check_full_amount_invested_amount,
    check_delete,
)
from app.schemas.charity_project import (
    CharityProjectResponses,
    CharityProjectCreate,
    CharityProjectUpdate,
)


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectResponses,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    '''Только для суперюзеров.'''
    if charity_project.name is not None:
        await check_name_duplicate(charity_project.name, session)

    new_charity_project = await charity_project_crud.create_project(
        charity_project, session
    )
    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProjectResponses],
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session),
):
    all_project = await charity_project_crud.get_multi(session)
    return all_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectResponses,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    '''Только для суперюзеров.'''
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )

    await check_name_duplicate(obj_in.name, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Проект полностью проинвестирован и не может быть обновлен.',
        )
    await check_full_amount_invested_amount(
        charity_project_id, obj_in, session
    )

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectResponses,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    '''Только для суперюзеров.'''
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )

    await check_delete(charity_project)

    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
