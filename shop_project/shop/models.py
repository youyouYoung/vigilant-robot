from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _

def get_image_upload_to(instance, filename):
    if isinstance(instance, ProductImage):
        type_name = Product.__name__
        instance_name = instance.product.id
    elif isinstance(instance, Category):
        type_name = instance.__class__.__name__
        instance_name = instance.name
    else:
        type_name = instance.__class__.__name__
        instance_name = None
    return f'{type_name}/images/{instance_name}/{filename}'.lower()

def get_icon_upload_to(instance, filename):
    if isinstance(instance, ProductImage):
        type_name = Product.__name__
        instance_name = instance.product.id
    elif isinstance(instance, Category):
        type_name = instance.__class__.__name__
        instance_name = instance.name
    else:
        type_name = instance.__class__.__name__
        instance_name = None
    return f'{type_name}/icons/{instance_name}/{filename}'.lower()

class Category(models.Model):
    """
    产品分类表
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    icon = models.ImageField(upload_to=get_icon_upload_to, null=True, blank=True)
    order = models.PositiveIntegerField(default=0) # 用于指定分类在列表中的显示顺序。这个字段可以是一个整数，越小的数字越优先显示
    seo_title = models.CharField(max_length=255, null=True, blank=True)
    seo_description = models.CharField(max_length=255, null=True, blank=True)
    seo_keywords = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=get_image_upload_to, null=True, blank=True)
    is_active = models.BooleanField(default=True) # 标记该分类是否处于启用状态。如果分类不再使用，可以将其设置为非激活状态，避免在前端展示
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    商品
    """
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100, default='xyz')
    current_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=150, null=True, blank=True)
    color = models.CharField(max_length=150, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True) # todo could have a couple weight based on size
    material = models.CharField(max_length=150, null=True, blank=True)
    seo_title = models.CharField(max_length=255, null=True, blank=True)
    seo_description = models.CharField(max_length=255, null=True, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True) # 适用于搜索引擎优化的关键词，可以提高搜索排名。
    is_featured = models.BooleanField(default=False) # 标记是否为推荐产品
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True) # 产品的平均评分，可以通过用户评分系统来计算 # todo: update it when we have a new approved customer view
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False) # 标记产品是否还在出售
    is_discontinued = models.BooleanField(default=False) # 标记产品是否已下架，不再出售
    on_sale = models.BooleanField(default=False) # 标记该产品是否正在促销中
    sale_start_date = models.DateTimeField(null=True, blank=True) # 促销活动开始的时间
    sale_end_date = models.DateTimeField(null=True, blank=True) #  促销活动结束的时间
    warranty_period = models.CharField(max_length=50, null=True, blank=True) # 产品的保修期（例如一年）
    returns_allowed = models.BooleanField(default=True) # 标记产品是否支持退换货
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductPriceHistory(models.Model):
    """
    价格历史表
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="price_histories")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True) # todo: update it until we have a new price

class ProductCostHistory(models.Model):
    """
    商品成本历史表
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)  # 每单位产品的成本
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)  # 运输成本
    quantity = models.PositiveIntegerField()  # 该成本下购买的数量
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)  # 计算总成本
    supplier = models.CharField(max_length=150, null=True, blank=True)  # 供应商
    batch_number = models.CharField(max_length=100, null=True, blank=True)  # 采购批次号, 可以通过批次号来追踪每个批次的产品。特别是当有产品质量问题时，可以帮助你追溯
    purchase_order_number = models.CharField(max_length=100, null=True, blank=True)  # 采购订单编号, 用来跟踪订单
    purchase_date = models.DateTimeField()  # 采购日期, 以便跟踪采购历史并对成本进行有效的时间管理
    start_date = models.DateTimeField(auto_now_add=True)  # 成本开始日期 todo: 没想好这个字段该在什么时候变化
    end_date = models.DateTimeField(auto_now=True)  # 成本结束日期（可为空）todo: 没想好这个字段该在什么时候变化

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    filename = models.CharField(max_length=150)
    image = models.ImageField(upload_to=get_image_upload_to)
    is_primary = models.BooleanField(default=False)  # 是否为主图
    # todo add fields alt_text, is_activate

    def __str__(self):
        return f"Image for {self.product.name}"

class CustomUser(AbstractUser):
    """
    自定义用户模型，继承自 AbstractUser
    """
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_temporary = models.BooleanField(default=False) # 快速购买用户的标志

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Address(models.Model):
    """
    用户地址，目前要求billing地址只能创建一个，shipping地址可以创建多个
    """
    ADDRESS_TYPE_CHOICES = (
        ('billing', 'Billing'),
        ('shipping', 'Shipping'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)  # e.g., Ontario, Manitoba
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='Canada')

    def __str__(self):
        return f'{self.address_type} - {self.address_line_1}, {self.city}, {self.country}'

class CustomerView(models.Model):
    """
    用户评价表
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")  # 与Product关联
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 与CustomUser模型关联
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 评分（1-5）
    comment = models.TextField()  # 评论内容
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)  # 最后更新时间
    is_approved = models.BooleanField(default=False)  # 是否已通过审核

    def __str__(self):
        return f'Review by {self.user.username} on {self.product.name}'

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
