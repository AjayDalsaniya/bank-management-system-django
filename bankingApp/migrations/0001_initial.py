# Generated by Django 4.2.3 on 2024-01-06 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(max_length=30)),
                ('account_number', models.CharField(max_length=30, null=True)),
                ('aadhar_card_number', models.CharField(max_length=16)),
                ('pan_card_number', models.CharField(max_length=16)),
                ('aadhar_card', models.FileField(default='media/no-image.png', upload_to='media/images/')),
                ('pan_card', models.FileField(default='media/no-image.png', upload_to='media/images/')),
                ('nominee_name', models.CharField(max_length=30)),
                ('nominee_relationship', models.CharField(max_length=30)),
                ('balance', models.IntegerField(default=500)),
                ('loanBalance', models.IntegerField(null=True)),
                ('tpassword', models.CharField(max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(max_length=30)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('mobile_no', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=60)),
                ('gender', models.CharField(max_length=30, null=True)),
                ('date', models.CharField(max_length=20, null=True)),
                ('country', models.CharField(max_length=30, null=True)),
                ('state', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=20, null=True)),
                ('pic', models.FileField(default='media/manager.png', upload_to='media/manager/')),
                ('mngTpassword', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('cust_no', models.BigIntegerField(default=None, primary_key=True, serialize=False)),
                ('mngid', models.CharField(max_length=30, null=True)),
                ('account_number', models.CharField(max_length=30, null=True)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('mobile_no', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=20)),
                ('date', models.CharField(max_length=20, null=True)),
                ('country', models.CharField(default='India', max_length=30, null=True)),
                ('state', models.CharField(max_length=30, null=True)),
                ('city', models.CharField(max_length=30)),
                ('address', models.TextField()),
                ('signature', models.FileField(default='media/manager.png', upload_to='media/signature/')),
                ('pic', models.FileField(default='media/manager.png', upload_to='media/customer/')),
                ('manager_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bankingApp.branch')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('role', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transcations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tpassword', models.CharField(max_length=300)),
                ('account_number', models.CharField(max_length=30, null=True)),
                ('title', models.CharField(max_length=60)),
                ('transcations_type', models.CharField(max_length=60)),
                ('amount', models.IntegerField(default=500)),
                ('created_at', models.CharField(max_length=60)),
                ('bank_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bankingApp.account')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bankingApp.customer')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bankingApp.user')),
            ],
        ),
        migrations.CreateModel(
            name='paymentLoan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=30, null=True)),
                ('paymentDate', models.CharField(max_length=60)),
                ('paymentAmount', models.CharField(max_length=60)),
                ('loanBalance', models.CharField(max_length=60)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bankingApp.customer')),
                ('manager_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bankingApp.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=30, null=True)),
                ('loan_type', models.CharField(max_length=60)),
                ('loan_amount', models.CharField(max_length=60)),
                ('interest_rate', models.CharField(max_length=60, null=True)),
                ('periods', models.CharField(max_length=60)),
                ('interest_amount', models.CharField(max_length=60)),
                ('monthli_amount', models.CharField(max_length=60)),
                ('totalAmount', models.CharField(max_length=60, null=True)),
                ('loanDate', models.CharField(max_length=60, null=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bankingApp.customer')),
                ('manager_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bankingApp.branch')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bankingApp.user'),
        ),
        migrations.AddField(
            model_name='branch',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bankingApp.user'),
        ),
        migrations.AddField(
            model_name='account',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bankingApp.customer'),
        ),
        migrations.AddField(
            model_name='account',
            name='manager_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bankingApp.branch'),
        ),
    ]