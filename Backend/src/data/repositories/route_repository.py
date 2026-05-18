from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.models.postgres.route import Route


class RouteRepository:

    async def create_route(self, db: AsyncSession, route_data: dict):
        route = Route(**route_data)
        db.add(route)
        await db.commit()
        await db.refresh(route)
        return route

    async def get_route_by_id(self, db: AsyncSession, route_id):
        result = await db.execute(
            select(Route).where(Route.id == route_id)
        )
        return result.scalar_one_or_none()

    async def update_route(self, db: AsyncSession, route_id, route_data: dict):
        route = await self.get_route_by_id(db, route_id)
        if not route:
            return None

        for key, value in route_data.items():
            setattr(route, key, value)

        await db.commit()
        await db.refresh(route)
        return route

    async def search_routes(self, db: AsyncSession, source, destination):
        result = await db.execute(
            select(Route).where(
                Route.source == source,
                Route.destination == destination
            )
        )
        return result.scalars().all()