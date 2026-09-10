from fastapi import APIRouter, HTTPException, Depends

from src.dependencies.database import DBDep
from src.dependencies.pagination import PaginationDep
from src.dependencies.auth import require_admin
from src.schemas.user import UserPrivillege

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])

@router.get("/")
async def get_list_of_users(
    db: DBDep,
    pagination: PaginationDep
):
    users = await db.user.get_all(limit=pagination.per_page, offset=(pagination.page-1)*pagination.per_page)
    return users


@router.patch("/{user_id}")
async def privilege_user(
    db: DBDep,
    user_id: int
):
    user = UserPrivillege(super_user=True)
    privileged_user = await db.user.edit(data=user, exclude_unset=True, user_id=user_id)
    if not privileged_user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.commit()
    return {"status": "OK", "detail": "User promoted to admin"}


@router.delete("/{user_id}")
async def delete_user(
    db: DBDep,
    user_id: int
):    
    deleted_user = await db.user.delete_filtered(user_id=user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.commit()
    return {"status": "OK", "detail": "User deleted"}