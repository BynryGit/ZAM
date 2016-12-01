from django.db import models
from zamapp.models import UserProfile, Currency,Variable, AccountType

ROW_STATUS = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
)

GOAL_STATUS = (
    ('Met', 'Met'),
    ('Not Met', 'Not Met'),
    ('May Be', 'May Be'),
)

MARITAL_STATUS = (
    ('MARRIED', 'MARRIED'),
    ('UNMARRIED', 'UNMARRIED'),
)

OCCUPATION_STATUS = (
    ('SELF EMPLOYED','SELF EMPLOYED'),
    ('PRIVATE SALARIED','PRIVATE SALARIED'),
    ('GOVT SALARIED','GOVT SALARIED')
)

BENEFIT_STATUS  = (
    ('YES','YES'),
    ('NO','NO')
)

class CustomerPersonalInfo(models.Model):
    customer_personal_info_id =models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, null=True)
    user_title = models.CharField(max_length=15, null=True)
    first_name=models.CharField(null=True,max_length=255)
    report_description=models.CharField(null=True,max_length=5000)
    last_name=models.CharField(null=True,max_length=255)
    spouse_first_name=models.CharField(null=True,max_length=255)
    spouse_last_name=models.CharField(null=True,max_length=255)
    age=models.IntegerField(null=True)
    spouse_age=models.IntegerField(null=True)
    gender=models.CharField(null=True,max_length=255)
    spouse_gender=models.CharField(null=True,max_length=255)
    marital_status=models.CharField(max_length=255,default='NO', choices = MARITAL_STATUS )
    no_of_child=models.IntegerField(default=0)
    dob = models.DateTimeField(null=True)
    registration_date = models.DateTimeField(null=True)
    spouse_dob = models.DateTimeField(null=True)
    occupation = models.CharField(max_length=150, null=True, default=None, choices=OCCUPATION_STATUS)
    spouse_occupation = models.CharField(max_length=150, null=True, default=None, choices=OCCUPATION_STATUS)
    monthly_salary = models.FloatField(max_length=15, null=True)
    spouse_monthly_salary = models.FloatField(max_length=15, null=True)
    govt_benefit = models.CharField(max_length=150, null=True, default=None, choices=BENEFIT_STATUS)
    spouse_govt_benefit = models.CharField(max_length=150, null=True, default=None, choices=BENEFIT_STATUS)
    home_loan = models.FloatField(max_length=15, null=True)
    car_loan = models.FloatField(max_length=15, null=True)
    cibil_score=models.FloatField(max_length=15, null=True)
    total_salary=models.FloatField(max_length=15, null=True)
    start_saving=models.FloatField(max_length=15, null=True)
    mortgage=models.FloatField(max_length=15, null=True)
    credit_card_deb=models.FloatField(max_length=15, null=True)
    other_loans=models.FloatField(max_length=15, null=True)
    profile_updated = models.CharField(max_length=150, null=True, default=None, choices=BENEFIT_STATUS)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    created_by = models.CharField(max_length=150, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=150, null=True)
    updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.first_name +' '+ self.last_name)


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=200, null=True)
    created_by = models.CharField(max_length=150, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=150, null=True)
    updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.product)


class Customer_Product(models.Model):
    customer_product_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserProfile, related_name='userp_id', null=True)
    customer_id = models.ForeignKey(CustomerPersonalInfo, related_name='cust_id', null=True)
    product_id = models.ForeignKey(Product, related_name='prod_id', null=True)
    product_name = models.CharField(max_length=200, null=True, blank=True)
    amount = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.CharField(max_length=150, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=150, null=True)
    updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.customer_product_id)


class Goal_Category(models.Model):
    goal_cat_id = models.AutoField(primary_key=True)
    goal_cat = models.CharField(max_length=200, null=True)
    goal_priorities = models.CharField(max_length=150, null=True)
    goal_percentage = models.FloatField(max_length=10, null=True)
    created_by = models.CharField(max_length=150, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=150, null=True)
    updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.goal_cat)


class Goal_Target_Year(models.Model):
    goal_target_year_id = models.AutoField(primary_key=True)
    goal_target_year = models.CharField(max_length=200, null=True)
    created_by = models.CharField(max_length=150, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=150, null=True)
    updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.goal_target_year)


class Goal(models.Model):
    goal_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserProfile, related_name='userg_id', null=True)
    goal_cat_id = models.ForeignKey(Goal_Category, related_name='gol_cat_id', null=True)
    goal_target_year = models.CharField(max_length=200, null=True, blank=True)
    goal_target_date = models.DateTimeField(null=True)
    goal_name = models.CharField(max_length=200, null=True, blank=True)
    amount = models.CharField(max_length=200, null=True, blank=True)
    amount_allocated = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.CharField(max_length=150, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    goal_status = models.CharField(max_length=150, null=True, default=None, choices=GOAL_STATUS)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=150, null=True)
    updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.goal_id)


class BankDetails(models.Model):
    bank_id = models.AutoField(primary_key=True)
    bank_name = models.CharField(max_length=200, null=True)
    bank_icon = models.CharField(max_length=150, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    created_by = models.CharField(max_length=150, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=150, null=True)
    updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.bank_name)


class CustomerBankAccountDetails(models.Model):
    CustomerBankAccount_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, related_name='account_user', null=True)
    bank = models.CharField(max_length=200, null=True, default=None, choices=ROW_STATUS)
    account_id = models.ForeignKey(AccountType, related_name='account_type', null=True)
    currency = models.ForeignKey(Currency, related_name='account_currency', null=True)
    amount = models.FloatField(max_length=200, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    created_by = models.CharField(max_length=150, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=150, null=True)
    updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.user)

class CustomerChildrenInfo(models.Model):
    child_id =models.AutoField(primary_key=True)
    customer_id =models.ForeignKey(CustomerPersonalInfo,related_name='customer_id', null=True)
    child_name=models.CharField(null=True,max_length=255)
    child_gender=models.CharField(null=True,max_length=255)
    child_dob = models.DateTimeField(null=True)
    age=models.IntegerField(null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    created_by = models.CharField(max_length=150, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=150, null=True)
    updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.child_name)


class CustomerVariable(models.Model):
    CustomerVariable_id = models.AutoField(primary_key=True)
    variable = models.ForeignKey(Variable, related_name='customer_variable_id', null=True)
    customer_id = models.ForeignKey(CustomerPersonalInfo, related_name='variable_customer_id', null=True)
    amount = models.FloatField(max_length=15, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    created_by = models.CharField(max_length=150, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=150, null=True)
    updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.variable)
