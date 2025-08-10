from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi import HTTPException
app = FastAPI()

# Example product data
products = [
    {"product_id": 1, "name": "Laptop", "category": "electronics", "price": 1200},
    {"product_id": 2, "name": "Headphones", "category": "electronics", "price": 150},
    {"product_id": 3, "name": "Shirt", "category": "clothing", "price": 30},
    {"product_id": 4, "name": "Shoes", "category": "clothing", "price": 80},
    {"product_id": 5, "name": "Coffee Maker", "category": "home", "price": 100}
]

class Product(BaseModel):
    product_id: Optional[int] = None
    name: str
    category: str
    price: int

@app.get("/products", response_model=List[Product])
def get_products(category: str = None, max_price: float = None):
    #all products
    filtered_products = products

    if category:
        temp_list = []
        for p in filtered_products:
            if p["category"] == category:
                temp_list.append(p)
        filtered_products = temp_list

    if max_price is not None:
        temp_list = []
        for p in filtered_products:
            if p['price'] <= max_price:
                temp_list.append(p)

        filtered_products = temp_list

    return filtered_products

@app.post('/products', response_model=Product)
def post_product(product: Product):
    product_data = product.model_dump()
    if products:
        max_id = max(p["product_id"] for p in products if "product_id" in p and p["product_id"] is not None)
        product_data['product_id'] = max_id + 1
    else:
        product_data['product_id'] = 1
    products.append(product_data)
    return product_data


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: Product):
    for idx, existing_product in enumerate(products):
        if existing_product["product_id"] == product_id:
            updated_product = product_update.model_dump()
            updated_product["product_id"] = product_id  # Always use path variable, ignore body
            products[idx] = updated_product
            return updated_product
    raise HTTPException(status_code=404, detail="Product not found")

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None

@app.patch("/products/{product_id}")
def patch_product(product_id: int, product: ProductUpdate):
    for p in products:
        if p['product_id'] == product_id:
            if product.name is not None:
                p["name"] = product.name
            if product.price is not None:
                p["price"] = product.price
            return p
    raise HTTPException(status_code=404, detail='Product Not Found')

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for idx, existing_product in enumerate(products):
        if existing_product["product_id"] == product_id:
            products.pop(idx)
            return {"detail": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")

orders = [
    {"id": 1, "customer_id": 5, "status": "shipped", "items": [1, 2]},
    {"id": 2, "customer_id": 5, "status": "pending", "items": [3]},
    {"id": 3, "customer_id": 7, "status": "shipped", "items": [4, 5]}
]

class Order(BaseModel):
    id: Optional[int]
    customer_id:Optional[int]
    status:str
    items:List[int]

@app.get("/customers/orders", response_model=List[Order])
def get_orders(customer_id: Optional[int] = None, status: Optional[str] = None):
    f_orders = []
    if customer_id is None and status is None:
        return orders

    for o in orders:
        if o["customer_id"] == customer_id and o["status"] == status:
            f_orders.append(o)
        elif o["customer_id"] == customer_id and status == None:
            f_orders.append(o)
        elif customer_id == None and o['status'] == status:
            f_orders.append(o)
    return f_orders

@app.post("/customers/{customer_id}/orders", response_model=Order)
def post_order(customer_id: int, order: Order):
    order_data = order.model_dump()
    order_data["customer_id"] = customer_id
    if orders:
        max_id = max(o["id"] for o in orders if "id" in o and o["id"] is not None)
        order_data["id"] = max_id + 1
    else:
        order_data["id"] = 1
    orders.append(order_data)
    return order_data


@app.put("/customers/{customer_id}/orders/{order_id}", response_model=Order)
def update_order(customer_id: int, order_id: int, order_update: Order):
    for idx, existing_order in enumerate(orders):
        if existing_order["id"] == order_id and existing_order["customer_id"] == customer_id:
            # Ensure path customer_id and id match the update data (optional)
            if order_update.id is not None and order_update.id != order_id:
                raise HTTPException(status_code=400, detail="Order ID mismatch")
            if hasattr(order_update, 'customer_id') and getattr(order_update, 'customer_id', None) != customer_id:
                raise HTTPException(status_code=400, detail="Customer ID mismatch")

            updated_order = order_update.model_dump()
            updated_order["customer_id"] = customer_id  # Ensure correct customer_id
            orders[idx] = updated_order
            return updated_order
    raise HTTPException(status_code=404, detail="Order not found")

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    items: Optional[List[int]] = None

@app.patch("/customers/{customer_id}/orders/{order_id}")
def patch_order(customer_id: int, order_id: int, order: OrderUpdate):
    for o in orders:
        if o['customer_id'] == customer_id and o['id'] == order_id:
            if order.status is not None:
                o['status'] = order.status
            if order.items is not None:
                o['items'] = order.items
            return o
    raise HTTPException(status_code=404, detail="Order not found")

@app.delete("/customers/{customer_id}/orders/{order_id}")
def delete_order(customer_id: int, order_id: int):
    for idx, existing_order in enumerate(orders):
        if existing_order["id"] == order_id and existing_order["customer_id"] == customer_id:
            orders.pop(idx)
            return {"detail": "Order deleted"}
    raise HTTPException(status_code=404, detail="Order not found")