from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Word(models.Model):

    GENDERS = [
        ('der', 'Der'),
        ('die', 'Die'),
        ('das', 'Das'),
    ]

    word = models.CharField(verbose_name='Word', max_length=100)
    gender = models.CharField(verbose_name='Gender', max_length=3, choices=GENDERS)

    def __str__(self):
        return f'{self.gender} {self.word}'


class User(BaseModel):
    telegram_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)
    preferred_currency = models.ForeignKey('Currency', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class Currency(BaseModel):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.code


class Income(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    category = models.ForeignKey('CategoryIncome', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} {self.currency} (Income)"


class CategoryIncome(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user}. {self.name}"


class Expense(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    category = models.ForeignKey('CategoryExpense', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.amount} {self.currency} (Expense)"


class CategoryExpense(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
