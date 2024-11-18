from api.users import router as users_router
from api.bank_accounts import router as bank_accounts_router
from api.users_roles import router as users_roles_router
from api.payments import router as payments_router
from api.expenses import router as expenses_router
from api.roles import router as roles_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(users_router, tags=["Users"], prefix="/users")
router.include_router(users_roles_router, tags=["Users_Roles"], prefix="/users_roles")
router.include_router(roles_router, tags=["Roles"], prefix="/roles")
router.include_router(
    bank_accounts_router, tags=["Bank accounts"], prefix="/bank_accounts"
)
router.include_router(payments_router, tags=["Payments"], prefix="/payments")
router.include_router(expenses_router, tags=["Expenses"], prefix="/expenses")
