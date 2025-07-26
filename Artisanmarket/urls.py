from django.urls import re_path ,path
from .import views 
urlpatterns = [ 
re_path(r'^$', views.login,name='login'), 

re_path(r'^home', views.home,name='home'), 
re_path(r'^DBLogin/$', views.DBLogin,name='DBLogin'), 
re_path(r'^logout/$', views.logout,name='logout'), 
re_path(r'^register/$', views.register,name='register'),
re_path(r'^registration/$', views.registration,name='registration'),
# re_path(r'add_product/', views.add_product, name='add_product'),
# re_path(r'product_list/', views.product_list, name='product_list'),
re_path(r'^productupload/$', views.productupload, name='productupload'), 
re_path(r'^viewproductupload/$', views.viewproductupload, name='viewproductupload'),  
re_path(r'delFile/(\d+)$',views.delFile,name='delFile'),
re_path(r'edit/(\d+)$',views.edit,name='edit'),
re_path(r'updateStd/(\d+)$',views.updateStd,name='updateStd'),

re_path(r'^cakes_page/$', views.cakes_page, name='cakes_page'), 
re_path(r'^crafts_page/$', views.crafts_page, name='crafts_page'), 
re_path(r'^mehandi_page/$', views.mehandi_page, name='mehandi_page'), 


re_path(r'^deals/$', views.deals, name='deals'), 
path('place_order/<int:product_id>/', views.place_order, name='place_order'),
path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
path('my_orders/', views.my_orders, name='my_orders'),
path('received_orders/', views.received_orders, name='received_orders'),

path('forgot-password/', views.forgot_password, name='forgot_password'),
path('verify-otp/', views.verify_otp, name='verify_otp'),
path('reset-password/', views.reset_password, name='reset_password'),

re_path(r'^ProfileEdit/$',views.ProfileEdit,name='ProfileEdit'),
re_path(r'^ProfileUpdate/$',views.ProfileUpdate,name='ProfileUpdate'),
path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
path('wishlist/', views.view_wishlist, name='view_wishlist'),
path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
re_path(r'^adLogin/$', views.adLogin,name='adLogin'), 
re_path(r'^page/$', views.page,name='page'), 
path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
re_path(r'^logout/$', views.logout,name='logout'), 
re_path(r'^userlogout/$', views.userlogout,name='userlogout'), 
path('prooduct_list/', views.product_list, name='product_list'),

 path('add_feedback/', views.add_feedback, name='add_feedback'),
    path('view_feedbacks/', views.view_feedbacks, name='view_feedbacks'),
    path('edit-feedback/<int:feedback_id>/', views.edit_feedback, name='edit_feedback'),
 path('add_feedbacks/', views.add_feedbacks, name='add_feedbacks'),
 path('viewallfeed/', views.viewallfeed, name='viewallfeed'),
 path('delete_feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),





    

]
