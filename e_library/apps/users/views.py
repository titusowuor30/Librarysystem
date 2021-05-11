from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.views import LoginView,PasswordResetView
from django.contrib import messages
from .models import *
from django.views.generic import CreateView
from .forms import *
from django.contrib.auth.decorators import login_required



class LoginView(LoginView):
    """
    Login view for Doorstep
    """
    template_name = 'users/auth//login.html'
    def get_context_data(self, **kwargs):
        next_url = self.request.GET.get('next', '')
        return super(LoginView, self).get_context_data(next_url=next_url, **kwargs)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if '@' in username:
            try:
                user = User.objects.get(email__iexact=username)
                username = user.username
            except User.DoesNotExist:
                pass

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('frontpage')
            else:
                error = ('Your account has been disabled. We apologize for any inconvenience! If this is a mistake'
                         ' please contact our <a href="mailto:%s">support</a>.') #% settings.SUPPORT_EMAIL
        else:
            messages.error = ('Username and password didn\'t matched, if you forgot your password?')

        return redirect('login')


def SingUp(request):
    return render(request, 'users/register.html')


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'users/auth/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        try:
            user=form.save()
            login(self.request, user)
            messages.success(self.request, 'User registration success!')
        except:
            messages.error('User registration failure!')
        return redirect('frontpage')


class LibmanSignUpView(CreateView):
    model = User
    form_class = LibmanSignUpForm
    template_name = 'users/auth/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'librarian'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        try:
            user = form.save()
            user.username = request.POST['username']
            user.password = request.POST['password']

            if '@' in username:
                try:
                    user = User.objects.get(email__iexact=username)
                    user.username = user.username
                except User.DoesNotExist:
                    pass

            user = authenticate(username=user.username, password=user.password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            messages.success(self.request, 'User registration success!')
        except:
            messages.error('User registration failure!')
        return redirect('frontpage')


@login_required
def profile(request):
    if request.method == 'POST':

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:

        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)




class ForgotPasswordView(PasswordResetView):
    """
    Password recovery view
    """
    template_name = 'users/auth/password_reset_form.html'
    page_title = 'Forgot password'

    def post(self, request):
        error = None
        success = None
        email = request.POST.get('email', None)

        if email:
            email = email.strip()
            try:
                user = User.objects.get_reset_code(email)

                # Sending password reset link email to user
                context = Context({'user': user, 'SITE_NAME': self.get_config('SITE_NAME'), 'DOMAIN': self.get_config('DOMAIN')})
                msg_subject = get_template("accounts/email/password_reset_subject.txt").render(context)
                context = Context({'user': user, 'SITE_NAME': self.get_config('SITE_NAME'), 'DOMAIN': self.get_config('DOMAIN')})
                msg_text = get_template("accounts/email/password_reset.html").render(context)
                to_email = '%s <%s>' % (user.get_full_name(), user.email)
                send_mail(msg_subject, msg_text, [to_email], True)

                success = 'Password reset intructions has been sent to your email address.'
            except Exception as e:
                   error = e

        return self.get(request, error=error, success=success)


class PasswordResetView(PasswordResetView):
    """
    Password recovery view
    """
    page_title = 'Password reset'
    template_name = 'users/auth/password_reset.html'

    def get(self, request, user_id, reset_code):
        form = PasswordResetForm()
        return super(PasswordResetView, self).get(request, form=form, user_id=user_id, reset_code=reset_code)

    def post(self, request, user_id, reset_code):
        error = None
        success = None
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            try:
                User.objects.reset_password(user_id, reset_code, data['password'])
                success = 'Your password has been successfully reset!'
            except DoorstepError as e:
                error = e.message

        return super(PasswordResetView, self).get(request, form=form, user_id=user_id, reset_code=reset_code,
                                                  error=error, success=success)


class ChangePasswordView(PasswordResetView):
    """
    Password recovery view
    """
    page_title = 'Change password'
    template_name = 'users/auth/change_password.html'
    decorators = [login_required]

    def get(self, request):
        form = ChangePasswordForm()
        return super(ChangePasswordView, self).get(request, form=form)

    def post(self, request):
        error = None
        success = None
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            try:
                User.objects.change_password(request.user, data['current_password'], data['password'])
                success = 'Your password has been successfully changed!'
            except DoorstepError as e:
                error = e.message

        return super(ChangePasswordView, self).get(request, form=form, error=error, success=success)
