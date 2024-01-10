from django.shortcuts import render, redirect
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator

def board(request):
    articles = Article.objects.all().order_by('-id')
    page = int(request.GET.get('page', 1))
    paginator=Paginator(articles, 10)
    pages = paginator.get_page(page)
    content = {'articles': pages}
    return render(request, "forum/index.html", content)

def search(request):
    question=request.GET.get('q', '')
    articles = Article.objects.order_by('-id')
    content={}
    if not question:
        search_article_list = articles
    else :
        if len(question) > 1 :
            search_article_list = articles.filter(Q (title__icontains=question) | Q (content__icontains=question)) #  | Q (user_id__icontains=question)
            
    page = int(request.GET.get('page', 1))
    paginator=Paginator(search_article_list, 10)
    pages = paginator.get_page(page)
    content = {'articles': pages}
    return render(request, 'forum/board.html', content)

def mypost(request):
    articles = Article.objects.order_by('-id')
    search_article_list = articles.filter(Q (user_id=request.user.id))
    page = int(request.GET.get('page', 1))
    paginator=Paginator(search_article_list, 10)
    pages = paginator.get_page(page)
    content = {'articles': pages}
    return render(request, "forum/board.html", content)


    # articles = Article.objects.all()
    # content = {'articles': articles}
    # print(request.user.id)
    # return render(request, 'forum/board.html', content)

def notice(request):
    return render(request, 'forum/notice.html')

def index(request):
    articles = Article.objects.all().order_by('-id')
    page = int(request.GET.get('page', 1))
    paginator=Paginator(articles, 10)
    pages = paginator.get_page(page)
    content = {'articles': pages}
    return render(request, "forum/index.html", content)


def create(request):
    if request.method == "POST" :
        form = ArticleForm(request.POST)
        if form.is_valid(): #유효성 검사
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('forum:index', pk = article.pk)
    else:
        form = ArticleForm()
    content = {'form':form}
    return render(request, 'forum/create.html', content)
    
def read(request, pk):
    article = get_object_or_404(Article, pk=pk)  # 좀 더 나은 에러 처리를 위해 get_object_or_404 사용

    # 조회수 증가
    if request.method == 'GET':  # 조회수가 GET 요청에만 증가하도록 함
        article.views += 1  # 조회수 증가
        article.save()  # 조회수가 증가된 게시글을 저장
        
        
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user == article.user:
                article.delete()
                return redirect('forum:index')
        return redirect('forum:index')
    else :
        commentform = CommentForm()
        comment = article.comment_set.all()
        content = {'article': article, 'commentform' : commentform, 'comment': comment,}
        return render(request, 'forum/read.html', content)

def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                form.save()
                return redirect('forum:read', pk=article.pk)
        else:
            form = ArticleForm(instance=article)
        content = {'form':form, 'article': article, }
        return render(request, 'forum/update.html', content)
    else :
        return redirect('forum:index')

def comment_create(request,pk):
    if request.user.is_authenticated:
        article = Article.objects.get(pk=pk)  # Article 객체를 가져옵니다.
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            comment = commentform.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()

            # 답변 여부를 업데이트합니다. 여기서 request.user가 관리자인지 확인해야 합니다.
            # 예를 들어, 관리자 여부를 확인하는 is_admin 필드가 있다고 가정하면:
            if request.user.is_superuser:
                article.is_answered = True
                article.save()

        return redirect('forum:read', article.pk)
    else :
        return redirect('accounts:login')

    
def comment_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = Comment.objects.get(pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
        return redirect('forum:read', article_pk)
    else :
        return redirect('accounts:login')
