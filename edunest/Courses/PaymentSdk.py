from django.conf import settings
import paypalrestsdk

paypalrestsdk.configure({
    "mode": 'sandbox',
    "client_id": 'AbCASLvwWw6V1PZsqomXD4svWf3mQNYlnn8R_CLlfOy8XjqLef6q4btUj99KkXRnv7bh3bHiVH4Shblj',
    "client_secret": 'EFDvGBADnswB9Fl0gd6LuSAA9sOLKcBzo-RRbCCvTS2lQKqIGm--aFpaltdcsyJzFBiMN6vLYvHmgmje'
})
