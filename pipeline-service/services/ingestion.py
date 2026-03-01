import requests
from models.customer import Customer
from decimal import Decimal
from datetime import datetime

def ingest_customers(db):
    # Logic here
    records_processed = 0
    page = 1
    
    while True:
        try:
            response = requests.get(
                f"http://mock-server:5000/api/customers",
                params={"page": page, "limit": 10}
            )
            response.raise_for_status()
            
            data = response.json()
            customers = data.get('data', [])
            
            if not customers:
                break
                
            page += 1
            
            for customer in customers:
                try:
                        existing_customer = db.query(Customer).filter_by(customer_id=str(customer['customer_id'])).first()
                
                        dob = datetime.strptime(customer['date_of_birth'], "%Y-%m-%d").date()
                        created_at = datetime.strptime(customer['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                        account_balance = Decimal(str(customer['account_balance']))
                
                        if existing_customer:
                            existing_customer.first_name = customer['first_name']
                            existing_customer.last_name = customer['last_name']
                            existing_customer.email = customer['email']
                            existing_customer.phone = customer['phone']
                            existing_customer.address = customer['address']
                            existing_customer.date_of_birth = dob
                            existing_customer.account_balance = account_balance
                            existing_customer.created_at = created_at
                        else:
                            new_customer = Customer(
                                customer_id=str(customer['customer_id']),
                                first_name=customer['first_name'],
                                last_name=customer['last_name'],
                                email=customer['email'],
                                phone=customer['phone'],
                                address=customer['address'],
                                date_of_birth=dob,
                                account_balance=account_balance,
                                created_at=created_at
                            )
                            db.add(new_customer)
                
                        records_processed += 1
                
                except Exception as e:
                    print(f"Failed to process customer {customer['customer_id']}: {e}")
                    db.rollback()
                    
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error fetching data from API: {e}")
            break
    
    return records_processed
