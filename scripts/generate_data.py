import json, random
from pathlib import Path
random.seed(7)
OUT=Path(__file__).parents[1]/"data"; OUT.mkdir(exist_ok=True)
templates=[
 ("Smartphone", "Samsung Galaxy S24 Ultra", ["Samsung Galaxy S24 Ultra"]),("Smartphone", "iPhone 15 Pro", ["iPhone 15 Pro"]),("Phone Case", "Protective Case", ["Samsung Galaxy S24 Ultra","Samsung Galaxy S24","iPhone 15 Pro","Pixel 8"]),("Screen Protector", "Tempered Glass", ["Samsung Galaxy S24 Ultra","Samsung Galaxy S24","iPhone 15 Pro","Pixel 8"]),("Charger", "Fast GaN Charger", []),("USB Cable", "USB-C Braided Cable", []),("Power Bank", "Power Bank 20000mAh", []),("Laptop", "Ultrabook", []),("Laptop Sleeve", "Waterproof Laptop Sleeve", []),("Keyboard", "Wireless Mechanical Keyboard", []),("Mouse", "Ergonomic Wireless Mouse", []),("USB Hub", "7-in-1 USB-C Hub", []),("Headphones", "Noise Cancelling Headphones", []),("Smart Watch", "Fitness Smart Watch", []),("Travel Accessory", "Universal Travel Adapter", [])]
products=[]
for i in range(100):
 c, name, devices=templates[i%len(templates)]; dev=devices if devices else ([] if c not in ["Laptop Sleeve"] else ["MacBook Air M3"])
 products.append({"id":f"product_{i+1:03}","name":f"{['Aero','Nova','Orbit','Pulse'][i%4]} {name}","category":c,"description":f"Reliable {name.lower()} designed for everyday use.","price":random.randrange(499,8999,100),"stock":0 if i in (17,71) else random.randint(8,150),"compatible_devices":dev,"tags":[c.lower().replace(' ','-'),"quality","popular"],"popularity":random.randint(45,98),"margin_percent":random.randint(15,42)})
products[0].update({"name":"Aero Samsung Galaxy S24 Ultra Protective Case","category":"Phone Case","price":1499,"compatible_devices":["Samsung Galaxy S24 Ultra"]})
products[3].update({"name":"Nova Samsung Galaxy S24 Ultra Tempered Glass","category":"Screen Protector","price":799,"compatible_devices":["Samsung Galaxy S24 Ultra"]})
(OUT/"products.json").write_text(json.dumps(products,indent=2))
customers=[]
for i in range(50): customers.append({"id":f"cust_{i+1:03}","previous_purchases":random.sample([p["id"] for p in products],2),"preferences":random.sample(["Phone Case","Screen Protector","Laptop","Headphones","Travel Accessory"],2),"average_order_value":random.randint(900,6000),"browsing_history":random.sample([p["id"] for p in products],3),"cart_history":[]})
(OUT/"customers.json").write_text(json.dumps(customers,indent=2))
print("Generated 100 products and 50 synthetic customers")
