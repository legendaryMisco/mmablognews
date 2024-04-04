from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import ListView, DetailView
from mmablog.models.BlogPostModel import BlogPost
from mmablog.models.BlogViewCount import BlogViewCount
from mmablog.models.BlogCommentModel import BlogComment
from mmablog.models.BlogCategoryModel import BlogCategory
from mmablog.models.BlogCommentModel import BlogComment
from mmablog.models.BlogContactUsModel import BlogContact
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from itertools import chain
from ipware import get_client_ip
import requests
from django.urls import reverse

class HomeView(ListView):
    queryset = BlogPost.objects.order_by('-posted_date')[:13]
    template_name = 'index.html'
    context_object_name = 'blogposts'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        current_date = timezone.now()

        start_date_trending = current_date - timedelta(days=7) 
        start_date_popular = current_date - timedelta(days=30) 

        context['trending_blogs']  = BlogPost.objects.filter(
                posted_date__range=[start_date_trending, current_date]
            ).annotate(
                view_count=Count('blogviewcount'),
                comment_count=Count('blogcomment')
            ).order_by('-view_count', '-comment_count', '-posted_date')[:5]
  
        mixed_queryset = list(set(chain(context['blogposts'], context['trending_blogs'])))
        mixed_queryset.sort(key=lambda x: x.posted_date, reverse=True)
        context['slider_blogs'] =  mixed_queryset[:3]
        context['aside_blogs'] =  mixed_queryset[4:8]
        context['blog_category'] = BlogCategory.objects.all()
        
        
        context['popular_blogs']  = BlogPost.objects.filter(
                posted_date__range=[start_date_popular, current_date]
            ).annotate(
                view_count=Count('blogviewcount'),
                comment_count=Count('blogcomment')
            ).order_by('-view_count', '-comment_count', '-posted_date')[:3]
            
        context['popular_blog_category']  = BlogCategory.objects.annotate(
                view_count=Count('blogpost__blogviewcount'),
                comment_count=Count('blogpost__blogcomment')
            ).order_by('-view_count', '-comment_count')
        
        context['page_name'] = 'home'

        return context
    

class ArticleView(DetailView):
    model = BlogPost
    template_name = 'single.html'
    context_object_name = 'blog'
    
    
    
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        blog_post = self.get_object()
        client_ip, is_routable = get_client_ip(request)
        url = f"http://ip-api.com/json/{client_ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query" 
        ip_response = requests.get(url)
        user_geo = ip_response.json()
        user_info = user_geo if user_geo else ''
        view_count_obj = BlogViewCount.objects.create(blogheadline=blog_post, ip_information=user_info)
        view_count_obj.save()
        return response
    
    def post(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        blog_post = self.get_object()
        name = request.POST['name']
        email = request.POST['email']
        website = request.POST['website']
        message = request.POST['message']
        client_ip, is_routable = get_client_ip(request)
        url = f"http://ip-api.com/json/{client_ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query" 
        response = requests.get(url)
        user_geo = response.json()
        user_info = user_geo if user_geo else ''
        
        user_comment = BlogComment.objects.create(blogheadline=blog_post, name=name, email=email, website=website, message=message, ip_information=user_info)
        user_comment.save()
        return redirect(reverse('mmablog:article',args=[self.kwargs['slug'],]))
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        current_date = timezone.now()
        
        latest_blog = BlogPost.objects.order_by('-posted_date')
        start_date_trending = current_date - timedelta(days=7) 
        start_date_popular = current_date - timedelta(days=30) 

        context['trending_blogs']  = BlogPost.objects.filter(
                posted_date__range=[start_date_trending, current_date]
            ).annotate(
                view_count=Count('blogviewcount'),
                comment_count=Count('blogcomment')
            ).order_by('-view_count', '-comment_count', '-posted_date')[:5]
  
        mixed_queryset = list(set(chain(latest_blog, context['trending_blogs'])))
        mixed_queryset.sort(key=lambda x: x.posted_date, reverse=True)
        context['slider_blogs'] =  mixed_queryset[:3]
        context['aside_blogs'] =  mixed_queryset[4:8]
        context['blog_category'] = BlogCategory.objects.all()
        
        
        context['popular_blogs']  = BlogPost.objects.filter(
                posted_date__range=[start_date_popular, current_date]
            ).annotate(
                view_count=Count('blogviewcount'),
                comment_count=Count('blogcomment')
            ).order_by('-view_count', '-comment_count', '-posted_date')[:3]
            
        context['popular_blog_category']  = BlogCategory.objects.annotate(
                view_count=Count('blogpost__blogviewcount'),
                comment_count=Count('blogpost__blogcomment')
            ).order_by('-view_count', '-comment_count')
        context['latest_blogs'] = latest_blog[:5]
        context['page_name'] = 'article'

        return context


      
class BlogView(View):
    template_name = 'category.html'
    
    def get(self, request, *args, **kwargs):
        current_date = timezone.now()

        start_date_trending = current_date - timedelta(days=7) 
        start_date_popular = current_date - timedelta(days=30) 

        
        context = {'blogposts': BlogPost.objects.filter(category__name=self.kwargs['category']), 'category': self.kwargs['category']}
        context['trending_blogs']  = BlogPost.objects.filter(
                posted_date__range=[start_date_trending, current_date]
            ).annotate(
                view_count=Count('blogviewcount'),
                comment_count=Count('blogcomment')
            ).order_by('-view_count', '-comment_count', '-posted_date')[:5]
        latest_blog = BlogPost.objects.all()
        mixed_queryset = list(set(chain(latest_blog, context['trending_blogs'])))
        mixed_queryset.sort(key=lambda x: x.posted_date, reverse=True)
        context['slider_blogs'] =  mixed_queryset[:3]
        context['aside_blogs'] =  mixed_queryset[4:8]
        context['blog_category'] = BlogCategory.objects.all()
        
        
        context['popular_blogs']  = BlogPost.objects.filter(
                posted_date__range=[start_date_popular, current_date]
            ).annotate(
                view_count=Count('blogviewcount'),
                comment_count=Count('blogcomment')
            ).order_by('-view_count', '-comment_count', '-posted_date')[:3]
            
        context['popular_blog_category']  = BlogCategory.objects.annotate(
                view_count=Count('blogpost__blogviewcount'),
                comment_count=Count('blogpost__blogcomment')
            ).order_by('-view_count', '-comment_count')
        
        context['page_name'] = self.kwargs['category']

        
        return render(request, self.template_name, context)
    
    

class ContactUsView(View):
    
    template_name = 'contact.html'
    
    def get(self, request):
        
        current_date = timezone.now()

        start_date_trending = current_date - timedelta(days=7) 
        start_date_popular = current_date - timedelta(days=30) 
        context = {}
        context['trending_blogs']  = BlogPost.objects.filter(
                posted_date__range=[start_date_trending, current_date]
            ).annotate(
                view_count=Count('blogviewcount'),
                comment_count=Count('blogcomment')
            ).order_by('-view_count', '-comment_count', '-posted_date')[:5]
        latest_blog = BlogPost.objects.all()
        mixed_queryset = list(set(chain(latest_blog, context['trending_blogs'])))
        mixed_queryset.sort(key=lambda x: x.posted_date, reverse=True)
        context['slider_blogs'] =  mixed_queryset[:3]
        context['aside_blogs'] =  mixed_queryset[4:8]
        context['blog_category'] = BlogCategory.objects.all()
        
        
        context['popular_blogs']  = BlogPost.objects.filter(
                posted_date__range=[start_date_popular, current_date]
            ).annotate(
                view_count=Count('blogviewcount'),
                comment_count=Count('blogcomment')
            ).order_by('-view_count', '-comment_count', '-posted_date')[:3]
            
        context['popular_blog_category']  = BlogCategory.objects.annotate(
                view_count=Count('blogpost__blogviewcount'),
                comment_count=Count('blogpost__blogcomment')
            ).order_by('-view_count', '-comment_count')
        
        context['page_name'] = 'contact'

        
        return render(request, self.template_name, context)
    
    def post(self, request, *args , **kwargs):
        name = request.POST['name']
        email=  request.POST['email']
        subject =  request.POST['subject']
        message =  request.POST['message']
        client_ip, is_routable = get_client_ip(request)
        url = f"http://ip-api.com/json/{client_ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query" 
        response = requests.get(url)
        user_geo = response.json()
        user_info = user_geo if user_geo else ''
        
        
        comment = BlogContact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
            ip_information=user_info
        )
        comment.save()
        return redirect('/contact/')
    
    