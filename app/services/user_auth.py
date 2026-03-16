import uuid
from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import db_settings
from app.db.models import Group, User, UserGroup

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def _hash_password(password: str) -> str:
    return pwd_context.hash(password)


def _verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=db_settings.jwt_expire_minutes)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, db_settings.jwt_secret, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str:
    """Decode token and return user_id (sub). Raises JWTError on failure."""
    payload = jwt.decode(token, db_settings.jwt_secret, algorithms=[ALGORITHM])
    sub: str | None = payload.get("sub")
    if sub is None:
        raise JWTError("Missing sub claim")
    return sub


async def get_user_with_groups(
    db: AsyncSession, user_id: str
) -> tuple[User, list[str]] | None:
    """Load user + list of group names. Returns None if user not found."""
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        return None

    groups_result = await db.execute(
        select(Group.name)
        .join(UserGroup, UserGroup.group_id == Group.id)
        .where(UserGroup.user_id == user.id)
    )
    group_names = [row[0] for row in groups_result.all()]
    return user, group_names


async def create_user(
    db: AsyncSession,
    username: str,
    password: str,
    email: str | None = None,
) -> User:
    """Create a local user. First user automatically gets admin group."""
    hashed = _hash_password(password)
    user = User(
        username=username,
        email=email,
        hashed_password=hashed,
    )
    db.add(user)
    await db.flush()  # get user.id

    # Check if this is the first local user (no hashed_password is null = OIDC users)
    count_result = await db.execute(
        select(func.count(User.id)).where(User.hashed_password.isnot(None))
    )
    local_user_count = count_result.scalar_one()

    if local_user_count == 1:  # this is the first local user
        # ensure admin group exists
        admin_group = await _get_or_create_admin_group(db)
        membership = UserGroup(user_id=user.id, group_id=admin_group.id)
        db.add(membership)

    await db.flush()
    return user


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None or user.hashed_password is None:
        return None
    if not _verify_password(password, user.hashed_password):
        return None
    return user


async def upsert_oidc_user(db: AsyncSession, sub: str, name: str) -> User:
    """Insert or update user identified by external_id (OIDC sub)."""
    stmt = (
        pg_insert(User)
        .values(
            external_id=sub,
            username=name or sub,
        )
        .on_conflict_do_update(
            index_elements=["external_id"],
            set_={"username": name or sub},
        )
        .returning(User)
    )
    result = await db.execute(stmt)
    await db.flush()
    return result.scalar_one()


async def _get_or_create_admin_group(db: AsyncSession) -> Group:
    result = await db.execute(select(Group).where(Group.name == "admin"))
    group = result.scalar_one_or_none()
    if group is None:
        group = Group(name="admin", description="Administrators")
        db.add(group)
        await db.flush()
    return group
