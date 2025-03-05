import re
import requests
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request,'index.html')

@csrf_exempt
def resume_parse(request):
    if request.method == 'POST':
        # Step 1: Parse the resume
        resume_file = request.FILES['resume']
        files = {'file': resume_file}
        parse_url = f"{settings.NGROK_URL}/parse-resume"
        parse_response = requests.post(parse_url, files=files)

        if parse_response.status_code != 200:
            return JsonResponse({"error": "Failed to parse resume"}, status=parse_response.status_code)

        resume_text = parse_response.json().get('resume_text')

        # Step 2: Evaluate the resume
        jd_a = request.POST.get('jd_a').strip()
        jd_b = request.POST.get('jd_b').strip()
        jd_b_entered = bool(jd_b)

        evaluate_url = f"{settings.NGROK_URL}/evaluate-resume"
        evaluate_data = {
            'resume_text': resume_text,
            'jd_a': jd_a,
            'jd_b': jd_b,
        }

        evaluate_response = requests.post(evaluate_url, json=evaluate_data)

        if evaluate_response.status_code != 200:
            return JsonResponse({"error": "Failed to evaluate resume"}, status=evaluate_response.status_code)

        evaluation_results = evaluate_response.json().get('evaluation_results')

        # Step 3: Summarize the resume
        summarize_url = f"{settings.NGROK_URL}/summarize-resume"
        summarize_data = {'resume_text': resume_text}
        summarize_response = requests.post(summarize_url, json=summarize_data)

        if summarize_response.status_code != 200:
            return JsonResponse({"error": "Failed to summarize resume"}, status=summarize_response.status_code)

        summary = summarize_response.json().get('summary')
 

         # Step 4: Extract X-Factor
        x_factor_url = f"{settings.NGROK_URL}/x-factor" 
        x_factor_data = {
            'resume_text': resume_text,
            'jd_a': jd_a,
            'jd_b': jd_b,
        }
        x_factor_response = requests.post(x_factor_url, json=x_factor_data)
        if x_factor_response.status_code != 200:
            return JsonResponse({"error": "Failed to extract X-Factor"}, status=x_factor_response.status_code)

        x_factor = x_factor_response.json().get('x_factor')

    return render(request, 'result.html',{
        'resume_text': resume_text,
        'evaluation_results': evaluation_results,
        'summary': summary,
        'x_factor': x_factor,
        'jd_b_entered': jd_b_entered
    })

