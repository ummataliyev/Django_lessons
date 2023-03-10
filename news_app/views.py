from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from hitcount.views import HitCountMixin
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from hitcount.utils import get_hitcount_model
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .models import News
from .models import Category
from .forms import CommentForm
from .forms import ContactForm
from new_project.custom_permissions import OnlyLoggedSuperUser


# Create your views here.
def news_list(request):
    # news_list = News.objects.filter(status=News.Status.Published)
    news_list = News.published.all()
    context = {
        "news": news_list
    }

    return render(request, "news/news_detail.html", context=context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)    # get the news object with the specified slug and status # noqa
    context = {}
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    new_comment = None # get the comments associated with the news object # noqa

    if request.method == "POST":
        # if the request method is POST, create a new comment
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            try:
                new_comment = comment_form.save(commit=False)
                new_comment.news = news
                new_comment.user = request.user
                new_comment.save()
                comment_form = CommentForm()
            except Exception as e:
                print(e) # log any errors that occur while creating the new comment # noqa
    else:
        comment_form = CommentForm()

    # create a dictionary of context variables to pass to the template
    context = {
        "news": news,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    }

    # render the news detail template with the context variables
    return render(request, "news/news_detail.html", context)


@login_required
def homePageView(request):
    categories = Category.objects.all()
    news_list = News.published.all().order_by('-publish_time')[:15]
    economics_one = News.published.filter(category__name="Economics").order_by("-publish_time")[:1] # noqa
    economics_news = News.published.all().filter(category__name="Economics")[1:6] # noqa
    context = {
        'news_list': news_list,
        "categories": categories,
        "economics_one": economics_one,
        "economics_news": economics_news
    }

    return render(request, 'news/home.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:5] # noqa
        context["economics_news"] = News.published.all().filter(category__name="Economics").order_by("-publish_time")[:5] # noqa
        context["world_news"] = News.published.all().filter(category__name="World").order_by("-publish_time")[:5] # noqa
        context["tech_news"] = News.published.all().filter(category__name="Technology").order_by("-publish_time")[:5] # noqa
        context["sport_news"] = News.published.all().filter(category__name="Sport").order_by("-publish_time")[:5] # noqa

        return context


class EconomicNewsView(ListView):
    model = News
    template_name = 'news/economic.html'
    context_object_name = 'economics_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Economics")
        return news


class WorldNewsView(ListView):
    model = News
    template_name = 'news/world.html'
    context_object_name = 'world_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="World")

        return news


class TechNewsView(ListView):
    model = News
    template_name = 'news/tech.html'
    context_object_name = 'tech_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Technology")

        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Sport")

        return news


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
            }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("<h2>Thank you for contacting us!</h2>")
        context = {
            'form': form
            }
        return render(request, self.template_name, context)


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status', )
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')
    success_message = 'The news has been deleted successfully.'


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = "crud/news_create.html"
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)


class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'all_news'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
