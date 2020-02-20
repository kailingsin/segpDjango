from django.shortcuts import render

posts = [
    {
        'author': 'Dummy data',
        'title': 'Tomato Predicted price',
        'content': 'Display some graph',
        'date_posted': 'Feburary 18, 2020'
    },
    {
      'author': 'Dummy data',
        'title': 'Chicken Predicted price',
        'content': 'Display some graph',
        'date_posted': 'Feburary 18, 2020'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def dashboard(request):
    return render(request, 'blog/dashboard.html')