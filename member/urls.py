
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="dashboard"),
    path('registration/', views.registration, name="registration"),
    path('updateMember/<str:pk>/', views.updateMember, name="updateMember"),
    path('deleteMember/<str:pk>/', views.deleteMember, name="deleteMember"),
    path('member/<str:pk>/', views.member, name="member"),
    path('memberEdit/<str:pk>/', views.memberEdit, name="memberEdit"),
    path('user/', views.userPage, name="user-page"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.register, name="register"),
    path('opt/', views.opt, name="opt"),
    path('listMember/', views.listMember, name="listMember"),
    path('errorPage/', views.errorPage, name="errorPage"),
    path('accountSetting/', views.accountSetting, name="accountSetting"),
    path('userEdit/', views.userEdit, name="userEdit"),

    path('listAhli/', views.listAhli, name="listAhli"),
    path('listPending/', views.listPending, name="listPending"),
    path('listTerminate/', views.listTerminate, name="listTerminate"),
    path('listNewMember/', views.listNewMember, name="listNewMember"),

    path('export-members/', views.export_members, name='export_members'),
    

    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='member/password_change_form.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='member/password_change_done.html'), name='password_change_done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('import-member-fees/', views.import_member_fees, name='import-fees'),
  

    path('update-member-status/', views.update_member_status, name='update_member_status'),
    
    path('member/<int:member_id>/fees/', views.member_fee_detail, name='member_fee_detail'),



# =========== txt to excel =========
    path('upload/', views.upload_file, name='upload_file'),

# chart


#fee table
    path('member-fees/', views.member_fees_table, name='member_fees'),
    path('download_excel/', views.download_excel, name='download_excel'),



]
