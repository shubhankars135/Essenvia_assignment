# ESSENVIA TASK


**To bring up the setup, follow these steps:**   
1. Clone the repository   
`git clone https://github.com/shubhankars135/Essenvia_assignment`   
2. Create a virtual environment and activate it        
`python -m venv .venv`   
For windows: `.venv\Scripts\activate`    
For mac\linux: `.venv/bin/activate`   
3. Install the required libraries and packages   
`pip install -r requirements.txt` 
4. Make Migration    
`python manage.py makemigrations`   
5. Migrate    
`python manage.py migrate`   
6. Runserver    
`python manage.py runserver`


**API SPECIFICATIONS**

This project has following APIs:

1. Fetch order number from backend

   URL : (http://127.0.0.1:8000/get_order_no)
   
   response : {"order_no": "171021_2"}
  
2. Check inventory status

   URL : (http://127.0.0.1:8000/v1/item_inventory/)
   
   `response : [
      {
          "item_model_no": "T2020UHD",
          "items_available": 1,
          "price": 38999.0
      },
      {
          "item_model_no": "T20214K",
          "items_available": 1,
          "price": 45449.0
      }
    ]`
3. Check order confirmation status / Estimated time of delivery

   URL: (http://127.0.0.1:8000/v1/order_info/)
   
   `response : [
        {
            "order": "171021_1",
            "team_assigned": "a",
            "delivery_start_at": "2021-10-17T23:49:52.422164+05:30",
            "estimated_delivery_at": "2021-10-18T00:29:52.422164+05:30"
        },
        {
            "order": "171021_2",
            "team_assigned": "a",
            "delivery_start_at": "2021-10-18T00:39:32.043026+05:30",
            "estimated_delivery_at": "2021-10-18T01:19:32.043026+05:30"
        }
    ]`

