import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.dependencies.auth import require_admin
from app.models.auth import UserInfo
from app.models.groups import GroupCreate, GroupResponse, MemberAdd, MemberResponse
from app.services import groups as group_svc

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("", response_model=list[GroupResponse])
async def list_groups(
    db: AsyncSession = Depends(get_db),
    _admin: UserInfo = Depends(require_admin),
) -> list[GroupResponse]:
    groups = await group_svc.list_groups(db)
    return [GroupResponse.model_validate(g) for g in groups]


@router.post("", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    body: GroupCreate,
    db: AsyncSession = Depends(get_db),
    _admin: UserInfo = Depends(require_admin),
) -> GroupResponse:
    try:
        group = await group_svc.create_group(db, body.name, body.description)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Group '{body.name}' already exists",
        )
    return GroupResponse.model_validate(group)


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: str,
    db: AsyncSession = Depends(get_db),
    _admin: UserInfo = Depends(require_admin),
) -> GroupResponse:
    group = await group_svc.get_group(db, group_id)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group not found"
        )
    return GroupResponse.model_validate(group)


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: str,
    db: AsyncSession = Depends(get_db),
    _admin: UserInfo = Depends(require_admin),
) -> None:
    deleted = await group_svc.delete_group(db, group_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group not found"
        )


@router.post("/{group_id}/members", response_model=MemberResponse)
async def add_member(
    group_id: str,
    body: MemberAdd,
    db: AsyncSession = Depends(get_db),
    _admin: UserInfo = Depends(require_admin),
) -> MemberResponse:
    try:
        await group_svc.add_member(db, group_id, body.user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return MemberResponse(user_id=body.user_id, group_id=group_id)


@router.delete("/{group_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    group_id: str,
    user_id: str,
    db: AsyncSession = Depends(get_db),
    _admin: UserInfo = Depends(require_admin),
) -> None:
    removed = await group_svc.remove_member(db, group_id, user_id)
    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found",
        )
