# accounts/urls.py
from django.urls import path
from .views import AllGuests, HomeEpisodes, RegisterView, LoginView, ai_generate, app_settings, generate_blog,logout_view,google_login,Register,Login,AssessmentCreateView,\
ForgotPasswordView, VerifyOtpView, ResetPasswordView,LoginOtpSendView,LoginOtpVerifyView,IntalksStatsGet,AllEpisodes, submit_eod, submit_onboarding, test_api,youtube_stats,save_questionnaire, youtube_stats,push_to_github

urlpatterns = [
    path('registerUser', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', logout_view, name='logout'),
    path('google-login/', google_login, name='google_login'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path("login-otp/send/", LoginOtpSendView.as_view()),
    path("login-otp/verify/", LoginOtpVerifyView.as_view()),
    path('assessment/', AssessmentCreateView.as_view(), name='assessment'),
    path('intalks-stats/', IntalksStatsGet.as_view(), name='intalks-stats'),
    path('home-episodes/', HomeEpisodes.as_view(),name='home-episodes'),
    path('episodes/', AllEpisodes.as_view(), name="episodes"),
    path('guests/', AllGuests.as_view(),name='guests'),
    path("questionnaire/", save_questionnaire, name="questionnaire"),
    path("youtube-stats/", youtube_stats, name="youtube-stats"),
    path("submit-onboarding/", submit_onboarding, name="submit-onboarding"),
    path("daily-work-report/", submit_eod, name="daily-work-report"),
    path("test-api/", test_api, name="test-api"),
    path('generate-blog/', generate_blog, name='generate-blog'),
    path('ai-generate/', ai_generate, name='ai-generate'),        # NEW — required
    path('push-to-github/', push_to_github, name='push-to-github'),
    path('app-settings/', app_settings, name='app-settings'),



    # path('forgot-password/', ForgotPassword.as_view(), name='forgot-password'),  # ✅ NEW
    # path('reset-password/', ResetPassword.as_view(), name='reset-password'),      # ✅ NEW
    
]
