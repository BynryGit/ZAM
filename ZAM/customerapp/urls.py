from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import include, url
from ZAM import settings
from zamapp import security
from zamapp import index
from zamapp import securityprice
from zamapp import trades
from zamapp import position
from zamapp import upload

urlpatterns = patterns('',
    url(r'^$', 'customerapp.myplan.open_myplan', name='open_myplan'),
    url(r'^customer-details', 'customerapp.CustomerDetails.open_customer_details', name='customer_details'),
    url(r'^add-customer-details', 'customerapp.CustomerDetails.add_customer_details', name='add_customer_details'),
    url(r'^update-customer-details', 'customerapp.CustomerDetails.update_customer_details', name='update_customer_details'),
    url(r'^customer-variable-details', 'customerapp.CustomerDetails.customer_variable_details', name='customer_variable_details'),
    url(r'^delete-variable', 'customerapp.CustomerDetails.delete_variable', name='delete_variable'),
    url(r'^open-add-details', 'customerapp.accountDetails.open_add_details', name='open_add_details'),
    url(r'^open-new-worth', 'customerapp.myplan.open_new_worth', name='open_new_worth'),
    url(r'^open-setting-goals', 'customerapp.accountDetails.setting_goals', name='setting_goals'),
    url(r'^open-implementation', 'customerapp.meter_gauge.open_implementation', name='open_implementation'),
    url(r'^open-roadmap', 'customerapp.implementation.open_roadmap', name='open_roadmap'),
    url(r'^implementation-year-calc', 'customerapp.implementation.implementation_year_calc', name='implementation_year_calc'),
    url(r'^implementation-debt-equity-calc', 'customerapp.implementation.implementation_debt_equity_calc', name='implementation_debt_equity_calc'),
    url(r'^open-bank-account', 'customerapp.accountDetails.open_bank_account', name='open_bank_acount'),
    url(r'^open-other-saving-product', 'customerapp.accountDetails.open_other_saving_product', name='open_other_saving_product'),
    url(r'^open-direct-brokrage', 'customerapp.accountDetails.open_direct_brokrage', name='open_direct_brokrage'),
    url(r'^open-mutual-fund', 'customerapp.accountDetails.open_mutual_fund', name='open_mutual_fund'),
    url(r'^open-pension-product', 'customerapp.accountDetails.open_pension_product', name='open-pension-product'),
    url(r'^open-provident-fund', 'customerapp.accountDetails.open_provident_fund', name='open_provident_fund'),   
    url(r'^open-property', 'customerapp.accountDetails.open_property', name='open_property'),      
    url(r'^open-gold', 'customerapp.accountDetails.open_gold', name='open_gold'),          

    url(r'^save-product', 'customerapp.accountDetails.save_product', name='save_product'),
    url(r'^edit-product-data', 'customerapp.accountDetails.edit_product_data', name='edit_product_data'),
    url(r'^delete-product-data', 'customerapp.accountDetails.delete_product_data', name='delete_product_data'),
    url(r'^get-product-list', 'customerapp.accountDetails.get_product_list', name='get_product_list'),
    url(r'^get-product-data', 'customerapp.accountDetails.get_product_data', name='get_product_data'),
    
    url(r'^save-goal', 'customerapp.accountDetails.save_goal', name='save_goal'),
    url(r'^get-goal-list', 'customerapp.accountDetails.get_goal_list', name='get_product_list'),
    url(r'^delete-goal-data', 'customerapp.accountDetails.delete_goal_data', name='delete_goal_data'),
    url(r'^edit-goal-data', 'customerapp.accountDetails.edit_goal_data', name='edit_goal_data'),
    url(r'^edit-bank-data', 'customerapp.accountDetails.edit_bank_data', name='edit_bank_data'),
    url(r'^delete-bank-data', 'customerapp.accountDetails.delete_bank_data', name='delete_bank_data'),



    url(r'^save-bank', 'customerapp.accountDetails.save_bank', name='save_bank'),
    url(r'^customer-report', 'customerapp.accountDetails.customer_report', name='customer_report'),
    url(r'^change-password/','zamapp.registration.open_rename_password', name='rename_password'),

) + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
