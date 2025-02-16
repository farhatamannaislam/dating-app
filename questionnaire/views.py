from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import QuestionnaireForm
from .models import UserResponse


@login_required
def questionnaire(request):
    # Check if user has already filled out the questionnaire
    user_response = UserResponse.objects.filter(user=request.user).first()
    form = QuestionnaireForm(instance=user_response)

    if request.method == 'POST':
        form = QuestionnaireForm(request.POST, instance=user_response)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.save()
            form.save_m2m()
            profile = request.user.profile
            profile.spark_type = response.spark_type
            profile.save()
            profile.gender_preferences.set(response.gender_preferences.all())
            profile.age_preferences.set(response.age_preferences.all())

            messages.success(request, 'Your preferences have been saved!')
            return redirect('profiles:matching_profiles')

    return render(request, 'questionnaire/questionnaire.html', {
        'form': form,
        'is_edit': user_response is not None
    })
