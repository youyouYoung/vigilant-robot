from django.db import models
from django.conf import settings


class Order(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class CustomerView(models.Model):
    """
    用户评价表
    """
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name="reviews")  # 与Product关联
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 与CustomUser模型关联
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 评分（1-5）
    comment = models.TextField()  # 评论内容
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)  # 最后更新时间
    is_approved = models.BooleanField(default=False)  # 是否已通过审核

    def __str__(self):
        return f'Review by {self.user.username} on {self.product.name}'
