from django.urls import path


from . import views


urlpatterns = [
    # path('user/', views.UserGet.as_view(), name='user'),
    path('tags/', views.TagListView.as_view(), name='tag-list'),
    path('tag/<int:pk>', views.TagDetailView.as_view(), name='tag-detail'),
    path('tag/create/', views.TagCreateView.as_view(), name='tag-create'),
    path('tasks/', views.TasksListView.as_view(), name='task-list'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/create/', views.TaskCreateView.as_view(), name='task-create'),
]

