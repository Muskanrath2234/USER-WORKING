from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.generic import  DetailView, UpdateView, DeleteView,ListView
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from datetime import datetime



class PostListView(ListView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'




class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'



class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm  # Use the customized form
    template_name = 'create_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to the database
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post')  # Redirect to the user's profile page
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


from django.shortcuts import render
from django.contrib.auth.models import User

def author_profile(request, username):
    # Get the user object based on username
    user = User.objects.get(username=username)
    # Get all posts by this user
    posts = user.post_set.all()
    # Render the author profile template with user and posts
    return render(request, 'author_profile.html', {'user': user, 'posts': posts})



def posts_by_date(request, year, month, day):
    # Convert year, month, day to datetime object
    date_obj = datetime(year, month, day)

    # Filter posts for the given date
    posts = Post.objects.filter(date_posted__year=year, date_posted__month=month, date_posted__day=day)

    # Render template with posts and date
    return render(request, 'datewisepost.html', {'date': date_obj, 'posts': posts})