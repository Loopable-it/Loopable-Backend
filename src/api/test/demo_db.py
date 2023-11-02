from api.models import ProductCategory, Product
from api.test.firebase_login import get_profile


class DemoDB:
    """
    This class is used to create a demo database for testing purposes.
    Make sure to create USER1 and USER2 before running this class.
    """
    def __init__(self):
        self.profile1 = get_profile('USER1')
        self.profile2 = get_profile('USER2')
        ProductCategory.objects.create(id=1, name='Category 1', description='Category 1 description')
        ProductCategory.objects.create(id=2, name='Category 2', description='Category 2 description')
        ProductCategory.objects.create(id=3, name='Category 3', description='Category 3 description')
        self.p1 = Product.objects.create(name='Product 1 ABC', description='Product 1 desc',
                                         owner=self.profile1, price=10.0, category_id=1, latitude=10.0, longitude=10.0)
        self.p2 = Product.objects.create(name='Product 2 BCD', description='Product 2 desc', stock_quantity=3,
                                         owner=self.profile1, price=20.0, category_id=2, latitude=20.0, longitude=20.0)
        self.p3 = Product.objects.create(name='Product 3 XYZ', description='Product 3 desc',
                                         owner=self.profile2, price=30.0, category_id=2, latitude=30.0, longitude=30.0)
        self.p4 = Product.objects.create(name='Product 4 not active', description='Product 3 desc', active=False,
                                         owner=self.profile2, price=30.0, category_id=2, latitude=30.0, longitude=30.0)
