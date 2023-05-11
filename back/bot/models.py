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
        ordering = ['id']


class Currency(BaseModel):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=50)
    rate = models.DecimalField(default=1, max_digits=20, decimal_places=10)

    def __str__(self):
        return self.code


class Account(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, verbose_name='Base currency', on_delete=models.PROTECT)
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Amount of money')

    def __str__(self):
        return self.user.first_name


class AccountCurrency(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.user.first_name}. {self.currency}"


class CategoryIncome(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name}. {self.name}"


class Income(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.RESTRICT)
    category = models.ForeignKey(CategoryIncome, on_delete=models.RESTRICT)
    converted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.amount} {self.currency} (Income)"


class CategoryExpense(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name}. {self.name}"


class Expense(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.RESTRICT)
    category = models.ForeignKey(CategoryExpense, on_delete=models.RESTRICT)
    converted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.amount} {self.currency} (Expense)"
