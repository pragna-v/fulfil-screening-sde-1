from .models import Product

def get_products(session, skip: int = 0, limit: int = 25, filters: dict = None):
    q = session.query(Product)
    if filters:
        if 'sku' in filters:
            q = q.filter(Product.sku.ilike(f"%{filters['sku']}%"))
        if 'name' in filters:
            q = q.filter(Product.name.ilike(f"%{filters['name']}%"))
    return q.offset(skip).limit(limit).all()
