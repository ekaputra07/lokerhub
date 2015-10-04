import random
import datetime
from urllib import quote
import urllib2
import json
import requests
from requests.auth import HTTPBasicAuth

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, get_object_or_404, render
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

from hub.models import OneallToken, Company, Category, Job, IndeedJob, PremiumOrder
from hub.forms import CompanyForm, TransferCompanyForm, JobForm, JobApplicationForm, PaymentConfirmationForm, ProfileForm, EmailForm
from hub.utils import convert_gtm_to_utc, send_premium_activation_email, send_free_activation_email, tweet_job


def home_view(request):
    """
    Homepage view.
    """
    page = request.GET.get('page')

    # -------------- Indeed Pagination ----------------------------------------#
    indeed_list = IndeedJob.objects.all()
    indeed_paginator = Paginator(indeed_list, 20)
    try:
        indeed_jobs = indeed_paginator.page(page)
    except PageNotAnInteger:
        indeed_jobs = indeed_paginator.page(1)
    except EmptyPage:
        indeed_jobs = indeed_paginator.page(indeed_paginator.num_pages)

    # -------------- LokerHub jobs Pagination ----------------------------------------#
    job_list = Job.objects.filter(status='ACTIVE', approved=True, ended__gte=now).order_by('ads_type', '-started')
    jobs_paginator = Paginator(job_list, 20)
    try:
        jobs = jobs_paginator.page(page)
    except PageNotAnInteger:
        jobs = jobs_paginator.page(1)
    except EmptyPage:
        jobs = []

    context = {
        'title': 'Lowongan kerja IT Indonesia',
        'description': 'LokerHub adalah situs penyedia informasi karir di bidang Teknologi Informasi.',
        'categories': Category.objects.all(),
        'jobs': jobs,
        'indeed_jobs': indeed_jobs,
    }
    return render_to_response('listing.html', context,
                              context_instance=RequestContext(request))


def login_view(request):
    """
    Login page.
    """
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    raise Http404


@csrf_exempt
def logincallback_view(request):
    """
    LoginRadius social login callback.
    """
    if request.method == 'POST':
        oa_token = request.POST.get('connection_token', '')

        url = 'https://%s.api.oneall.com/connections/%s.json' % (settings.ONEALL_SUBDOMAIN, oa_token)
        resp = requests.get(url, auth=HTTPBasicAuth(settings.ONEALL_API_KEY, settings.ONEALL_API_SECRET))
        json_resp = resp.json()

        data = json_resp['response']['result']['data']
        key = data['plugin']['key']
        status = data['plugin']['data']['status']

        # Handle social login.
        if key and (key == 'social_login' or key == 'single_sign_on') and status == 'success':
            user_token = data['user']['user_token']
            displayName = data['user']['identity']['displayName']

            email = None
            try:
                email = data['user']['identity']['emails'][0]['value']
            except:
                pass

            user = authenticate(oneall_token=user_token)

            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                username = 'user%s' % random.randint(1000, 90000)

                # generate temp email if no email returned.
                if not email:
                    email = '%s+generated@lokerhub.com' % username

                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    # User with this email doesn't exist.
                    # Create new user and login
                    user = User(
                        username = username,
                        email = email,
                        first_name = displayName
                    )
                    user.is_active = True
                    user.save()

                    token = OneallToken(user=user, token=user_token)
                    token.save()

                    # Authenticate once again and login.
                    u = authenticate(oneall_token=user_token)
                    login(request, u)
                    return HttpResponseRedirect(reverse('dashboard'))
                else:
                    messages.error(request, 'Email sudah terdaftar dengan akun lain.', extra_tags='danger')
                    return HttpResponseRedirect(reverse('login'))

            messages.error(request, 'Login / Register gagal.', extra_tags='danger')
            return HttpResponseRedirect(reverse('login'))

        # Social link
        if key and (key == 'social_link') and status == 'success':
            link_action = data['plugin']['data']['action']

            # link account
            if link_action == 'link_identity':
                user_token = data['user']['user_token']
                provider = data['user']['identity']['source']['name']
                try:
                    oneall = request.user.oneall
                    oneall.token = user_token
                    oneall.save()
                except:
                    oneall = OneallToken(user=request.user, token=user_token)
                    oneall.save()

                messages.success(request, "Akun anda sudah tersambung dengan %s." % provider, extra_tags='success')
                return HttpResponseRedirect(reverse('edit_profile'))

            # unlink account
            if link_action == 'unlink_identity':
                messages.success(request, "Social login berhasil diupdate.", extra_tags='success')
                return HttpResponseRedirect(reverse('edit_profile'))

    return Http404


@login_required
def finish_signup_view(request):
    """
    Finish signup page.
    """
    user = request.user
    if request.method == 'GET':
        form = EmailForm(user)
    else:
        form = EmailForm(user, request.POST)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.save()

            messages.success(request, 'Email anda telah disimpan.', extra_tags='success')
            return HttpResponseRedirect(reverse('dashboard'))

    return render(request, 'finish-signup.html', {'form': form})


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
        'transfer_form': TransferCompanyForm(instance=company)
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


@login_required
def company_transfer_view(request, company_id):
    """
    Transfer company owner.
    """
    user = request.user
    company = get_object_or_404(Company, user=user, pk=company_id)
    form  = TransferCompanyForm(request.POST, instance=company)
    if form.is_valid():
        c = form.save(commit=False)

        # To make sure transfer can only be done by superuser.
        if not user.is_superuser:
            c.user = user
        else:
            # Transfer all jobs under the company to the new owner.
            Job.objects.filter(company=company).update(user=form.cleaned_data['user'])
        c.save()
        messages.success(request, 'Perusahaan berhasil ditransfer.', extra_tags='success')
    else:
        messages.error(request, 'Perusahaan gagal ditransfer.', extra_tags='warning')
    return HttpResponseRedirect(reverse('dashboard'))

# ------------------------------- Jobs ----------------------------------------#

def jobs_view(request, category_slug):
    """
    List all jobs in category.
    """
    category = get_object_or_404(Category, slug=category_slug)

    page = request.GET.get('page')

    # -------------- Indeed Pagination ----------------------------------------#
    indeed_list = IndeedJob.objects.filter(category=category)
    indeed_paginator = Paginator(indeed_list, 20)
    try:
        indeed_jobs = indeed_paginator.page(page)
    except PageNotAnInteger:
        indeed_jobs = indeed_paginator.page(1)
    except EmptyPage:
        indeed_jobs = indeed_paginator.page(indeed_paginator.num_pages)

    # -------------- LokerHub jobs Pagination ----------------------------------------#
    job_list = Job.objects.filter(category=category, status='ACTIVE', approved=True, ended__gte=now).order_by('ads_type', '-started')
    jobs_paginator = Paginator(job_list, 20)
    try:
        jobs = jobs_paginator.page(page)
    except PageNotAnInteger:
        jobs = jobs_paginator.page(1)
    except EmptyPage:
        jobs = []

    context = {
        'title': 'Kategori %s' % category.name,
        'description': category.description,
        'active_page': 'jobs',
        'categories': Category.objects.all(),
        'category': category,
        'jobs': jobs,
        'indeed_jobs': indeed_jobs,
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
        'job': job
    }

    if request.method == 'GET':
        form = JobForm(user, instance=job)
    else:
        form = JobForm(user, request.POST, instance=job)
        if form.is_valid():
            form.save(commit=False)
            form.user = user
            job = form.save()
            job.approved = True
            job.save()
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
        'company_jobs': Job.objects.filter(company=job.company, status='ACTIVE', approved=True, ended__gte=now).exclude(id=job.id),
        'linkedin_api_key': settings.LINKEDIN_API_KEY,
        'status': request.GET.get('apply'),
    }

    if request.method == 'GET':
        context.update({'categories': Category.objects.all()})

        if job.company.logo:
            context.update({'page_img': settings.SITE_DOMAIN + job.company.logo.url})

        if request.GET.get('apply') == 'yes':
            form = JobApplicationForm()
            context.update({'form': form})


        # Get related jobs.
        related_num = 8
        related_jobs = job_list = Job.objects.filter(category=job.category,
                                                     status='ACTIVE',
                                                     approved=True,
                                                     ended__gte=now).exclude(id=job.id).order_by('ads_type', '-started')[:related_num]
        related_jobs_num = related_jobs.count()
        context['related_jobs'] = related_jobs

        if related_jobs_num < related_num:
            job_left = related_num - related_jobs_num
            indeed_jobs = IndeedJob.objects.filter(category=job.category)[:job_left]
            context['indeed_related_jobs'] = indeed_jobs
    else:
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            appl = form.save(commit=False)
            appl.job = job
            appl.company = job.company
            appl.save()
            messages.success(request, 'Selamat! Lowongan anda sudah terkirim.', extra_tags='success')
            return HttpResponseRedirect(job.get_absolute_url())
        else:
            context['form'] = form

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
        job.ads_type = 0
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
        url = settings.SITE_DOMAIN + cat.get_cron_url()+'?key='+settings.CRONJOB_KEY
        links.append('%s - <a href="%s" target="_blank">%s</a>' % (cat.name, url, url))
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
        return HttpResponse('Error opening source URL.')
    else:
        raw_json = f.read()
        try:
            fine_json = json.loads(raw_json)
        except Exception as e:
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
        }
        if jobs.has_next(): context.update({'next_page': jobs.next_page_number()})

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


def page_fb_promo(request):
    """
    fb promo page.
    """
    context={
        'title': 'Promosi via iklan Facebook',
        'description': 'Upgrade iklan ke Premium dan kami akan mengalokasikan Rp. 50,000,- untuk mengiklankan lowongan anda ke Facebook.',
    }
    return render_to_response('pages/fb-promo.html', context, context_instance=RequestContext(request))


def robots_txt(request):
    """
    Robots.txt
    """
    return render_to_response('robots.txt', content_type='text/plain')
