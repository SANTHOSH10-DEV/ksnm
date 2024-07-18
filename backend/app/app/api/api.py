from api.endpoints import ksnm
from api.endpoints import login
from api.endpoints import user
from api.endpoints import cart
from api.endpoints import stock
from api.endpoints import wishlist
from api.endpoints import product
from api.endpoints import master
from api.endpoints import sales
from api.endpoints import salesdetails
from api.endpoints import order
from fastapi import APIRouter
api_router= APIRouter()

api_router.include_router(login.router, tags=["Login"], prefix="/login")
api_router.include_router(ksnm.router, tags=["ksnm"], prefix="/ksnm")
# api_router.include_router(ksnm.router)

api_router.include_router(user.router, tags=["User"], prefix="/user")

api_router.include_router(cart.router, tags=["Cart"], prefix="/cart")

api_router.include_router(stock.router, tags=["Stock"], prefix="/stock")

api_router.include_router(wishlist.router, tags=["Wishlist"], prefix="/stock")

api_router.include_router(product.router, tags=["Product"], prefix="/product")

api_router.include_router(master.router, tags=["Master"], prefix="/master")

api_router.include_router(sales.router, tags=["Sales"], prefix="/sales")

api_router.include_router(salesdetails.router, tags=["SalesDetails"], prefix="")

api_router.include_router(order.router, tags=['Order'], prefix="/order")

