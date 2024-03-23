from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
    charity_project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        charity_project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(status_code=404, detail='Проект не найден!')
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400, detail='Проект проинвестирован обновить нельзя!'
        )

    return charity_project


async def check_full_amount_invested_amount(
    charity_project_id,
    obj_in,
    session: AsyncSession,
):
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if (
        obj_in.full_amount is not None and
        obj_in.full_amount < charity_project.invested_amount
    ):
        raise HTTPException(
            status_code=400,
            detail='Невозможно установить требуемую сумму меньше уже внесенной.',
        )


async def check_delete(charity_project):

    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400, detail='Нельзя удалить закрытый проект'
        )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='Нельзя удалить проект, в который уже внесены средства',
        )
