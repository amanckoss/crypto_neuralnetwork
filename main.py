import random
import time
import db_api
from decimal import Decimal

with db_api.con:
    db_api.get_orders()
    db_api.close_order(363.61)