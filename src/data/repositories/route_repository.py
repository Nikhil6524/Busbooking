from sqlalchemy import select
from data.models.postgres.route import Route


class RouteRepository:

    async def create_route(self, db, route_data):
        route = Route(**route_data)
        db.add(route)
        await db.commit()
        await db.refresh(route)
        return route

    async def search_routes(self, db, source, destination):
        result = await db.execute(
            select(Route).where(
                Route.source == source,
                Route.destination == destination
            )
        )
        return result.scalars().all()