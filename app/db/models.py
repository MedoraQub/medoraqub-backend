# Import all models so SQLAlchemy can register them

from app.modules.users.models import User
from app.modules.pharmacy.models import Pharmacy
from app.modules.medicines.models import Medicine
from app.modules.inventory.models import Inventory
from app.modules.cart.models import Cart
from app.modules.orders.models import Order
from app.modules.orderItem.models import OrderItem
from app.modules.address.models import Address