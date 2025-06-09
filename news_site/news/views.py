from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Article, Category, Comment
from .forms import ArticleForm

def home(request):
    """Home page showing latest articles"""
    articles = Article.objects.filter(status='published').select_related('author', 'category')
    categories = Category.objects.all()

    # Featured article (most recent)
    featured_article = articles.first()

    # Latest articles (excluding featured)
    latest_articles = articles[1:9]  # Get next 8 articles

    # Popular articles (by views)
    popular_articles = articles.order_by('-views')[:5]

    context = {
        'featured_article': featured_article,
        'latest_articles': latest_articles,
        'popular_articles': popular_articles,
        'categories': categories,
    }
    return render(request, 'news/home.html', context)

def article_detail(request, slug):
    """Display individual article"""
    article = get_object_or_404(Article, slug=slug, status='published')

    # Increment view count
    article.increment_views()

    # Get related articles from same category
    related_articles = Article.objects.filter(
        category=article.category,
        status='published'
    ).exclude(id=article.id)[:4]

    # Get comments
    comments = article.comments.filter(active=True)

    context = {
        'article': article,
        'related_articles': related_articles,
        'comments': comments,
    }
    return render(request, 'news/article_detail.html', context)

def category_view(request, category_id):
    """Display articles by category"""
    category = get_object_or_404(Category, id=category_id)
    articles = Article.objects.filter(
        category=category,
        status='published'
    ).select_related('author')

    # Pagination
    paginator = Paginator(articles, 6)  # 6 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'articles': page_obj,
        'categories': Category.objects.all(),
    }
    return render(request, 'news/category.html', context)

def search(request):
    """Search articles"""
    query = request.GET.get('q', '')
    articles = []

    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status='published'
        ).select_related('author', 'category')

    context = {
        'articles': articles,
        'query': query,
        'categories': Category.objects.all(),
    }
    return render(request, 'news/search_results.html', context)

# NEW: article create view (for image upload)
def article_create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            return redirect(article.get_absolute_url())
    else:
        form = ArticleForm()
    return render(request, 'news/article_form.html', {'form': form})