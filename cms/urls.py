from django.urls import path
from cms import views

app_name = 'cms'
urlpatterns = [
    # Live
    path('live/', views.live_list, name='live_list'),   # 一覧
    path('live/add/', views.live_edit, name='live_add'),  # 登録
    path('live/mod/<int:live.id>', views.live_edit, name='live_mod'),  # 修正
    path('live/del/<int:live.id>', views.live_del, name='live_del'),   # 削除
]