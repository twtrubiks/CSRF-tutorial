from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommentForm
from .models import Comment


@login_required(login_url='/admin/')
def index(request):
    comments_list = Comment.objects.order_by('-created')
    return render(request,
                  'Comments/index.html', {
                      'comments': comments_list
                  })


@login_required(login_url='/admin/')
def comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = CommentForm()

    return render(request,
                  'Comments/comment.html', {
                      'form': form
                  })


@login_required(login_url='/admin/')
def delete_comment(request):
    if request.method == 'POST':
        comment_id = request.POST['id']
        comment_data = get_object_or_404(Comment, id=comment_id)
        comment_data.delete()
    return redirect('index')
