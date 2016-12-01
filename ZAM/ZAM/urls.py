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
from customerapp.urls import urlpatterns
from zamapp import upload
#urlpatterns = (
urlpatterns = patterns('',
    ##----------login and captcha urls--------

    url(r'^$', 'zamapp.index.open_index', name='login'),
    url(r'^open-login-page', 'zamapp.index.login_open', name='login'),
    url(r'^loging-in/', 'zamapp.index.loging_in', name='loging_in'),
    url(r'^signing-out/', 'zamapp.index.signing_out', name='loging_in'),
    url(r'^reload-captcha/', 'zamapp.captcha_mod.reload_captcha', name='captcha_reload'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^do-active-user/', 'zamapp.index.do_active_user', name='do_active_user'),
    url(r'^do-active-user/', 'zamapp.index.do_active_user', name='do_active_user'),
    url(r'^delete-user/', 'zamapp.index.delete_user', name='delete_user'),
    url(r'^open-otp/', 'zamapp.index.open_otp', name='delete_user'),
    url(r'^check-otp/', 'zamapp.index.check_otp', name='check_otp'),
    url(r'^retrive-user/', 'zamapp.index.retrive_user', name='retrive_user'),


    ##-----------------Sign-up----------------------
    url(r'^open-signup-page/', 'zamapp.registration.open_signup_page', name='signup_page'),
    url(r'^signing-up/', 'zamapp.registration.signing_up', name='signing_in'),
    url(r'^open-user-index/', 'zamapp.registration.open_user_index', name='signup_page'),
    url(r'^open-add-user-page/', 'zamapp.registration.open_add_user_page', name='signup_page'),
    url(r'^get-user-list/', 'zamapp.registration.get_user_list', name='get_user_list'),
    url(r'^view-user-details/','zamapp.registration.view_user_details', name='open_add_bulk_security_page'),
    url(r'^update-userdetails-up/','zamapp.registration.update_userdetails_up', name='open_add_bulk_security_page'),
    url(r'^open-rename-password/','zamapp.registration.open_rename_password', name='open_add_bulk_security_page'),
    url(r'^change-password/','zamapp.registration.change_password', name='open_add_bulk_security_page'),

    ##-----------------Customer----------------------------
    url(r'^customer/', include(urlpatterns)),
    url(r'^open-YFinAdvisor-customer/', 'zamapp.zam_admin.open_YFinAdvisor_customer', name='open_YFinAdvisor_customer'),
    url(r'^get-customer-list/', 'zamapp.registration.get_customer_list', name='get_customer_list'),
    url(r'^view-customer-details/','zamapp.registration.view_customer_details', name='view_customer_details'),
    url(r'^save-customer-description/','zamapp.registration.save_customer_description', name='save_customer_description'),
    url(r'^send-welcome-mail/','zamapp.registration.send_welcome_email', name='send_welcome_email'),

    ##----------Security urls--------
    url(r'^open-security-page/', security.open_security_page, name='home'),
    url(r'^open-add-security-page/', security.open_add_security_page, name='home'),
    url(r'^add-currency-security/', security.add_currency_security, name='home'),
    url(r'^add-subassetclass-security/', security.add_subassetclass_security, name='home'),
    url(r'^save-security-details/', security.save_security_details, name='save_security_details'),
    url(r'^get-securitydetails-list/', security.get_securitydata_list, name='security_details'),
    url(r'^view-security-details/', security.view_security_details, name='security_details'),
    url(r'^update-security-details/', security.update_security_details, name='home'),
    url(r'^open-add-bulk-security-page/', security.open_add_bulk_security_page, name='open_add_bulk_security_page'),
    url(r'^add-bulk-security/', security.add_bulk_security, name='add_bulk_security'),
    url(r'^edit-security-details/', security.view_security_details, name='security_details'),
    url(r'^change-security-status/', 'zamapp.security.change_status', name='change-status'),

    ##----------Security price urls--------
    url(r'^open-security-price-page/', securityprice.open_security_price_page, name='home'),
    url(r'^open-add-security-price-page/', securityprice.open_add_security_price_page, name='home'),
    url(r'^open-add-bulk-security-price-page/', securityprice.open_add_bulk_security_price_page, name='home'),
    url(r'^add-securities-list/', security.add_securities_list, name='add-securities-list'),
    url(r'^save-security-price-details/', securityprice.save_security_price_details,
        name='save_security_price_details'),
    url(r'^get-securityprice-list/', securityprice.get_securityprice_list, name='security_details'),
    url(r'^view-security-price-details/', securityprice.view_security_price_details, name='security_details'),
    url(r'^update-security-price-details/', securityprice.update_security_price_details, name='security_details'),
    url(r'^add-bulk-price/', securityprice.add_bulk_price, name='add_bulk_price'),
    url(r'^delete-security-price/', securityprice.delete_security_price, name='add_bulk_price'),
    url(r'^add-bloombergTicker-list/', security.add_bloombergTicker_list, name='add_bloombergTicker_list'),
    url(r'^add-security-intextbox/', security.add_security_intextbox, name='add_bloombergTicker_list'),



    ##----------Dashboard urls--------
    url(r'^open-dashboard/', index.open_dashboard, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', 'zamapp.index.open_dashboard', name='home'),

    ##--------------CRM urls-------------------------------------------
    url(r'^crm-index/', 'zamapp.crm.crm_index', name='crm_index'),
    url(r'^get-client-list/', 'zamapp.crm.get_client_list', name='client_list'),
    url(r'^add-client/', 'zamapp.crm.add_client', name='add_client'),
    url(r'^view-client/', 'zamapp.crm.view_client', name='view_client'),
    url(r'^edit-client/', 'zamapp.crm.edit_client', name='view_client'),
    url(r'^client-communication/', 'zamapp.crm.communication_details', name='client_comm'),
    url(r'^save-client/', 'zamapp.crm.save_client', name='save_client'),
    url(r'^update-basic-info/', 'zamapp.crm.update_basic_info', name='update_basic_info'),
    url(r'^save-client-ip/', 'zamapp.crm.save_client_ip', name='client_ip'),
    url(r'^update-client-ip/', 'zamapp.crm.update_client_ip', name='update_client_ip'),
    url(r'^add-contact-person/', 'zamapp.crm.add_contact_person', name='contact_person'),
    url(r'^add-communication/', 'zamapp.crm.add_communication', name='communication'),
    url(r'^search-communication/', 'zamapp.crm.search_communication', name='search_communication'),
    url(r'^get-communication-msg/', 'zamapp.crm.get_communication_msg', name='get_communication'),
    url(r'^files-upload/', 'zamapp.upload.imageupload', name='image_upload'),
    url(r'^files-remove/', 'zamapp.upload.remove_image', name='remove'),
    url(r'^get-communication-list/', 'zamapp.crm.get_communication_list', name='comm_list'),
    url(r'^change-status/', 'zamapp.crm.change_status', name='change-status'),
    url(r'^get-contact-person/', 'zamapp.crm.get_contact_person', name='contact-person'),

    #-------------Trade URLS---------------------------------------

    url(r'^open-trade/', trades.open_trade, name='open_trade'),
    url(r'^open-add-trade/', trades.open_add_trade, name='open_add_trade'),
    url(r'^open-view-trade/', trades.open_view_trade, name='open_view_trade'),
    url(r'^open-add-bulk-trade/', trades.open_add_bulk_trade, name='open_add_bulk_trade'),
    url(r'^add-trade/', trades.add_trade, name='add_trade'),
    url(r'^edit-trade/', trades.edit_trade, name='edit_trade'),
    url(r'^delete-trade/', trades.delete_trade, name='delete_trade'),
    url(r'^get_price/', trades.get_price, name='get_price'),
    url(r'^view-trades/', trades.view_trades, name='view-trades'),
    url(r'^asset-subclass/', trades.asset_subclass, name='asset_subclass'),
    url(r'^append-security/', trades.append_security, name='append_security'),
    url(r'^add-bulk-trade/', trades.add_bulk_trade, name='add_bulk_trade'),
    url(r'^view-security-list/', trades.view_security_list, name='view_security_list'),
    url(r'^view-security-lists/', trades.view_security_lists, name='view_security_lists'),
    url(r'^check-price/', trades.check_price, name='check_price'),

    ##--------------------Research URLS------------------------------------------

    url(r'^open-research-page/','zamapp.research.open_analyst', name='open_analyst'),
    url(r'^add-focuslist-page/','zamapp.research.add_focus_list', name='add_focus_list'),
    url(r'^add-activelist-page/','zamapp.research.add_active_list', name='add_active_list'),
    url(r'^add-portfoliolist-page/','zamapp.research.add_portfolio_list', name='add_portfolio_list'),
    url(r'^save-focuslist-comapany/','zamapp.research.save_focuslist_company', name='save_focuslist_company'),
    url(r'^get-focus-list/','zamapp.research.get_focus_list', name='save_focuslist_company'),
    url(r'^get-focus-researchlog/','zamapp.research.get_focus_researchlog', name='get_focus_researchlog'),
    url(r'^update-focus-researchlog/','zamapp.research.update_focus_researchlog', name='update_focus_researchlog'),
 #   url(r'^view-focuslist-company/','zamapp.research.view_focuslist_company', name='view_focuslist_company'),
    url(r'^edit-focuslist-company/','zamapp.research.edit_focuslist_company', name='edit_focuslist_company'),
    url(r'^update-focuslist-company/','zamapp.research.update_focuslist_company', name='update_focuslist_company'),
    url(r'^change-company-status/', 'zamapp.research.change_company_status', name='change-status'),
    url(r'^save-portfoliolist-comapany/','zamapp.research.save_portfoliolist_company', name='save_portfoliolist_company'),
    url(r'^get-portfolio-list/','zamapp.research.get_portfolio_list', name='get_portfolio_list'),
    url(r'^change-portfolio-company-status/', 'zamapp.research.change_portfolio_company_status', name='change-portfolio-status'),
    url(r'^edit-portfoliolist-company/','zamapp.research.edit_portfoliolist_company', name='edit_portfoliolist_company'),
    url(r'^update-portfoliolist-company/','zamapp.research.update_portfoliolist_company', name='update_portfoliolist_company'),
    
    url(r'^save-focuslog/','zamapp.research.add_log_focus_list', name='add_log_focus_list'),
    url(r'^save-activelog/','zamapp.research.add_log_active_list', name='add_log_active_list'),
    url(r'^save-portfoliolog/','zamapp.research.add_log_portfolio_list', name='add_log_portfolio_list'),
    url(r'^get-focus-communication-msg/', 'zamapp.research.get_focus_communication_msg', name='get_communication'),
    url(r'^get-active-communication-msg/', 'zamapp.research.get_active_communication_msg', name='get_communication'),
    url(r'^get-portfolio-communication-msg/', 'zamapp.research.get_portfolio_communication_msg', name='get_communication'),
    url(r'^get-port-researchlog/','zamapp.research.get_port_researchlog', name='get_port_researchlog'),
    url(r'^update-port-researchlog/','zamapp.research.update_port_researchlog', name='update_port_researchlog'),

    url(r'^save-activelist-company/','zamapp.research.save_activelist_company', name='save_activelist_company'),
    url(r'^view-activelist-company/','zamapp.research.view_activelist_company', name='view_activelist_company'),
    url(r'^edit-activelist-company/','zamapp.research.edit_activelist_company', name='edit_activelist_company'),
    url(r'^update-activelist-company/','zamapp.research.update_activelist_company', name='update_activelist_company'),
    url(r'^delete-activelist-company/','zamapp.research.delete_activelist_company', name='delete_activelist_company'),
    url(r'^get-active-researchlog/','zamapp.research.get_active_researchlog', name='get_active_researchlog'),
    url(r'^update-active-researchlog/','zamapp.research.update_active_researchlog', name='update_active_researchlog'),

    url(r'^active-files-upload/', 'zamapp.upload.active_file_upload', name='active_file_upload'),
    url(r'^focus-files-upload/', 'zamapp.upload.focus_file_upload', name='focus_file_upload'),
    url(r'^portfolio-files-upload/', 'zamapp.upload.portfolio_file_upload', name='portfolio_file_upload'),
    url(r'^focus-files-remove/', 'zamapp.upload.focus_file_remove', name='focus_file_remove'),
    url(r'^active-files-remove/', 'zamapp.upload.active_file_remove', name='active_file_remove'),
    url(r'^portfolio-files-remove/', 'zamapp.upload.portfolio_file_remove', name='portfolio_file_remove'),
    url(r'^focuslist-file-upload/', 'zamapp.upload.focuslist_file_upload', name='focuslist_file_upload'),
    url(r'^activelist-file-upload/', 'zamapp.upload.activelist_file_upload', name='activelist_file_upload'),
    url(r'^portfoliolist-file-upload/', 'zamapp.upload.portfoliolist_file_upload', name='portfoliolist_file_upload'),
    url(r'^update-focus-file-upload/', 'zamapp.upload.update_focus_file_upload', name='update_focus_file_upload'),
    url(r'^update-activelist-file-upload/', 'zamapp.upload.update_activelist_file_upload', name='update_activelist_file_upload'),
    url(r'^update-portfoliolist-file-upload/', 'zamapp.upload.update_portfoliolist_file_upload', name='update_portfoliolist_file_upload'),
    url(r'^remove-focuslistmisc-image/', 'zamapp.upload.remove_focuslistmisc_image', name='remove_focuslistmisc_image'),
    url(r'^remove-activelistmisc-image/', 'zamapp.upload.remove_activelistmisc_image', name='remove_activelistmisc_image'),
    url(r'^remove-portfoliolistmisc-image/', 'zamapp.upload.remove_portfoliolistmisc_image', name='remove_portfoliolistmisc_image'),


    url(r'^get-price-msi/','zamapp.research.get_price_msi', name='get_price_msi'),

    #-------------Position URLS---------------------------------------

    url(r'^open-position/', position.open_postion, name='open_postion'),
    url(r'^get-security-position/', position.get_security_position, name='open_postion'),
    url(r'^open-add-bulk-position/', position.open_add_bulk_position, name='open_add_bulk_position'),
    url(r'^generate-position/', position.generate_position, name='open_add_bulk_position'),
    url(r'^get-trades/', position.get_trades, name='get_trades'),
    url(r'^get-position-list-by-country/', position.get_position_list_by_country, name='get_position_list_by_country'),
    url(r'^get-position-list-by-assetclass/', position.get_position_list_by_assetclass, name='get_position_list_by_assetclass'),

##-------------------Marketing Manager--------------------##
    url(r'^open-discussion-forum/', 'zamapp.marketing_manager.open_marketing_manager', name='open_marketing_manager'),
    url(r'^save-question/', 'zamapp.marketing_manager.save_question', name='save_question'),
    url(r'^save-response/', 'zamapp.marketing_manager.save_response', name='save_response'),
    url(r'^save-responseto/', 'zamapp.marketing_manager.save_responseto', name='save_responseto'),
    url(r'^view-questions-details/', 'zamapp.marketing_manager.view_questions_typewise', name='view_questions_typewise'),
  #  url(r'^save-response1/', 'zamapp.marketing_manager.save_response1', name='save_response'),
  #  url(r'^save-responseto1/', 'zamapp.marketing_manager.save_responseto1', name='save_responseto'),
    url(r'^search-question/', 'zamapp.marketing_manager.search_question', name='save_response'),
    url(r'^delete-question/', 'zamapp.marketing_manager.delete_question', name='delete_question'),
    url(r'^delete-responses/', 'zamapp.marketing_manager.delete_responses', name='delete_response'),
    url(r'^delete-response/', 'zamapp.marketing_manager.delete_response', name='delete_response'),
    url(r'^delete-responseto/', 'zamapp.marketing_manager.delete_responseto', name='delete_responseto'),



##-----------------------Admin URLs---------------------------------#
    url(r'^open-YFinAdvisor-index/', 'zamapp.zam_admin.open_YFinAdvisor_index', name='open_YFinAdvisor_index'),
    url(r'^save-variables/', 'zamapp.zam_admin.save_variables', name='save_variables'),
    url(r'^get-variables-list/', 'zamapp.zam_admin.get_variable_list', name='get_variable_list'),
    url(r'^delete-variable/', 'zamapp.zam_admin.delete_variable', name='delete_variable'),
    url(r'^get-variable-data/', 'zamapp.zam_admin.get_variable_data', name='get_variable_data'),
    url(r'^edit-variables/', 'zamapp.zam_admin.edit_variable', name='edit_variable'),
    url(r'^save-full-asset-tool/', 'zamapp.zam_admin.save_full_asset_tool', name='save_full_asset_tool'),
    url(r'^get-full-asset-tool-list/', 'zamapp.zam_admin.get_full_asset_tool_list', name='get_full_asset_tool_list'),
    url(r'^view-full-asset-tool/', 'zamapp.zam_admin.view_full_asset_tool', name='view_full_asset_tool'),
    url(r'^view-full-bank-asset-tool/', 'zamapp.zam_admin.view_full_bank_asset_tool', name='view_full_bank_asset_tool'),
    url(r'^update-full-asset-tool/', 'zamapp.zam_admin.update_full_asset_tool', name='update_full_asset_tool'),
    url(r'^delete-product/', 'zamapp.zam_admin.delete_product', name='delete_variable'),
    url(r'^save-goal-parameter/', 'zamapp.zam_admin.save_goal_parameter', name='save_goal_parameter'),  
    url(r'^get-goal-setting-parameter/', 'zamapp.zam_admin.get_goal_setting_parameter', name='get_goal_setting_parameter'),
    url(r'^view-goal-parameter/', 'zamapp.zam_admin.view_goal_parameter', name='view_goal_parameter'),
    url(r'^edit-goal-parameter/', 'zamapp.zam_admin.edit_goal_parameter', name='edit_goal_parameter'),


) + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)