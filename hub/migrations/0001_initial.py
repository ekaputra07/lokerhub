# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SocialLoginProvider'
        db.create_table('social_login_providers', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('provider_user_id', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'hub', ['SocialLoginProvider'])

        # Adding model 'Company'
        db.create_table('companies', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('email', self.gf('django.db.models.fields.EmailField')(default='', max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(default='', max_length=50, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('website', self.gf('django.db.models.fields.URLField')(default='', max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'hub', ['Company'])

        # Adding model 'Category'
        db.create_table('categories', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('indeed_query', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal(u'hub', ['Category'])

        # Adding model 'Job'
        db.create_table('jobs', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='INACTIVE', max_length=15)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
            ('is_premium', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hub.Company'])),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('job_type', self.gf('django.db.models.fields.CharField')(default='FULLTIME', max_length=15)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hub.Category'])),
            ('location', self.gf('django.db.models.fields.CharField')(default='', max_length=150, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('how_to_apply', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('started', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('ended', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'hub', ['Job'])

        # Adding model 'JobApplication'
        db.create_table('job_applications', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hub.Company'])),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hub.Job'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('resume', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('coverletter', self.gf('django.db.models.fields.TextField')()),
            ('read_status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'hub', ['JobApplication'])

        # Adding model 'IndeedJob'
        db.create_table('indeed_jobs', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hub.Category'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('jobkey', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('onmousedown', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
        ))
        db.send_create_signal(u'hub', ['IndeedJob'])

        # Adding model 'PremiumOrder'
        db.create_table('premium_orders', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hub.Job'], null=True, blank=True)),
            ('job_title', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('status', self.gf('django.db.models.fields.CharField')(default='UNPAID', max_length=15)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=2)),
            ('unique_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=2)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'hub', ['PremiumOrder'])

        # Adding model 'PaymentConfirmation'
        db.create_table('payment_confirmations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hub.PremiumOrder'])),
            ('bank_to', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('from_bank', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('from_name', self.gf('django.db.models.fields.CharField')(default='', max_length=150)),
            ('from_acc', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('from_amount', self.gf('django.db.models.fields.CharField')(default=100000, max_length=50)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            ('from_note', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('checked', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'hub', ['PaymentConfirmation'])


    def backwards(self, orm):
        # Deleting model 'SocialLoginProvider'
        db.delete_table('social_login_providers')

        # Deleting model 'Company'
        db.delete_table('companies')

        # Deleting model 'Category'
        db.delete_table('categories')

        # Deleting model 'Job'
        db.delete_table('jobs')

        # Deleting model 'JobApplication'
        db.delete_table('job_applications')

        # Deleting model 'IndeedJob'
        db.delete_table('indeed_jobs')

        # Deleting model 'PremiumOrder'
        db.delete_table('premium_orders')

        # Deleting model 'PaymentConfirmation'
        db.delete_table('payment_confirmations')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'hub.category': {
            'Meta': {'object_name': 'Category', 'db_table': "'categories'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indeed_query': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'hub.company': {
            'Meta': {'ordering': "['-pk']", 'object_name': 'Company', 'db_table': "'companies'"},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'hub.indeedjob': {
            'Meta': {'ordering': "['-created']", 'object_name': 'IndeedJob', 'db_table': "'indeed_jobs'"},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hub.Category']"}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jobkey': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'onmousedown': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'hub.job': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Job', 'db_table': "'jobs'"},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hub.Category']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hub.Company']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'ended': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'how_to_apply': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_premium': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_type': ('django.db.models.fields.CharField', [], {'default': "'FULLTIME'", 'max_length': '15'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'started': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'INACTIVE'", 'max_length': '15'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'hub.jobapplication': {
            'Meta': {'ordering': "['-created']", 'object_name': 'JobApplication', 'db_table': "'job_applications'"},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hub.Company']"}),
            'coverletter': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hub.Job']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'read_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'resume': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'hub.paymentconfirmation': {
            'Meta': {'ordering': "['-created']", 'object_name': 'PaymentConfirmation', 'db_table': "'payment_confirmations'"},
            'bank_to': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'checked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'from_acc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'from_amount': ('django.db.models.fields.CharField', [], {'default': '100000', 'max_length': '50'}),
            'from_bank': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'from_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'from_note': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hub.PremiumOrder']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'hub.premiumorder': {
            'Meta': {'object_name': 'PremiumOrder', 'db_table': "'premium_orders'"},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hub.Job']", 'null': 'True', 'blank': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'UNPAID'", 'max_length': '15'}),
            'unique_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '2'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'hub.socialloginprovider': {
            'Meta': {'object_name': 'SocialLoginProvider', 'db_table': "'social_login_providers'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'provider_user_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['hub']