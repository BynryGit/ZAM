# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customerapp', '0001_initial'),
        ('zamapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='user_id',
            field=models.ForeignKey(related_name='userg_id', to='zamapp.UserProfile', null=True),
        ),
        migrations.AddField(
            model_name='customervariable',
            name='customer_id',
            field=models.ForeignKey(related_name='variable_customer_id', to='customerapp.CustomerPersonalInfo', null=True),
        ),
        migrations.AddField(
            model_name='customervariable',
            name='variable',
            field=models.ForeignKey(related_name='customer_variable_id', to='zamapp.Variable', null=True),
        ),
        migrations.AddField(
            model_name='customerpersonalinfo',
            name='user',
            field=models.ForeignKey(to='zamapp.UserProfile', null=True),
        ),
        migrations.AddField(
            model_name='customerchildreninfo',
            name='customer_id',
            field=models.ForeignKey(related_name='customer_id', to='customerapp.CustomerPersonalInfo', null=True),
        ),
        migrations.AddField(
            model_name='customerbankaccountdetails',
            name='account_id',
            field=models.ForeignKey(related_name='account_type', to='zamapp.AccountType', null=True),
        ),
        migrations.AddField(
            model_name='customerbankaccountdetails',
            name='currency',
            field=models.ForeignKey(related_name='account_currency', to='zamapp.Currency', null=True),
        ),
        migrations.AddField(
            model_name='customerbankaccountdetails',
            name='user',
            field=models.ForeignKey(related_name='account_user', to='zamapp.UserProfile', null=True),
        ),
        migrations.AddField(
            model_name='customer_product',
            name='customer_id',
            field=models.ForeignKey(related_name='cust_id', to='customerapp.CustomerPersonalInfo', null=True),
        ),
        migrations.AddField(
            model_name='customer_product',
            name='product_id',
            field=models.ForeignKey(related_name='prod_id', to='customerapp.Product', null=True),
        ),
        migrations.AddField(
            model_name='customer_product',
            name='user_id',
            field=models.ForeignKey(related_name='userp_id', to='zamapp.UserProfile', null=True),
        ),
    ]
