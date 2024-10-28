from django.shortcuts import render, redirect , get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings  # Import settings
from .models import Question, Choice, TestResult,Response
from django.contrib.auth.decorators import login_required
from personalityperfume.models import PersonalityPerfume
from django.http import Http404
from django.contrib import messages
from .models import TestResult
import speech_recognition as sr
import json




@login_required
def personality_test(request):
    questions = Question.objects.all()

    if request.method == 'POST':
        total_score = 0
        # Create or get the TestResult instance for the user
        test_result, created = TestResult.objects.update_or_create(
            user=request.user,
            defaults={'personality_type': '', 'score': 0}  # Initialize if creating
        )

        # Iterate through each question to calculate the total score and save responses
        for question in questions:
            response_value = request.POST.get(f'question_{question.id}')
            if response_value:
                # Update total score based on the response
                if response_value == 'yes':
                    total_score += 1  # Assign 1 point for "Yes"

                # Save the response in the Response model
                Response.objects.create(
                    test_result=test_result,
                    question=question,
                    value=response_value
                )

        # Define personality types based on score ranges
        if total_score < 10:
            personality_type = "Rêveur (Imagineur)"
        elif 10 <= total_score < 20:
            personality_type = "Empathique"
        elif 20 <= total_score < 30:
            personality_type = "Persévérant"
        elif 30 <= total_score < 40:
            personality_type = "Travaillomane (Analyseur)"
        elif 40 <= total_score < 50:
            personality_type = "Promoteur"
        else:
            personality_type = "Rebelle (Energiseur)"

        # Update the test result with the calculated score and personality type
        test_result.score = total_score
        test_result.personality_type = personality_type
        test_result.save()  # Save the updated TestResult

        # Save the result in the session
        request.session['test_result'] = {
            'personality_type': personality_type,
            'score': total_score
        }

        # Redirect to the result page with the personality type
        return redirect('test_result', personality_type=personality_type)

    return render(request, 'personality_test.html', {'questions': questions})

@login_required
def update_test(request):
    test_result = get_object_or_404(TestResult, user=request.user)
    questions = Question.objects.all()
    previous_responses = Response.objects.filter(test_result=test_result)
    responses_dict = {response.question.id: response.value for response in previous_responses}

    if request.method == 'POST':
        total_score = 0
        for question in questions:
            response_value = request.POST.get(f'question_{question.id}')
            if response_value:
                # Use a try-except block to handle potential multiple objects error
                try:
                    response, created = Response.objects.update_or_create(
                        question=question,
                        test_result=test_result,
                        defaults={'value': response_value}
                    )
                except MultipleObjectsReturned:
                    # Handle the case where more than one object is found
                    # You may want to log this error or clean up duplicates in the database
                    responses = Response.objects.filter(question=question, test_result=test_result)
                    # You can delete the duplicates if needed
                    for duplicate in responses[1:]:  # Keep the first one
                        duplicate.delete()
                    # Now try to create or update again
                    response, created = Response.objects.update_or_create(
                        question=question,
                        test_result=test_result,
                        defaults={'value': response_value}
                    )

                if response_value == 'yes':
                    total_score += 1

        # Determine personality type based on score
        if total_score < 10:
            personality_type = "Rêveur (Imagineur)"
        elif 10 <= total_score < 20:
            personality_type = "Empathique"
        elif 20 <= total_score < 30:
            personality_type = "Persévérant"
        elif 30 <= total_score < 40:
            personality_type = "Travaillomane (Analyseur)"
        elif 40 <= total_score < 50:
            personality_type = "Promoteur"
        else:
            personality_type = "Rebelle (Energiseur)"

        # Save or update the test result
        TestResult.objects.update_or_create(
            user=request.user,
            defaults={'personality_type': personality_type, 'score': total_score}
        )

        # Save the result in the session
        request.session['test_result'] = {
            'personality_type': personality_type,
            'score': total_score
        }

        return redirect('test_result', personality_type=personality_type)

    return render(request, 'update_test.html', {
        'questions': questions,
        'previous_responses': responses_dict,
        'result': test_result
    })


    
def get_corresponding_perfume(personality_type):
    # Récupérer le parfum correspondant au type de personnalité
    try:
        return PersonalityPerfume.objects.get(personality_type=personality_type)
    except PersonalityPerfume.DoesNotExist:
        return None  # Ou un parfum par défaut si nécessaire
    # Retrieve the existing test result for the authenticated user
    test_result = get_object_or_404(TestResult, user=request.user)

    questions = Question.objects.all()
    previous_responses = {}  # Initialize to store responses

    if request.method == 'POST':
        total_score = 0
        for question in questions:
            response = request.POST.get(f'question_{question.id}')
            previous_responses[question.id] = response  # Store the response
            if response == 'yes':
                total_score += 1  # Assign 1 point for "Yes"

        # Define personality types based on score ranges
        if total_score < 10:
            personality_type = "Rêveur (Imagineur)"
        elif 10 <= total_score < 20:
            personality_type = "Empathique"
        elif 20 <= total_score < 30:
            personality_type = "Persévérant"
        elif 30 <= total_score < 40:
            personality_type = "Travaillomane (Analyseur)"
        elif 40 <= total_score < 50:
            personality_type = "Promoteur"
        else:
            personality_type = "Rebelle (Energiseur)"

        # Update the existing test result
        test_result.personality_type = personality_type
        test_result.score = total_score
        test_result.save()  # Save the updated result

        # Save the updated result in the session
        request.session['test_result'] = {
            'personality_type': personality_type,
            'score': total_score
        }

        try:
            # Retrieve the perfume corresponding to the updated personality type
            perfume = PersonalityPerfume.objects.get(personality_type=personality_type)
        except PersonalityPerfume.DoesNotExist:
            raise Http404("No perfume matching this personality type.")

        context = {
            'result': {
                'personality_type': personality_type,
                'score': total_score
            },
            'perfume': perfume
        }

        return render(request, 'test_result.html', context)

    # Populate previous responses if the user is updating
    for question in questions:
        previous_responses[question.id] = getattr(test_result, f'response_for_{question.id}', None)

    return render(request, 'update_test.html', {'questions': questions, 'previous_responses': previous_responses})



@login_required
def test_result(request, personality_type):
    result = request.session.get('test_result')  # Retrieve the test results from the session

    if not result:
        raise Http404("No test results found.")

    try:
        # Retrieve the perfume corresponding to the personality type
        perfume = PersonalityPerfume.objects.get(personality_type=personality_type)
    except PersonalityPerfume.DoesNotExist:
        raise Http404("No perfume matching this personality type.")

    
    context = {
        'result': result,
        'perfume': perfume,
    }
    
    return render(request, 'test_result.html',context)

def delete_test(request):
    # Vérifiez si l'utilisateur a un résultat de test
    try:
        test_result = TestResult.objects.get(user=request.user)
        test_result.delete()
        messages.success(request, "Votre test a été supprimé avec succès.")
    except TestResult.DoesNotExist:
        # Si aucun TestResult n'est trouvé, affichez un message d'erreur
        messages.error(request, "Aucun test à supprimer.")
    
    # Redirigez vers la page d'accueil ou une autre page appropriée
    return redirect('personality_test')  # Remplacez 'home' par l'URL de redirection souhaitée





# Define the available personalities
personalities = {
    "Rêveur (Imagineur)": ["dream", "imagine", "creative"],
    "Empathique": ["caring", "sensitive", "empathize"],
    "Persévérant": ["determined", "strong", "steady"],
    "Travaillomane (Analyseur)": ["analytical", "detailed", "methodical"],
    "Promoteur": ["enthusiastic", "energetic", "lively"],
    "Rebelle (Energiseur)": ["independent", "bold", "daring"]
}

def analyze_personality(description):
    # Analyzing the description to determine the personality
    for personality, keywords in personalities.items():
        if any(keyword in description.lower() for keyword in keywords):
            return personality
    return "Unknown personality"
    
@csrf_exempt  # Disable CSRF protection for this view (only if necessary)
def capture_voice_input(request):
    if request.method == "POST":
        data = json.loads(request.body)
        description = data.get("description", "")
        personality = analyze_personality(description)
        
        # Log for debugging
        print("Transcript:", description)
        print("Personality:", personality)

        # Return both the transcript and personality in the JSON response
        return JsonResponse({"transcript": description, "personality": personality})
    
    return JsonResponse({"error": "Invalid request"}, status=400)
