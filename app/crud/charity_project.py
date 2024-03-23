from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpgrade,
)
from app.models import Donation
from app.api.services.Invest import investing


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(self.model.id).where(self.model.name == project_name)
        )
        return db_project_id.scalars().first()

    async def create_project(
        self,
        project: CharityProjectCreate,
        session: AsyncSession,
    ):

        charity_project = await investing(project, session, Donation)

        new_charity_project = await self.create(
            CharityProjectUpgrade(**charity_project), session
        )
        return new_charity_project


charity_project_crud = CRUDCharityProject(CharityProject)
