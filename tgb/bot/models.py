from django.db import models


class User(models.Model):
    telegram_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)
    preferred_currency = models.ForeignKey('Currency', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.code


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    category = models.ForeignKey('CategoryIncome', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.amount} {self.currency.code} (Income)"


class CategoryIncome(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    category = models.ForeignKey('CategoryExpense', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.amount} {self.currency.code} (Expense)"


class CategoryExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
