from django.contrib import admin
from zamapp.models import *


class ClientDetailsTblAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'client_firm', 'firmtype_id', 'client_contact_email', 'client_office_address_line_1',
                    'client_reference_person', 'client_record_status')
    search_fields = ['firmtype_id__firm_name']
    list_filter = ('client_firm', 'client_contact_email', 'client_reference_person', 'client_record_status',)


class ClientIPDetailsTblAdmin(admin.ModelAdmin):
    list_display = ('client_ip_id', 'client_id', 'client_ecv', 'asset_class_one_name', 'asset_class_one_percentage',
                    'asset_class_two_name', 'asset_class_two_percentage',
                    'asset_class_three_name', 'asset_class_three_percentage', 'client_risk_category',
                    'client_ip_record_status')
    search_fields = ['client_ecv']
    list_filter = (
    'client_ecv', 'asset_class_one_name', 'asset_class_two_name', 'asset_class_three_name', 'client_risk_category',
    'client_ip_record_status')


class ClientCommunicationDetailsTblAdmin(admin.ModelAdmin):
    list_display = ('communication_Id', 'client_id', 'contact_person_id', 'communication_date', 'communicationtype_id')
    search_fields = ['communication_date', 'contact_person_id__contact_person_first_name']
    list_filter = ('client_id',)


class ClientCommunicationAttachmentsDetailsTblAdmin(admin.ModelAdmin):
    list_display = ('attachment_id', 'communication_Id')
    search_fields = ['attachment_id', 'communication_Id__communication_date']


class TradeDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'trade_id', 'security_id', 'trade_date', 'buy_sell_indicator', 'trade_security_quantity', 'trade_amount',
        'record_status')
    search_fields = ['security_id__security_name', 'buy_sell_indicator', 'record_status']
    list_filter = ('security_id', 'buy_sell_indicator')


class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_id', 'country_name', 'row_status')
    search_fields = ['country_name', 'row_status']


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('currency_id', 'currency', 'country_id', 'row_status')
    search_fields = ['currency', 'country_id__country_name', 'row_status']


class SecurityStateAdmin(admin.ModelAdmin):
    list_display = ('state_id', 'state', 'row_status')
    search_fields = ['state', 'row_status']


class BenchmarkIndexAdmin(admin.ModelAdmin):
    list_display = ('benchmarkindex_id', 'benchmarkindex', 'row_status')
    search_fields = ['benchmarkindex', 'row_status']


class SecurityTypeAdmin(admin.ModelAdmin):
    list_display = ('securitytype_id', 'securitytype', 'row_status')
    search_fields = ['securitytype', 'row_status']


class FirmtypeAdmin(admin.ModelAdmin):
    list_display = ('firmtype_id', 'firm_name', 'row_status')
    search_fields = ['firm_name', 'row_status']


class ClientpriorityAdmin(admin.ModelAdmin):
    list_display = ('priority_id', 'priority_name', 'row_status')
    search_fields = ['priority_name', 'row_status']


class ContactPersonDetailsAdmin(admin.ModelAdmin):
    list_display = ('contact_person_id', 'client_id', 'contact_person_first_name', 'contact_person_last_name',
                    'contact_person_contact_no'
                    , 'contact_person_email_id')
    search_fields = ['client_id__client_id', 'contact_person_first_name']
    list_filter = ('client_id',)


class ZAMPersonAdmin(admin.ModelAdmin):
    list_display = ('zam_person_id', 'zam_person_name', 'row_status')
    search_fields = ['zam_person_name', 'row_status']


class CommunicationTypesAdmin(admin.ModelAdmin):
    list_display = ('communicationtype_id', 'communicationtype_name')
    search_fields = ['communicationtype_name']


class SecurityCountryAdmin(admin.ModelAdmin):
    list_display = ('country_id', 'country_name', 'row_status')
    search_fields = ['country_name', 'row_status']


class SecuritySectorAdmin(admin.ModelAdmin):
    list_display = ('sector_id', 'sector_name', 'row_status')
    search_fields = ['sector_name', 'row_status']


class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('question_type_id', 'question_type')
    search_fields = ['question_type']


class FocusListAdmin(admin.ModelAdmin):
    list_display = (
        'focuslist_company_id', 'company_name', 'country_id', 'mkt_cap', 'daily_turnover', 'cmp',
        'move_since_inseption',
        'up_down_side', 'company_record_status')
    search_fields = ['company_name', 'country_id__country_name', 'company_record_status']
    list_filter = ('company_name', 'country_id')


class ActiveListAdmin(admin.ModelAdmin):
    list_display = (
        'activelist_company_id', 'company_name', 'country_id', 'congruence', 'industry_analysis', 'cmp',
        'move_since_inseption',
        'up_down_side', 'row_status')
    search_fields = ['company_name', 'country_id__country_name', 'row_status']
    list_filter = ('company_name', 'country_id')


class PortfolioListAdmin(admin.ModelAdmin):
    list_display = (
        'portfolio_company_id', 'company_name', 'country_id', 'cmp', 'move_since_inseption',
        'up_down_side', 'company_record_status')
    search_fields = ['company_name', 'country_id__country_name', 'company_record_status']
    list_filter = ('company_name', 'country_id')


class ResearchAttachmentTypesAdmin(admin.ModelAdmin):
    list_display = ('communicationtype_id', 'communicationtype_name', 'record_status')
    search_fields = ['communicationtype_name', 'record_status']


class FocusListResearchLogAdmin(admin.ModelAdmin):
    list_display = (
        'focus_researchlog_Id', 'focuslist_company_id', 'zam_person_id', 'company_personel', 'designation',
        'bank_name', 'analyst_name', 'communicationtype_id', 'record_status')
    search_fields = ['focuslist_company_id__company_name', 'zam_person_id', 'record_status']
    list_filter = ('focuslist_company_id', 'bank_name', 'analyst_name', 'communicationtype_id')


class ActiveListResearchLogAdmin(admin.ModelAdmin):
    list_display = (
        'active_researchlog_Id', 'activelist_company_id', 'zam_person_id', 'company_personel', 'designation',
        'bank_name', 'analyst_name', 'communicationtype_id', 'record_status')
    search_fields = ['activelist_company_id__company_name', 'zam_person_id', 'record_status']
    list_filter = ('activelist_company_id', 'bank_name', 'analyst_name', 'communicationtype_id')


class PortfolioListResearchLogAdmin(admin.ModelAdmin):
    list_display = (
        'portfolio_researchlog_Id', 'portfolio_company_id', 'zam_person_id', 'company_personel', 'designation',
        'bank_name', 'analyst_name', 'communicationtype_id', 'record_status')
    search_fields = ['portfolio_company_id__company_name', 'zam_person_id', 'record_status']
    list_filter = ('portfolio_company_id', 'bank_name', 'analyst_name', 'communicationtype_id')


class ActiveListAttechmentAdmin(admin.ModelAdmin):
    list_display = ('attechment_id', 'active_researchlog_id', 'attachment_path')
    list_filter = ('active_researchlog_id',)


class FocusListAttechmentAdmin(admin.ModelAdmin):
    list_display = ('attechment_id', 'focus_researchlog_Id', 'attachment_path')
    list_filter = ('focus_researchlog_Id',)


class PortfolioListAttechmentAdmin(admin.ModelAdmin):
    list_display = ('attechment_id', 'portfolio_researchlog_Id', 'attachment_path')
    list_filter = ('portfolio_researchlog_Id',)


class FocusListMiscleneousAttachmentAdmin(admin.ModelAdmin):
    list_display = ('misleneous_attechment_id', 'focuslist_company_id', 'attachment_path')
    list_filter = ('focuslist_company_id',)
    search_fields = ['focuslist_company_id__company_name']


class ActiveListMiscleneousAttachmentAdmin(admin.ModelAdmin):
    list_display = ('misleneous_attechment_id', 'activelist_company_id', 'attachment_path')
    list_filter = ('activelist_company_id',)
    search_fields = ['activelist_company_id__company_name']


class PortfolioMiscleneousAttachmentAdmin(admin.ModelAdmin):
    list_display = ('misleneous_attechment_id', 'portfolio_company_id', 'attachment_path')
    list_filter = ('portfolio_company_id',)
    search_fields = ['portfolio_company_id__company_name']


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
    'question_id', 'question_type', 'question', 'question_ask_date', 'user_id', 'read_status', 'record_status')
    list_filter = ('question_type', 'read_status')
    search_fields = ['question_type__question_type', 'read_status', 'record_status']


class ResponseAdmin(admin.ModelAdmin):
    list_display = (
    'response_id', 'question_id', 'response', 'response_date', 'user_id', 'read_status', 'record_status')
    list_filter = ('question_id', 'read_status')
    search_fields = ['question_id__question', 'response', 'read_status', 'record_status']


class ResponsetoAdmin(admin.ModelAdmin):
    list_display = (
    'responseto_id', 'response_id', 'responseto', 'responseto_date', 'user_id', 'read_status', 'record_status')
    list_filter = ('read_status',)
    search_fields = ['response_id__response', 'read_status', 'record_status']


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_first_name', 'user_last_name', 'user_email_id', 'role_id', 'row_status')
    search_fields = ['role_id__role', 'user_first_name', 'user_last_name', 'user_email_id', 'row_status']
    list_filter = ('role_id__role',)


class AssetClassAdmin(admin.ModelAdmin):
    list_display = ('asset_class_id', 'asset_class_name', 'row_status')
    search_fields = ('asset_class_id', 'asset_class_name', 'row_status')


class AssetSubClassAdmin(admin.ModelAdmin):
    list_display = ('asset_sub_class_id', 'asset_class_id', 'asset_sub_class_name', 'row_status')
    search_fields = ('asset_sub_class_id', 'asset_class_id__asset_class_name', 'asset_sub_class_name', 'row_status')
    list_display_links = ('asset_sub_class_id', 'asset_sub_class_name')


class SecurityAdmin(admin.ModelAdmin):
    list_display = (
    'security_id', 'asset_sub_class_id', 'sector_id', 'security_name', 'security_bloomer_ticker', 'record_status')
    search_fields = (
    'security_id', 'asset_sub_class_id__asset_sub_class_name', 'sector_id__sector_name', 'security_name',
    'security_bloomer_ticker', 'record_status')
    list_filter = ('sector_id', 'asset_sub_class_id')


class SecurityPriceAdmin(admin.ModelAdmin):
    list_display = (
    'security_price_id', 'security_id', 'security_price_date', 'security_last_price', 'security_in_price',
    'record_status')
    search_fields = ('security_price_id', 'security_id__security_name', 'security_price_date', 'security_last_price',
                     'security_in_price', 'record_status')
    # date_hierarchy = 'security_price_date'
    list_filter = ('security_price_date',)


class PositionDetailsAdmin(admin.ModelAdmin):
    list_display = (
    'position_id', 'security_id', 'last_price', 'in_price', 'position', 'position_date', 'position_status')
    search_fields = ('position_id', 'security_id__security_name', 'last_price', 'in_price', 'position', 'position_date',
                     'position_status')
    # date_hierarchy = 'security_price_date'
    list_filter = ('position_date',)


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role', 'role_status')
    search_fields = ('role_id', 'role', 'role_status')
    list_filter = ('role_created_date',)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(ClientDetailsTbl, ClientDetailsTblAdmin)
admin.site.register(ClientIPDetailsTbl, ClientIPDetailsTblAdmin)
admin.site.register(ClientCommunicationDetailsTbl, ClientCommunicationDetailsTblAdmin)
admin.site.register(ClientCommunicationAttachmentsDetailsTbl, ClientCommunicationAttachmentsDetailsTblAdmin)
admin.site.register(Asset_Class_Details, AssetClassAdmin)
admin.site.register(Asset_Sub_Class_Details, AssetSubClassAdmin)
admin.site.register(Security_Details, SecurityAdmin)
admin.site.register(Security_Price_Details, SecurityPriceAdmin)
admin.site.register(Trade_Details, TradeDetailsAdmin)
admin.site.register(Position_Details, PositionDetailsAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(SecurityState, SecurityStateAdmin)
admin.site.register(BenchmarkIndex, BenchmarkIndexAdmin)
admin.site.register(SecurityType, SecurityTypeAdmin)
admin.site.register(Firmtype, FirmtypeAdmin)
admin.site.register(Clientpriority, ClientpriorityAdmin)
admin.site.register(ContactPersonDetails, ContactPersonDetailsAdmin)
admin.site.register(ZAMPerson, ZAMPersonAdmin)
admin.site.register(CommunicationTypes, CommunicationTypesAdmin)
admin.site.register(SecurityCountry, SecurityCountryAdmin)
admin.site.register(SecuritySector, SecuritySectorAdmin)
admin.site.register(ResearchAttachmentTypes, ResearchAttachmentTypesAdmin)
admin.site.register(Focus_List, FocusListAdmin)
admin.site.register(Active_List, ActiveListAdmin)
admin.site.register(Portfolio_List, PortfolioListAdmin)
admin.site.register(FocusListResearchLog, FocusListResearchLogAdmin)
admin.site.register(ActiveListResearchLog, ActiveListResearchLogAdmin)
admin.site.register(PortfolioListResearchLog, PortfolioListResearchLogAdmin)
admin.site.register(ActiveListAttechment, ActiveListAttechmentAdmin)
admin.site.register(FocusListAttechment, FocusListAttechmentAdmin)
admin.site.register(PortfolioListAttechment, PortfolioListAttechmentAdmin)
admin.site.register(FocusListMiscleneousAttachment, FocusListMiscleneousAttachmentAdmin)
admin.site.register(ActiveListMiscleneousAttachment, ActiveListMiscleneousAttachmentAdmin)
admin.site.register(PortfolioMiscleneousAttachment, PortfolioMiscleneousAttachmentAdmin)
admin.site.register(QuestionType, QuestionTypeAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Responseto, ResponsetoAdmin)
admin.site.register(Variable)
admin.site.register(VariableType)
admin.site.register(AccountType)
admin.site.register(Full_Asset_Tool)
admin.site.register(Goal_Parameter_Year)
admin.site.register(Goal_Setting_Parameter)
