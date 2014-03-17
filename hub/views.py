import random
import datetime
from urllib import quote
import urllib2
import json

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.timezone import now
from django.contrib import messages

from LoginRadius import LoginRadius

from hub.models import SocialLoginProvider, Company, Category, Job, IndeedJob, PremiumOrder
from hub.forms import CompanyForm, JobForm, JobApplicationForm, PaymentConfirmationForm, ProfileForm
from hub.utils import convert_gtm_to_utc, send_premium_activation_email, send_free_activation_email, tweet_job


def home_view(request):
    """
    Homepage view.
    """
    context = {
        'title': 'Lowongan kerja IT Indonesia',
        'description': 'LokerHub adalah situs penyedia informasi karir di bidang Teknologi Informasi. Berusaha memberi kesan baru dan segar buat situs lowongan kerja di Indonesia.',
        'categories': Category.objects.all(),
        'premium_jobs': Job.objects.filter(status='ACTIVE', approved=True, is_premium=True,
                                   ended__gte=now).order_by('-started'),
        'free_jobs': Job.objects.filter(status='ACTIVE', approved=True, is_premium=False,
                                   ended__gte=now).order_by('-started'),
    }
    return render_to_response('listing.html', context,
                              context_instance=RequestContext(request))


def login_view(request):
    """
    Login page.
    """
    if not request.user.is_authenticated():
        context = {
            'fb_auth_url': settings.LRD_FACEBOOK_AUTH_URL,
            'goo_auth_url': settings.LRD_GOOGLE_AUTH_URL,
            'lnkd_auth_url': settings.LRD_LINKEDIN_AUTH_URL,
        }
        return render_to_response('login.html', context,
                                   context_instance=RequestContext(request))
    raise Http404


@csrf_exempt
def logincallback_view(request):
    """
    LoginRadius social login callback.
    """
    if request.method == 'POST':
        lrd_token = request.POST.get('token', '')
        loginradius = LoginRadius(settings.LRD_API_SECRET, lrd_token)
        profile = loginradius.loginradius_get_data()

        u_provider = profile.get('Provider')
        u_ID = profile.get('ID', None)

        user = authenticate(provider=u_provider, provider_user_id=u_ID)

        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            u_emails = profile.get('Email', None)
            u_email = None
            if len(u_emails) > 0:
                u_email = u_emails[0].get('Value', None)

            u_firstname = profile.get('FirstName', '')
            u_lastname = profile.get('LastName', '')
            u_username = 'user%s' % random.randint(1000, 90000)

            try:
                user = User.objects.get(email=u_email)
            except User.DoesNotExist:
                # User with this email doesn't exist.
                # Create new user and login
                user = User(
                    username = u_username,
                    email = u_email,
                    first_name = u_firstname,
                    last_name = u_lastname
                )
                user.is_active = True
                user.save()

                provider_user = SocialLoginProvider(user=user,
                                                    name=u_provider,
                                                    provider_user_id=u_ID)
                provider_user.save()

                # Authenticate once again and login.
                u = authenticate(provider=u_provider, provider_user_id=u_ID)
                login(request, u)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                messages.error(request, 'Email sudah terdaftar dengan akun lain.', extra_tags='danger')
                return HttpResponseRedirect(reverse('login'))
            return HttpResponseRedirect(reverse('login'))

    raise Http404


@login_required
def logout_view(request):
    """
    Logout.
    """
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def dashboard_view(request):
    """
    Dashboard page.
    """
    user = request.user
    context = {
        'active_page': 'dashboard',
        'jobs': Job.objects.filter(user=user),
    }
    
    return render_to_response('dashboard.html', context,
                              context_instance=RequestContext(request))

# ----------------------------------- Profile ----------------------------------#

@login_required
def profile_view(request):
    """
    Edit user profile.
    """
    user = request.user
    context = {
        'active_page': 'profile',
    }

    if request.method == 'GET':
        form = ProfileForm(user, instance=user)
        context.update({'form': form})
    else:
        form = ProfileForm(user, request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil anda telah disimpan.', extra_tags='success')
            return HttpResponseRedirect(reverse('edit_profile'))

        context.update({'form': form})
    return render_to_response('edit-profile.html', context,
                              context_instance=RequestContext(request))

# ------------------------------------Company ----------------------------------#

@login_required
def companies_view(request):
    """
    Companies page.
    """
    user = request.user
    context = {
        'active_page': 'companies',
        'companies': Company.objects.filter(user=user),
    }
    return render_to_response('companies.html', context,
                              context_instance=RequestContext(request))


@login_required
def company_new_view(request):
    """
    Create new company page.
    """
    user = request.user
    context = {
        'active_page': 'companies',
    }

    if request.method == 'GET':
        form = CompanyForm()
    else:
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = user
            company.save()
            messages.success(request, 'Perusahaan telah di simpan.', extra_tags='success')
            return HttpResponseRedirect(reverse('company_edit', args=(company.pk,)))
    context.update({'form': form})
    return render_to_response('companies-edit.html', context,
                              context_instance=RequestContext(request))


@login_required
def company_edit_view(request, company_id):
    """
    Companies edit page.
    """
    user = request.user
    company = get_object_or_404(Company, user=user, pk=company_id)
    context = {
        'active_page': 'companies',
        'company': company,
    }

    if request.method == 'GET':
        form = CompanyForm(instance=company)
    else:
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save(commit=False)
            form.user = user
            form.save()
            messages.success(request, 'Perusahaan baru telah di simpan.', extra_tags='success')
            return HttpResponseRedirect(reverse('company_edit', args=(company_id,)))

    context.update({'form': form})
    return render_to_response('companies-edit.html', context,
                              context_instance=RequestContext(request))


@login_required
def company_delete_view(request, company_id):
    """
    Delete the company.
    """
    user = request.user
    company = get_object_or_404(Company, user=user, pk=company_id)
    company.delete()
    messages.success(request, 'Satu perusahaan telah di dihapus.', extra_tags='success')
    return HttpResponseRedirect(reverse('companies'))


# ------------------------------- Jobs ----------------------------------------#

def jobs_view(request, category_slug):
    """
    List all jobs in category.
    """
    category = get_object_or_404(Category, slug=category_slug)
    context = {
        'title': 'Kategori %s' % category.name,
        'description': category.description,
        'active_page': 'jobs',
        'categories': Category.objects.all(),
        'category': category,
        'premium_jobs': Job.objects.filter(category=category, status='ACTIVE', approved=True, is_premium=True,
                                   ended__gte=now).order_by('-started'),
        'free_jobs': Job.objects.filter(category=category, status='ACTIVE', approved=True, is_premium=False,
                                   ended__gte=now).order_by('-started'),
    }
    return render_to_response('listing-category.html', context,
                              context_instance=RequestContext(request))

@login_required
def job_new_view(request):
    """
    Create new job page.
    """
    user = request.user
    context = {
        'active_page': 'dashboard',
    }

    if request.method == 'GET':
        form = JobForm(user)
    else:
        form = JobForm(user, request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = user
            job.started = now()
            job.ended = job.started + datetime.timedelta(+30)
            job.status = 'PENDING'
            job.approved = False
            job.save()
            messages.success(request, 'Lowongan baru telah disimpan dan sedang dimoderasi admin.', extra_tags='success')
            return HttpResponseRedirect(reverse('job_edit',args=(job.pk,)))

    context.update({'form': form})
    return render_to_response('jobs-edit.html', context,
                              context_instance=RequestContext(request))


@login_required
def job_edit_view(request, job_id):
    """
    Edit job page.
    """
    user = request.user
    job = get_object_or_404(Job, user=user, pk=job_id)
    context = {
        'active_page': 'dashboard',
        'job': job,
    }

    if request.method == 'GET':
        form = JobForm(user, instance=job)
    else:
        form = JobForm(user, request.POST, instance=job)
        if form.is_valid():
            form.save(commit=False)
            form.user = user
            form.save()
            messages.success(request, 'Lowongan telah disimpan.', extra_tags='success')
            return HttpResponseRedirect(reverse('job_edit',
                                                args=(job_id,)) + "?s=success")

    context.update({'form': form})
    return render_to_response('jobs-edit.html', context,
                              context_instance=RequestContext(request))


@login_required
def job_delete_view(request, job_id):
    """
    Delete Job.
    """
    user = request.user
    job = get_object_or_404(Job, user=user, pk=job_id)
    job.delete()
    messages.success(request, 'Satu lowongan telah dihapus.', extra_tags='success')
    return HttpResponseRedirect(reverse('dashboard'))


def job_detail_view(request, job_slug):
    """
    Display single job.
    """
    if request.user.is_authenticated():
        job = get_object_or_404(Job, slug=job_slug)
    else:
        job = get_object_or_404(Job, slug=job_slug, status='ACTIVE', approved=True, ended__gte=now)

    context = {
        'title': 'Lowongan %s' % job.title,
        'description': job.description,
        'job': job,
        'linkedin_api_key': settings.LINKEDIN_API_KEY,
        'status': request.GET.get('apply'),
    }
    form = None

    if request.method == 'GET':
        context.update({'categories': Category.objects.all()})

        if request.GET.get('apply') == 'yes':
            form = JobApplicationForm()
    else:
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            appl = form.save(commit=False)
            appl.job = job
            appl.company = job.company
            appl.save()
            messages.success(request, 'Selamat! Lowongan anda sudah terkirim.', extra_tags='success')
            return HttpResponseRedirect(job.get_absolute_url())

    context.update({'form': form})
    return render_to_response('jobs-single.html', context,
                              context_instance=RequestContext(request))


def job_shortlink_view(request, job_id):
    """
    Job short link handler, redirect to full job url.
    """
    job = get_object_or_404(Job, pk=job_id, status='ACTIVE', ended__gte=now)
    return HttpResponseRedirect(job.get_absolute_url())


@login_required
def job_toggle_view(request, job_id):
    """
    Toggle Job active Status.
    """
    user = request.user
    job = get_object_or_404(Job, user=user, pk=job_id)

    if job.status == 'PENDING':
        raise Http404

    if job.status == 'ACTIVE':
        job.status = 'INACTIVE'
        job.save()
        messages.success(request, 'Lowongan telah di non-aktifkan.', extra_tags='success')
    elif job.status == 'INACTIVE':
        job.status = 'ACTIVE'

        # If jobs currently expired, reset started and ended date.
        if job.ended < now():
            job.started = now()
            job.ended = job.started + datetime.timedelta(+30)
        job.save()
        messages.success(request, 'Lowongan telah di aktifkan.', extra_tags='success')

    return HttpResponseRedirect(job.get_edit_url())


@login_required
def job_cancelpremium_view(request, job_id):
    """
    Cancel premium.
    """
    user = request.user
    job = get_object_or_404(Job, user=user, pk=job_id)

    orders = job.premiumorder_set.filter(status='UNPAID').update(status='CANCELED')
    messages.success(request, 'Aktifasi PREMIUM sudah dibatalkan.', extra_tags='success')
    return HttpResponseRedirect(job.get_edit_url())


@login_required
def job_gopremium_view(request, job_id):
    """
    Go premium.
    """
    user = request.user
    job = get_object_or_404(Job, user=user, pk=job_id)
    if job.has_active_order:
        raise Http404
    else:
        order = PremiumOrder(user=user, job=job, job_title=job.title,
                             status='UNPAID', amount=settings.PREMIUM_FEE,
                             unique_amount=0.00)
        order.save()
        messages.success(request, 'Order aktifasi PREMIUM sudah dibuat. Silahkan cek email anda untuk informasi pembayaran.', extra_tags='success')
        return HttpResponseRedirect(reverse('billing'))

# --------------------------- BILLING -----------------------------------------#

@login_required
def billing_view(request):
    """
    Billings page.
    """
    user = request.user
    context = {
        'active_page': 'billing',
        'orders': PremiumOrder.objects.filter(user=user, status='UNPAID'),
    }
    return render_to_response('billing.html', context,
                              context_instance=RequestContext(request))


@login_required
def payconfirm_view(request):
    """
    Payment confirmation page.
    """
    user = request.user
    context = {
        'active_page': 'pay_confirm',
    }
    if request.method == 'GET':
        context.update({'form': PaymentConfirmationForm(user)})
    else:
        form = PaymentConfirmationForm(user, request.POST)
        if form.is_valid():
            confirm = form.save(commit=False)
            confirm.user = user
            confirm.save()
            messages.success(request, 'Terima Kasih! Konfirmasi pembayaran anda telah terkirim dan akan kami verifikasi.', extra_tags='success')
            return HttpResponseRedirect(reverse('pay_confirm'))
        context.update({'form': form})

    return render_to_response('payment-confirmation.html', context,
                              context_instance=RequestContext(request))

@login_required
def payment_valid_view(request, order_id):
    """
    Set payment to valid.
    """
    user = request.user
    order = get_object_or_404(PremiumOrder, pk=order_id)
    # This is can only be done by superuser
    if user.is_superuser:
        order.status = 'PAID'
        order.save()
        return HttpResponseRedirect(reverse('admin:hub_job_change', args=[order.job.pk]))
        
    raise Http404


@login_required
def activate_free_view(request, job_id):
    """
    Activate Free for Job and send email.
    """
    user = request.user
    job = get_object_or_404(Job, pk=job_id)
    # This is can only be done by superuser
    if user.is_superuser:
        job.status = 'ACTIVE'
        job.approved = True
        job.started = now()
        job.ended = job.started + datetime.timedelta(+30)
        job.save()

        tweet_job(job)
        send_free_activation_email(job)
        
        return HttpResponseRedirect(reverse('admin:hub_job_change', args=[job.pk]))
    raise Http404


@login_required
def activate_premium_view(request, job_id):
    """
    Activate premium for Job and send email.
    """
    user = request.user
    job = get_object_or_404(Job, pk=job_id)
    # This is can only be done by superuser
    if user.is_superuser:
        job.is_premium = True
        job.approved = True
        job.status = 'ACTIVE'
        job.started = now()
        job.ended = job.started + datetime.timedelta(+30)
        job.save()
        
        send_premium_activation_email(job)
        return HttpResponseRedirect(reverse('admin:hub_job_change', args=[job.pk]))
    raise Http404

# ---------------------------------- INDEED -----------------------------------#

@login_required
def indeed_cron_links(request):
    """
    Simple print cron links on the browser.
    """
    links = []
    categories = Category.objects.all()
    for cat in categories:
        links.append(settings.SITE_DOMAIN + cat.get_cron_url()+'?key='+settings.CRONJOB_KEY)
    return HttpResponse(u'<br>'.join(links))


def fetch_indeed(url, cat):
    """
    Fetch jobs from Indeed.
    """
    jobs = []
    fine_json = None

    try:
        f = urllib2.urlopen(url)
    except Exception as e:
        print e
        return HttpResponse('Error opening source URL.')
    else:
        raw_json = f.read()
        try:
            fine_json = json.loads(raw_json)
        except Exception as e:
            print e
            return HttpResponse('Error parsing JSON.')

    if fine_json:
        for job in fine_json.get('results'):
            j = IndeedJob(
                    category=cat,
                    title=job.get('jobtitle'),
                    company=job.get('company'),
                    location=job.get('formattedLocation'),
                    description=job.get('snippet'),
                    jobkey=job.get('jobkey'),
                    url=job.get('url'),
                    onmousedown=job.get('onmousedown'),
                    created=convert_gtm_to_utc(job.get('date'))
                )
            jobs.append(j)
    return jobs


def indeed_cron_view(request, category_id):
    """
    Update indeed jobs.
    """
    if(request.GET.get('key') != settings.CRONJOB_KEY):
        return HttpResponse('Invalid key.')

    cat = get_object_or_404(Category, pk=category_id)
    query = cat.indeed_query
    url1 = settings.INDEED_API_URL % (settings.INDEED_PUBLISHER_ID,
                                     quote(query), 0, settings.SERVER_IP)
    print url1
    url2 = settings.INDEED_API_URL % (settings.INDEED_PUBLISHER_ID,
                                     quote(query), 25, settings.SERVER_IP)

    try:
        jobs_1 = fetch_indeed(url1, cat)
        jobs_2 = fetch_indeed(url2, cat)
        new_jobs = jobs_1 + jobs_2
    except Exception as e:
        print e
    else:
        current_jobs = IndeedJob.objects.filter(category=cat)
        current_jobs.delete()
        try:
            IndeedJob.objects.bulk_create(new_jobs)
        except Exception as e:
            print e
    return HttpResponse('finished')


def indeed_jobs(request, category_id):
    """
    Load Indeed jobs via ajax.
    """
    if request.is_ajax() and request.method == 'POST':

        per_page = 10
        page = 1
        html = []

        if category_id == '0':
            all_jobs = IndeedJob.objects.all()
        else:
            all_jobs = IndeedJob.objects.filter(category=category_id)

        paginator = Paginator(all_jobs, per_page)
        page = request.GET.get('page')
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)

        for job in jobs:
            html.append(render_to_string('indeed-job.html', {'job': job}))
        context = {
            'html': u''.join(html),
            'page': jobs.number,
            'next_page': jobs.next_page_number(),
        }

        return HttpResponse(json.dumps(context), content_type='application/json')
    raise Http404


# -------------------------------------- PAGES --------------------------------#


def page_about(request):
    """
    About page.
    """
    context={
        'title': 'Tentang LokerHub',
        'description': 'LokerHub merupakan situs penyedia informasi karir di bidang Teknologi Informasi. Berusaha memberi kesan baru dan segar buat situs lowongan kerja di Indonesia.',
    }
    return render_to_response('pages/about.html', context, context_instance=RequestContext(request))


def page_faq(request):
    """
    Faq page.
    """
    context={
        'title': 'LokerHub F.A.Q',
        'description': 'Daftar pertanyaan dan jawaban yang paling sering di tanyakan oleh user kami.',
    }
    return render_to_response('pages/faq.html', context, context_instance=RequestContext(request))


def page_contact(request):
    """
    Contact page.
    """
    context={
        'title': 'Hubungi Kami',
        'description': 'Apabila anda ada kendala dengan penggunaan sitem kami, ada pertanyaan, saran, kritik kami akan dengan senang hati mendengarnya dari anda.',
    }
    return render_to_response('pages/contact.html', context, context_instance=RequestContext(request))


def robots_txt(request):
    """
    Robots.txt
    """
    return render_to_response('robots.txt', content_type='text/plain')