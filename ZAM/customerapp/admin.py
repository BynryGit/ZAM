from django.contrib import admin
from customerapp.models import *

class Customer_ProductAdmin(admin.ModelAdmin):
    list_display=('customer_product_id','user_id','product_id','amount')
    search_fields=['user_id__user_first_name']
    list_filter = ('user_id',)

class GoalAdmin(admin.ModelAdmin):
    list_display=('goal_id','user_id','goal_name','goal_target_year','amount','amount_allocated','goal_status')
    search_fields=['user_id__user_first_name','goal_cat_id__goal_cat','goal_name','amount','goal_status']
    list_filter = ('user_id','goal_status',)

class Customer_VariablesAdmin(admin.ModelAdmin):
    list_display=('CustomerVariable_id','customer_id','variable','amount','row_status')
    search_fields=['customer_id__first_name','variable','row_status']
    list_filter = ('customer_id','row_status',)

class CustomerBankAccountDetailsAdmin(admin.ModelAdmin):
    list_display=('CustomerBankAccount_id','user_id','bank','currency_id','amount','row_status')
    search_fields=['user_id__user_first_name','bank','amount']
    list_filter = ('user_id','bank')


admin.site.register(Product)
admin.site.register(Customer_Product,Customer_ProductAdmin)
admin.site.register(Goal_Category)
admin.site.register(Goal_Target_Year)
admin.site.register(Goal,GoalAdmin)
admin.site.register(BankDetails)
#admin.site.register(CustomerBankAccountDetails,CustomerBankAccountDetailsAdmin)
admin.site.register(CustomerPersonalInfo)
admin.site.register(CustomerChildrenInfo)
admin.site.register(CustomerVariable,Customer_VariablesAdmin)

