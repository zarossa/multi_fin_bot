from django.contrib.auth.models import User
from django.db import models


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Account(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.ForeignKey('Currency', verbose_name='Base currency', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.user.first_name


class Currency(BaseModel):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.code
#
#
# class Income(BaseModel):
#     user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
#     category = models.ForeignKey('CategoryIncome', on_delete=models.PROTECT)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user} - {self.amount} {self.currency} (Income)"
#
#
# class CategoryIncome(BaseModel):
#     user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return f"{self.user}. {self.name}"
#
#
# class Expense(BaseModel):
#     user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
#     category = models.ForeignKey('CategoryExpense', on_delete=models.PROTECT)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user.name} - {self.amount} {self.currency} (Expense)"
#
#
# class CategoryExpense(BaseModel):
#     user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
