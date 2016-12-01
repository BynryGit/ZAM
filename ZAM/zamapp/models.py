from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


ROW_STATUS = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
)

VIEW_STATUS = (
    ('Read', 'Read'),
    ('Unread', 'Unread'),
)

SECURITY_VIEW = (
    ('Hold', 'Hold'),
    ('Buy', 'Buy'),
    ('Sell', 'Sell'),
)
VERIFICATION_STATUS = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

ATTACHMENTS = "media"
PORTFOLIO_MODEL = "portfolio/model"
PORTFOLIO_LASTMANAGEMENT = "portfolio/last_management"
PORTFOLIO_LASTANAKYST = "portfolio/last_analyst"
PORTFOLIO_INVESTMENT = "portfolio/investment"

ACTIVE_INVESTMENTNOTE = "active_list/investment_note"
ACTIVE_MODEL = "active_list/model"
ACTIVE_MANAGEMENT = "active_list/management_interview"
ACTIVE_ANALYST = "active_list/analyst_interview"

FOCUSLIST_COMMUNICATION = "research/focuslistcommunication"
ACTIVELIST_COMMUNICATION = "research/activelistcommunication"
PORTFOLIOLIST_COMMUNICATION = "research/portfoliolistcommunication"

FOCUSLIST_MISCLENEOUS_ATTACHMENT = "focus_list/miscleneous_focus"
ACTIVELIST_MISCLENEOUS_ATTACHMENT = "active_list/miscleneous_active"
PORTFOLIO_MISCLENEOUS_ATTACHMENT = "portfolio/miscleneous_portfolio"


class UserRole(models.Model):
    role_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=100, null=True)
    role_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    role_created_by = models.CharField(max_length=150, null=True)
    role_created_date = models.DateTimeField(null=True)
    role_updated_by = models.CharField(max_length=150, null=True)
    role_updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.role)


# Create your models here.
class UserProfile(User):
    user_id = models.AutoField(primary_key=True)
    role_id = models.ForeignKey(UserRole, related_name='UserRole', null=True, default=None)
    user_first_name = models.CharField(max_length=150, null=True)
    user_last_name = models.CharField(max_length=150, null=True)
    user_email_id = models.CharField(max_length=150, null=True)
    user_address = models.CharField(max_length=150, null=True)
    user_city = models.CharField(max_length=100, null=True)
    user_state = models.CharField(max_length=100, null=True)
    user_contact_number = models.CharField(max_length=100, null=True)
    user_pincode = models.CharField(max_length=20, null=True)
    user_emailId_verified = models.CharField(max_length=150, null=True, default='No', choices=VERIFICATION_STATUS)
    welcome_mail = models.CharField(max_length=15, null=True, default='No', choices=VERIFICATION_STATUS)
    row_status = models.CharField(max_length=150, null=True, default='Active', choices=ROW_STATUS)
    user_created_by = models.CharField(max_length=150, null=True)
    user_created_date = models.DateTimeField(null=True)
    user_updated_by = models.CharField(max_length=150, null=True)
    user_updated_date = models.DateTimeField(null=True)
    user_title = models.CharField(max_length=15, null=True)

    def __unicode__(self):
        return unicode(str(self.user_id) + " name: " + str(self.user_first_name) + " uid: " + str(self.user_email_id))


# -------------------------------Master Tables-------------------------------


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=100, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    country_created_by = models.CharField(max_length=150, null=True)
    country_created_date = models.DateTimeField(null=True)
    country_updated_by = models.CharField(max_length=150, null=True)
    country_updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.country_name)


class SecuritySector(models.Model):
    sector_id = models.AutoField(primary_key=True)
    sector_name = models.CharField(max_length=100, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    sector_created_by = models.CharField(max_length=150, null=True)
    sector_created_date = models.DateTimeField(null=True)
    sector_updated_by = models.CharField(max_length=150, null=True)
    sector_updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.sector_name)


class Firmtype(models.Model):
    firmtype_id = models.AutoField(primary_key=True)
    firm_name = models.CharField(max_length=100, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    firm_created_by = models.CharField(max_length=150, null=True)
    firm_created_date = models.DateTimeField(null=True)
    firm_updated_by = models.CharField(max_length=150, null=True)
    firm_updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.firmtype_id)


class Clientpriority(models.Model):
    priority_id = models.AutoField(primary_key=True)
    priority_name = models.CharField(max_length=100, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    priority_created_by = models.CharField(max_length=150, null=True)
    priority_created_date = models.DateTimeField(null=True)
    priority_updated_by = models.CharField(max_length=150, null=True)
    priority_updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.priority_name)


class SecurityState(models.Model):
    state_id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=150, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    state_created_by = models.CharField(max_length=150, null=True)
    state_created_date = models.DateTimeField(null=True)
    state_updated_by = models.CharField(max_length=150, null=True)
    state_updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.state)


class SecurityType(models.Model):
    securitytype_id = models.AutoField(primary_key=True)
    securitytype = models.CharField(max_length=150, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    securitytype_created_by = models.CharField(max_length=150, null=True)
    securitytype_created_date = models.DateTimeField(null=True)
    securitytype_updated_by = models.CharField(max_length=150, null=True)
    securitytype_updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.securitytype)


class SecurityCountry(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=100, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    country_created_by = models.CharField(max_length=150, null=True)
    country_created_date = models.DateTimeField(null=True)
    country_updated_by = models.CharField(max_length=150, null=True)
    country_updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.country_name)


class Currency(models.Model):
    currency_id = models.AutoField(primary_key=True)
    country_id = models.ForeignKey(SecurityCountry, related_name='currency_country', null=True)
    currency = models.CharField(max_length=150, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    Currency_created_by = models.CharField(max_length=150, null=True)
    Currency_created_date = models.DateTimeField(null=True)
    Currency_updated_by = models.CharField(max_length=150, null=True)
    Currency_updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.currency)


class BenchmarkIndex(models.Model):
    benchmarkindex_id = models.AutoField(primary_key=True)
    benchmarkindex = models.CharField(max_length=150, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    benchmarkindex_created_by = models.CharField(max_length=150, null=True)
    benchmarkindex_created_date = models.DateTimeField(null=True)
    benchmarkindex_updated_by = models.CharField(max_length=150, null=True)
    benchmarkindex_updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.benchmarkindex)


class Asset_Class_Details(models.Model):
    asset_class_id = models.AutoField(primary_key=True)
    asset_class_name = models.CharField(max_length=100, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    asset_class_created_by = models.CharField(max_length=100, null=True)
    asset_class_updated_by = models.CharField(max_length=100, null=True)
    asset_class_created_date = models.DateTimeField(null=True)
    asset_class_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.asset_class_name)


class Asset_Sub_Class_Details(models.Model):
    asset_sub_class_id = models.AutoField(primary_key=True)
    asset_class_id = models.ForeignKey(Asset_Class_Details, related_name='assetclassid', null=True)
    asset_sub_class_name = models.CharField(max_length=100, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    asset_sub_class_created_by = models.CharField(max_length=100, null=True)
    asset_sub_class_updated_by = models.CharField(max_length=100, null=True)
    asset_sub_class_created_date = models.DateTimeField(null=True)
    asset_sub_class_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.asset_class_id.asset_class_name + ' - ' + self.asset_sub_class_name)


class ZAMPerson(models.Model):
    zam_person_id = models.AutoField(primary_key=True)
    zam_person_name = models.CharField(max_length=100, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    zam_person_created_by = models.CharField(max_length=150, null=True)
    zam_person_created_date = models.DateTimeField(null=True)
    zam_person_updated_by = models.CharField(max_length=150, null=True)
    zam_person_updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.zam_person_name)


class CommunicationTypes(models.Model):
    communicationtype_id = models.AutoField(primary_key=True)
    communicationtype_name = models.CharField(max_length=100, null=True)
    communicationtype_created_by = models.CharField(max_length=100, null=True)
    communicationtype_updated_by = models.CharField(max_length=100, null=True)
    communicationtype_created_date = models.DateTimeField(null=True)
    communicationtype_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.communicationtype_name)


class ClientDetailsTbl(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_firm = models.CharField(max_length=100, null=True)
    firmtype_id = models.ForeignKey(Firmtype, related_name='firmtype', null=True)
    client_phone = models.CharField(max_length=30, null=True)
    client_contact_email = models.CharField(max_length=50, null=True)
    client_relationship_manager = models.CharField(max_length=50, null=True)
    client_office_address_line_1 = models.CharField(max_length=100, null=True)
    client_office_address_line_2 = models.CharField(max_length=100, null=True)
    city_name = models.CharField(max_length=100, blank=True, null=True)
    state_name = models.CharField(max_length=100, blank=True, null=True)
    country_id = models.ForeignKey(Country, related_name='country_names', null=True)
    client_pincode = models.CharField(max_length=20, null=True)
    client_reference_person = models.CharField(max_length=100, null=True)
    client_comment = models.CharField(max_length=1000, null=True)
    client_invested_in_asia = models.CharField(max_length=100, null=True)
    client_invested_in_hedge_fund = models.CharField(max_length=100, null=True)
    client_stage = models.CharField(max_length=50, null=True)
    priority_id = models.ForeignKey(Clientpriority, related_name='priority', null=True)
    client_record_status = models.CharField(max_length=150, null=True, default="Active", choices=ROW_STATUS)
    client_created_by = models.CharField(max_length=50, null=True)
    client_updated_by = models.CharField(max_length=50, null=True)
    client_created_date = models.DateTimeField(null=True)
    client_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.client_id)


class ClientIPDetailsTbl(models.Model):
    client_ip_id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey(ClientDetailsTbl, related_name='clientid', null=True)
    client_ecv = models.FloatField(null=True)
    asset_class_one_name = models.ForeignKey(Asset_Class_Details, related_name='assetclass_one', null=True)
    asset_class_one_percentage = models.FloatField(null=True)
    asset_class_two_name = models.ForeignKey(Asset_Class_Details, related_name='assetclass_two', null=True)
    asset_class_two_percentage = models.FloatField(null=True)
    asset_class_three_name = models.ForeignKey(Asset_Class_Details, related_name='assetclass_three', null=True)
    asset_class_three_percentage = models.FloatField(null=True)
    client_risk_category = models.CharField(max_length=20, null=True)
    client_ip_record_status = models.CharField(max_length=150, null=True, default="Active", choices=ROW_STATUS)
    client_ip_created_by = models.CharField(max_length=100, null=True)
    client_ip_updated_by = models.CharField(max_length=100, null=True)
    client_ip_created_date = models.DateTimeField(null=True)
    client_ip_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.client_ip_id)


class ContactPersonDetails(models.Model):
    contact_person_id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey(ClientDetailsTbl, related_name='clientContid', null=True)
    contact_person_first_name = models.CharField(max_length=100, null=True)
    contact_person_last_name = models.CharField(max_length=100, null=True)
    contact_person_contact_no = models.CharField(max_length=100, null=True)
    contact_person_email_id = models.CharField(max_length=100, null=True)
    contact_person_created_by = models.CharField(max_length=100, null=True)
    contact_person_updated_by = models.CharField(max_length=100, null=True)
    contact_person_created_date = models.DateTimeField(null=True)
    contact_person_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.contact_person_id)


class ClientCommunicationDetailsTbl(models.Model):
    communication_Id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey(ClientDetailsTbl, related_name='clientComid', null=True)
    zam_person_id = models.ForeignKey(ZAMPerson, related_name='zam_person', null=True)
    contact_person_id = models.ForeignKey(ContactPersonDetails, related_name='clientCond', null=True)
    communication_date = models.DateField(null=True)
    communication_desc = models.CharField(max_length=1000, null=True)
    communication_attachment = models.CharField(max_length=100, null=True)
    communicationtype_id = models.ForeignKey(CommunicationTypes, related_name='comType', null=True)
    record_status = models.CharField(max_length=100, null=True)
    communication_created_by = models.CharField(max_length=100, null=True)
    communication_updated_by = models.CharField(max_length=100, null=True)
    communication_created_date = models.DateTimeField(null=True)
    communication_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.communication_Id)


class ClientCommunicationAttachmentsDetailsTbl(models.Model):
    attachment_id = models.AutoField(primary_key=True)
    communication_Id = models.ForeignKey(ClientCommunicationDetailsTbl, related_name='communicationId', null=True)
    attachment_file_path = models.FileField(upload_to=ATTACHMENTS, max_length=500, null=True, blank=True)
    attacchment_status = models.CharField(max_length=20, null=True)
    attacchment_created_by = models.CharField(max_length=100, null=True)
    attacchment_updated_by = models.CharField(max_length=100, null=True)
    attacchment_created_date = models.DateTimeField(null=True)
    attacchment_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.attachment_id)


class Security_Details(models.Model):
    security_id = models.AutoField(primary_key=True)
    asset_sub_class_id = models.ForeignKey(Asset_Sub_Class_Details, related_name='assetsubclass', null=True)
    sector_id = models.ForeignKey(SecuritySector, null=True)
    security_name = models.CharField(max_length=100, null=True)
    security_isin = models.CharField(max_length=100, null=True)
    security_type = models.ForeignKey(SecurityType, related_name='securityType', null=True)
    security_benchmark_index = models.ForeignKey(BenchmarkIndex, related_name='securityBenchmarkIndex', null=True)
    security_bloomer_ticker = models.CharField(max_length=100, null=True)
    security_security_state = models.ForeignKey(SecurityState, related_name='securitySate', null=True)
    security_local_currency = models.ForeignKey(Currency, related_name='securityCurrency', null=True)
    country_id = models.ForeignKey(SecurityCountry, related_name='contry_currency', null=True)
    security_beta = models.FloatField(max_length=10, null=True, blank=True)
    security_lot_size = models.IntegerField(max_length=10, null=True, blank=True)
    record_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    security_created_by = models.CharField(max_length=100, null=True)
    security_updated_by = models.CharField(max_length=100, null=True)
    security_created_date = models.DateTimeField(null=True)
    security_updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(str(self.security_id) + "  " + str(self.security_name))


class Security_Price_Details(models.Model):
    security_price_id = models.AutoField(primary_key=True)
    security_id = models.ForeignKey(Security_Details, related_name='securityid', null=True)
    security_price_date = models.DateTimeField(null=True)
    security_last_price = models.FloatField(max_length=10, null=True)
    security_in_price = models.FloatField(max_length=10, null=True)
    security_usd_in = models.FloatField(max_length=10, null=True)
    security_usd_last = models.FloatField(max_length=10, null=True)
    security_fx_rate_in = models.FloatField(max_length=10, null=True)
    security_fx_rate_last = models.FloatField(max_length=10, null=True)
    security_one_d = models.FloatField(max_length=10, null=True)
    record_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    security_price_created_by = models.CharField(max_length=100, null=True)
    security_price_updated_by = models.CharField(max_length=100, null=True)
    security_price_created_date = models.DateTimeField(null=True)
    security_price_updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(str(self.security_id) + ' vkm' + str(self.security_price_id))


class Trade_Details(models.Model):
    trade_id = models.AutoField(primary_key=True)
    security_id = models.ForeignKey(Security_Details, related_name='securityTrid', null=True)
    trade_date = models.DateTimeField(null=True)
    buy_sell_indicator = models.CharField(max_length=100, null=True)
    trade_security_quantity = models.CharField(max_length=100, null=True)
    trade_amount = models.CharField(max_length=100, null=True)
    trade_price = models.CharField(max_length=100, null=True)
    fx_price = models.CharField(max_length=100, null=True)
    broker = models.CharField(max_length=100, null=True)
    lot_size = models.FloatField(max_length=10, null=True, blank=True)
    record_status = models.CharField(max_length=20, null=True, choices=ROW_STATUS)
    trade_created_by = models.CharField(max_length=100, null=True)
    trade_updated_by = models.CharField(max_length=100, null=True)
    trade_created_date = models.DateTimeField(null=True)
    trade_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(str(self.trade_date) + ' ' + str(self.security_id.security_name))


class Position_Details(models.Model):
    position_id = models.AutoField(primary_key=True)
    security_id = models.ForeignKey(Security_Details, related_name='securityPosDid', null=True)
    last_price = models.FloatField(max_length=10, null=True)
    in_price = models.FloatField(max_length=10, null=True)
    position = models.FloatField(max_length=10, null=True)
    move_since_incepton = models.FloatField(max_length=10, null=True)
    position_security_quntity = models.CharField(max_length=100, null=True)
    in_principal = models.FloatField(max_length=10, null=True)
    market_value = models.FloatField(max_length=10, null=True)
    beta_adj = models.FloatField(max_length=10, null=True)
    profit_and_loss = models.FloatField(max_length=10, null=True)
    contrib_daily = models.FloatField(max_length=10, null=True)
    portfolio_return_contrib = models.FloatField(max_length=10, null=True)
    FX = models.CharField(max_length=20, null=True)
    beta = models.FloatField(max_length=10, null=True)
    FX_in = models.FloatField(max_length=10, null=True)
    fx_contrib = models.FloatField(max_length=10, null=True)
    position_date = models.DateTimeField(null=True)
    position_security_market_value = models.CharField(max_length=100, null=True)
    position_long_short_indicator = models.CharField(max_length=100, null=True)
    position_status = models.CharField(max_length=20, null=True)
    position_created_by = models.CharField(max_length=100, null=True)
    position_updated_by = models.CharField(max_length=100, null=True)
    position_created_date = models.DateTimeField(null=True)
    position_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(
            str(self.position_id) + " " + str(self.security_id.security_name) + " " + str(self.position_date))


class ResearchAttachmentTypes(models.Model):
    communicationtype_id = models.AutoField(primary_key=True)
    communicationtype_name = models.CharField(max_length=100, null=True)
    record_status = models.CharField(max_length=150, null=True, default="Active", choices=ROW_STATUS)
    communicationtype_created_by = models.CharField(max_length=100, null=True)
    communicationtype_updated_by = models.CharField(max_length=100, null=True)
    communicationtype_created_date = models.DateTimeField(null=True)
    communicationtype_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.communicationtype_name)


class Focus_List(models.Model):
    focuslist_company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    country_id = models.ForeignKey(SecurityCountry, related_name='focus_country', null=True)
    local_currency = models.ForeignKey(Currency, null=True)
    bloomberg_ticker = models.CharField(max_length=200, blank=True, null=True)
    source = models.CharField(max_length=200, blank=True, null=True)
    mkt_cap = models.FloatField(null=True, blank=True)
    daily_turnover = models.FloatField(null=True)
    target_price = models.FloatField(null=True)
    cmp = models.FloatField(null=True)
    move_since_inseption = models.CharField(max_length=200, blank=True, null=True)
    up_down_side = models.FloatField(null=True)
    management_quality = models.CharField(max_length=200, blank=True, null=True)
    company_record_status = models.CharField(max_length=150, null=True, default="Active", choices=ROW_STATUS)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, blank=True, null=True)
    updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.company_name)


class FocusListMiscleneousAttachment(models.Model):
    misleneous_attechment_id = models.AutoField(primary_key=True)
    focuslist_company_id = models.ForeignKey(Focus_List, related_name='focus_list', null=True)
    attachment_path = models.FileField(upload_to=FOCUSLIST_MISCLENEOUS_ATTACHMENT, max_length=500, null=True,
                                       blank=True)
    attachment_date = models.DateTimeField(null=True)
    attachment_created_by = models.CharField(max_length=100, null=True)
    attachment_updated_by = models.CharField(max_length=100, null=True)
    attachment_created_date = models.DateTimeField(null=True)
    attachment_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.misleneous_attechment_id)


class FocusListResearchLog(models.Model):
    focus_researchlog_Id = models.AutoField(primary_key=True)
    focuslist_company_id = models.ForeignKey(Focus_List, related_name='focus_id', null=True)
    zam_person_id = models.CharField(max_length=200, blank=True, null=True)
    company_personel = models.CharField(max_length=200, blank=True, null=True)
    designation = models.CharField(max_length=200, blank=True, null=True)
    bank_name = models.CharField(max_length=200, blank=True, null=True)
    analyst_name = models.CharField(max_length=200, blank=True, null=True)
    log_date = models.DateField(null=True)
    log_desc = models.CharField(max_length=1000, null=True)
    log_attachment = models.FileField(upload_to=FOCUSLIST_COMMUNICATION, max_length=500, null=True, blank=True)
    communicationtype_id = models.ForeignKey(ResearchAttachmentTypes, related_name='focus_att_type', blank=True,
                                             null=True)
    record_status = models.CharField(max_length=150, null=True, default="Active", choices=ROW_STATUS)
    communication_created_by = models.CharField(max_length=100, null=True)
    communication_updated_by = models.CharField(max_length=100, null=True)
    communication_created_date = models.DateTimeField(null=True)
    communication_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.focus_researchlog_Id)


class Active_List(models.Model):
    activelist_company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    country_id = models.ForeignKey(SecurityCountry, related_name='Countryid', null=True)
    local_currency = models.ForeignKey(Currency, related_name='Currency', null=True)
    bloomberg_ticker = models.CharField(max_length=200, blank=True, null=True)
    move_since_inseption = models.CharField(max_length=200, blank=True, null=True)
    model_file = models.FileField(upload_to=ACTIVE_MODEL, max_length=500, null=True, blank=True)
    model_updated_date = models.DateTimeField(default=datetime.now())
    analyst_interview_file = models.FileField(upload_to=ACTIVE_ANALYST, max_length=500, null=True, blank=True)
    analyst_interview_date = models.DateTimeField(default=datetime.now())
    management_interview_file = models.FileField(upload_to=ACTIVE_MANAGEMENT, max_length=500, null=True, blank=True)
    management_interview_date = models.DateTimeField(default=datetime.now())
    investment_note = models.DateTimeField(default=datetime.now())
    investment_note_file = models.FileField(upload_to=ACTIVE_INVESTMENTNOTE, max_length=500, null=True, blank=True)
    congruence = models.CharField(max_length=150, null=True, default='No', choices=VERIFICATION_STATUS)
    industry_analysis = models.CharField(max_length=150, null=True, default='No', choices=VERIFICATION_STATUS)
    target_price = models.CharField(max_length=150, null=True, blank=True)
    cmp = models.CharField(max_length=150, null=True, blank=True)
    up_down_side = models.CharField(max_length=150, null=True, blank=True)
    management_quality = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, blank=True, null=True)
    updated_date = models.DateTimeField(default=datetime.now())
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)

    def __unicode__(self):
        return unicode(self.company_name)


class ActiveListMiscleneousAttachment(models.Model):
    misleneous_attechment_id = models.AutoField(primary_key=True)
    activelist_company_id = models.ForeignKey(Active_List, related_name='active_list', null=True)
    attachment_path = models.FileField(upload_to=ACTIVELIST_MISCLENEOUS_ATTACHMENT, max_length=500, null=True,
                                       blank=True)
    attachment_date = models.DateTimeField(null=True)
    attachment_created_by = models.CharField(max_length=100, null=True)
    attachment_updated_by = models.CharField(max_length=100, null=True)
    attachment_created_date = models.DateTimeField(null=True)
    attachment_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.misleneous_attechment_id)


class ActiveListResearchLog(models.Model):
    active_researchlog_Id = models.AutoField(primary_key=True)
    activelist_company_id = models.ForeignKey(Active_List, related_name='active_id', null=True)
    zam_person_id = models.CharField(max_length=200, blank=True, null=True)
    company_personel = models.CharField(max_length=200, blank=True, null=True)
    designation = models.CharField(max_length=200, blank=True, null=True)
    bank_name = models.CharField(max_length=200, blank=True, null=True)
    analyst_name = models.CharField(max_length=200, blank=True, null=True)
    log_date = models.DateField(null=True)
    log_desc = models.CharField(max_length=2000, null=True)
    log_attachment = models.FileField(upload_to=ACTIVELIST_COMMUNICATION, max_length=500, null=True, blank=True)
    communicationtype_id = models.ForeignKey(ResearchAttachmentTypes, related_name='active_att_type', null=True)
    record_status = models.CharField(max_length=150, null=True, default="Active", choices=ROW_STATUS)
    communication_created_by = models.CharField(max_length=100, null=True)
    communication_updated_by = models.CharField(max_length=100, null=True)
    communication_created_date = models.DateTimeField(null=True)
    communication_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.active_researchlog_Id)


class ActiveListAttechment(models.Model):
    attechment_id = models.AutoField(primary_key=True)
    active_researchlog_id = models.ForeignKey(ActiveListResearchLog, related_name='active_research_log', null=True)
    attachment_path = models.FileField(upload_to=ACTIVELIST_COMMUNICATION, max_length=500, null=True, blank=True)
    attachment_date = models.DateTimeField(null=True)
    attachment_created_by = models.CharField(max_length=100, null=True)
    attachment_updated_by = models.CharField(max_length=100, null=True)
    attachment_created_date = models.DateTimeField(null=True)
    attachment_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.attechment_id)


class Portfolio_List(models.Model):
    portfolio_company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    country_id = models.ForeignKey(SecurityCountry, related_name='portfolio_country', null=True)
    local_currency = models.ForeignKey(Currency, null=True)
    bloomberg_ticker = models.CharField(max_length=200, blank=True, null=True)
    model_file = models.FileField(upload_to=PORTFOLIO_MODEL, max_length=500, null=True, blank=True)
    model_updated_date = models.DateTimeField(default=datetime.now())
    last_analyst_call_file = models.FileField(upload_to=PORTFOLIO_LASTANAKYST, max_length=500, null=True, blank=True)
    last_analyst_call_date = models.DateTimeField(default=datetime.now())
    last_management_call_file = models.FileField(upload_to=PORTFOLIO_LASTMANAGEMENT, max_length=500, null=True,
                                                 blank=True)
    last_management_call_date = models.DateTimeField(default=datetime.now())
    investment_note = models.DateTimeField(default=datetime.now())
    investment_note_file = models.FileField(upload_to=PORTFOLIO_INVESTMENT, max_length=500, null=True, blank=True)
    company_record_status = models.CharField(max_length=150, null=True, default="Active", choices=ROW_STATUS)
    target_price = models.CharField(max_length=200, blank=True, null=True)
    cmp = models.CharField(max_length=200, blank=True, null=True)
    move_since_inseption = models.CharField(max_length=200, blank=True, null=True)
    up_down_side = models.CharField(max_length=200, blank=True, null=True)
    management_quality = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, blank=True, null=True)
    updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.company_name)


class PortfolioMiscleneousAttachment(models.Model):
    misleneous_attechment_id = models.AutoField(primary_key=True)
    portfolio_company_id = models.ForeignKey(Portfolio_List, related_name='portfolio_list', null=True)
    attachment_path = models.FileField(upload_to=PORTFOLIO_MISCLENEOUS_ATTACHMENT, max_length=500, null=True,
                                       blank=True)
    attachment_date = models.DateTimeField(null=True)
    attachment_created_by = models.CharField(max_length=100, null=True)
    attachment_updated_by = models.CharField(max_length=100, null=True)
    attachment_created_date = models.DateTimeField(null=True)
    attachment_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.misleneous_attechment_id)


class PortfolioListResearchLog(models.Model):
    portfolio_researchlog_Id = models.AutoField(primary_key=True)
    portfolio_company_id = models.ForeignKey(Portfolio_List, related_name='portfolio_id', null=True)
    zam_person_id = models.CharField(max_length=200, blank=True, null=True)
    company_personel = models.CharField(max_length=200, blank=True, null=True)
    designation = models.CharField(max_length=200, blank=True, null=True)
    bank_name = models.CharField(max_length=200, blank=True, null=True)
    analyst_name = models.CharField(max_length=200, blank=True, null=True)
    log_date = models.DateField(null=True)
    log_desc = models.CharField(max_length=1000, null=True)
    log_attachment = models.FileField(upload_to=PORTFOLIOLIST_COMMUNICATION, max_length=500, null=True, blank=True)
    communicationtype_id = models.ForeignKey(ResearchAttachmentTypes, related_name='portfolio_att_type', null=True)
    record_status = models.CharField(max_length=150, null=True, default="Active", choices=ROW_STATUS)
    communication_created_by = models.CharField(max_length=100, null=True)
    communication_updated_by = models.CharField(max_length=100, null=True)
    communication_created_date = models.DateTimeField(null=True)
    communication_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.portfolio_researchlog_Id)


class FocusListAttechment(models.Model):
    attechment_id = models.AutoField(primary_key=True)
    focus_researchlog_Id = models.ForeignKey(FocusListResearchLog, related_name='focus_research_log', null=True)
    attachment_path = models.FileField(upload_to=FOCUSLIST_COMMUNICATION, max_length=500, null=True, blank=True)
    attachment_date = models.DateTimeField(null=True)
    attachment_created_by = models.CharField(max_length=100, null=True)
    attachment_updated_by = models.CharField(max_length=100, null=True)
    attachment_created_date = models.DateTimeField(null=True)
    attachment_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.attechment_id)


class PortfolioListAttechment(models.Model):
    attechment_id = models.AutoField(primary_key=True)
    portfolio_researchlog_Id = models.ForeignKey(PortfolioListResearchLog, related_name='port_research_log', null=True)
    attachment_path = models.FileField(upload_to=PORTFOLIOLIST_COMMUNICATION, max_length=500, null=True, blank=True)
    attachment_date = models.DateTimeField(null=True)
    attachment_created_by = models.CharField(max_length=100, null=True)
    attachment_updated_by = models.CharField(max_length=100, null=True)
    attachment_created_date = models.DateTimeField(null=True)
    attachment_updated_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return unicode(self.attechment_id)


class QuestionType(models.Model):
    question_type_id = models.AutoField(primary_key=True)
    question_type = models.CharField(max_length=100, null=True)
    created_by = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=100, null=True)
    updated_date = models.DateTimeField(default=datetime.now())
    record_status = models.CharField(max_length=150, null=True, default="Active", choices=ROW_STATUS)

    def __unicode__(self):
        return unicode(self.question_type)


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_type = models.ForeignKey(QuestionType, related_name='qtype_id', null=True)
    question = models.CharField(max_length=500, null=True)
    question_ask_date = models.DateTimeField(default=datetime.now())
    user_id = models.ForeignKey(UserProfile, related_name='userq_id', null=True)
    response_count = models.CharField(max_length=20, null=True, blank=True)
    record_status = models.CharField(max_length=150, null=True, default="Active", choices=ROW_STATUS)
    read_status = models.CharField(max_length=150, null=True, default="Unread", choices=VIEW_STATUS)

    def __unicode__(self):
        return unicode(self.question)


class Response(models.Model):
    response_id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(Question, related_name='quest_id', null=True)
    response = models.CharField(max_length=1000, null=True)
    response_date = models.DateTimeField(default=datetime.now())
    user_id = models.ForeignKey(UserProfile, related_name='userr_id', null=True)
    responseto_count = models.CharField(max_length=20, null=True, blank=True)
    record_status = models.CharField(max_length=150, null=True, default="Active", choices=ROW_STATUS)
    read_status = models.CharField(max_length=150, null=True, default="Unread", choices=VIEW_STATUS)

    def __unicode__(self):
        return unicode(self.response_id)


class Responseto(models.Model):
    responseto_id = models.AutoField(primary_key=True)
    response_id = models.ForeignKey(Response, related_name='respon_id', null=True)
    responseto = models.CharField(max_length=1000, null=True)
    responseto_date = models.DateTimeField(default=datetime.now())
    user_id = models.ForeignKey(UserProfile, related_name='userreto_id', null=True)
    record_status = models.CharField(max_length=150, null=True, default="Active", choices=ROW_STATUS)
    read_status = models.CharField(max_length=150, null=True, default="Unread", choices=VIEW_STATUS)

    def __unicode__(self):
        return unicode(self.responseto_id)


class VariableType(models.Model):
    variableType_id = models.AutoField(primary_key=True)
    variableType = models.CharField(null=True, max_length=255)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    created_by = models.CharField(max_length=150, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=150, null=True)
    updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.variableType)


class Variable(models.Model):
    variable_id = models.AutoField(primary_key=True)
    variableType_id = models.ForeignKey(VariableType, null=True)
    variable = models.CharField(null=True, max_length=255)
    percentage = models.FloatField(max_length=10, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    created_by = models.CharField(max_length=150, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=150, null=True)
    updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.variable)


class AccountType(models.Model):
    account_id = models.AutoField(primary_key=True)
    account_name = models.CharField(max_length=200, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    created_by = models.CharField(max_length=150, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=150, null=True)
    updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.account_name)


class Full_Asset_Tool(models.Model):
    full_asset_id = models.AutoField(primary_key=True)
    product       = models.CharField(null=True,max_length=255)
    product_name  = models.CharField(null=True,max_length=255)
    balance       = models.CharField(null=True,max_length=255)
    account_id    = models.ForeignKey(AccountType,related_name='acc_type',blank=True,null=True)
    duration      = models.CharField(null=True,max_length=255)
    pretax_rate    = models.FloatField(max_length=10, null=True)
    posttax_return    = models.FloatField(max_length=10, null=True)
    liquidity     = models.CharField(null=True,max_length=255)
    row_status = models.CharField(max_length=150, null=True, default="Active", choices=ROW_STATUS)
    created_by = models.CharField(max_length=150, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=150, null=True)
    updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.product_name)



class Goal_Parameter_Year(models.Model):
    goal_parameter_year_id = models.AutoField(primary_key=True)
    goal_parameter_year = models.CharField(max_length=200, null=True)
    created_by = models.CharField(max_length=150, null=True)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=150, null=True)
    updated_date = models.DateTimeField(null=True)

    def __unicode__(self):
        return unicode(self.goal_parameter_year) 
    
    
class Goal_Setting_Parameter(models.Model):
    goal_setting_parameter_id  =  models.AutoField(primary_key=True)
    goal_setting_parameter     =  models.CharField(max_length=200, null=True)
    goal_setting_parameter_per     =  models.FloatField(max_length=10, null=True)
    goal_parameter_year_id     = models.ForeignKey(Goal_Parameter_Year,related_name='goal_pr_yr_id', null=True)
    created_by = models.CharField(max_length=150, null=True)
    row_status = models.CharField(max_length=150, null=True, default=None, choices=ROW_STATUS)
    created_date = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=150, null=True)
    updated_date = models.DateTimeField(null=True)
    
    def __unicode__(self):
        return unicode(self.goal_setting_parameter) 
