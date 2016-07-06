from django.conf.urls import url

#from PyCApp.views import HomePageView
from . import views



urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^Sign-up/', views.sign_up, name='sign_up'),
    url(r'^activate/(?P<activation_key>.+)', views.activation, name='activation'),
    url(r'^Verification/', views.verify, name='verify'),
    url(r'^Main/', views.main_page, name='main_page'),
    url(r'^addAccount', views.add_account, name='add_account'),
    url(r'^accountProfile/', views.acc_pro, name='acc_pro'),
    url(r'^accountProfile(?P<slink>.+)', views.change, name='change'),
    url(r'^Success(?P<key>.+)/', views.redirects, name='sign_success'),
    url(r'^changeUsername/', views.change, name='change_user'),
    url(r'^changePassword/', views.change, name='change_password'),
    url(r'^confirmUpdate/', views.confirm, name='confirm_update'),
    url(r'^addAuthUsers/', views.change, name='addAuthUsers'),
    url(r'^paperlessEnrollment/', views.change, name='paperless'),
    url(r'^updateContactInfo/', views.change, name='contact_update'),

    url(r'^logout/', views.logout, name='logout')
]
