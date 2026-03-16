import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Group, User, UserGroup


async def list_groups(db: AsyncSession) -> list[Group]:
    result = await db.execute(select(Group).order_by(Group.name))
    return list(result.scalars().all())


async def create_group(
    db: AsyncSession, name: str, description: str | None = None
) -> Group:
    group = Group(name=name, description=description)
    db.add(group)
    await db.flush()
    return group


async def get_group(db: AsyncSession, group_id: str) -> Group | None:
    result = await db.execute(
        select(Group)
        .where(Group.id == uuid.UUID(group_id))
        .options(selectinload(Group.memberships))
    )
    return result.scalar_one_or_none()


async def delete_group(db: AsyncSession, group_id: str) -> bool:
    group = await get_group(db, group_id)
    if group is None:
        return False
    await db.delete(group)
    await db.flush()
    return True


async def add_member(db: AsyncSession, group_id: str, user_id: str) -> None:
    """Add user to group. Raises ValueError if not found, LookupError if duplicate."""
    group = await db.get(Group, uuid.UUID(group_id))
    if group is None:
        raise ValueError(f"Group {group_id} not found")

    user = await db.get(User, uuid.UUID(user_id))
    if user is None:
        raise ValueError(f"User {user_id} not found")

    existing = await db.execute(
        select(UserGroup).where(
            UserGroup.group_id == uuid.UUID(group_id),
            UserGroup.user_id == uuid.UUID(user_id),
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise LookupError("User is already a member of this group")

    membership = UserGroup(user_id=uuid.UUID(user_id), group_id=uuid.UUID(group_id))
    db.add(membership)
    await db.flush()


async def remove_member(db: AsyncSession, group_id: str, user_id: str) -> bool:
    result = await db.execute(
        select(UserGroup).where(
            UserGroup.group_id == uuid.UUID(group_id),
            UserGroup.user_id == uuid.UUID(user_id),
        )
    )
    membership = result.scalar_one_or_none()
    if membership is None:
        return False
    await db.delete(membership)
    await db.flush()
    return True


async def ensure_admin_group(db: AsyncSession) -> Group:
    """Create admin group if it doesn't exist."""
    result = await db.execute(select(Group).where(Group.name == "admin"))
    group = result.scalar_one_or_none()
    if group is None:
        group = Group(name="admin", description="Administrators")
        db.add(group)
        await db.commit()
    return group
