from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMessage
# from reportlab.pdfgen import canvas
import io
from .models import Subscription
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
def landing(request):
    return render(request, 'landing.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def service(request):
    return render(request, 'services.html')

def booking(request):
    return render(request, 'booking.html')
def room_list(request):
    return render(request, 'room_list_user.html')


@csrf_exempt
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscription, created = Subscription.objects.get_or_create(email=email)
            if created:
                try:
                    # Send notification email to admin
                    send_mail(
                        'New Subscription',
                        f'A new subscription request has been received from {email}.',
                        'akankshamarathe19@gmail.com',
                        ['akankshamarathe19@gmail.com'],
                        fail_silently=False,
                    )

                    # Generate PDF
                    pdf_buffer = generate_pdf(email)

                    # Plain text email body
                    email_subject = "Subscription Confirmation"
                    email_body = f"Dear {email},\n\nThank you for subscribing to our service. Please find attached a confirmation PDF with your subscription details.\n\nBest regards,\nYour Company Name"
                    email_message = EmailMessage(
                        email_subject,
                        email_body,
                        'akankshamarathe19@gmail.com',
                        [email],
                    )
                    email_message.attach('subscription_details.pdf', pdf_buffer.read(), 'application/pdf')
                    email_message.send()

                    return JsonResponse(
                        {'status': 'success', 'message': 'Subscription successful. Check your email for confirmation.'})
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': f'Failed to send email: {str(e)}'}, status=500)
            else:
                return JsonResponse({'status': 'error', 'message': 'You have already subscribed.'}, status=400)

        return JsonResponse({'status': 'error', 'message': 'Email not provided.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


def generate_pdf(email):
    pdf_buffer = io.BytesIO()
    p = canvas.Canvas(pdf_buffer)
    p.drawString(100, 750, f"Subscription Confirmation")
    p.drawString(100, 730, f"Thank you for subscribing to our service.")
    p.drawString(100, 710, f"Email: {email}")
    p.showPage()
    p.save()
    pdf_buffer.seek(0)  # Move buffer position to the start
    return pdf_buffer



def base_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if role == 'admin' and user.is_superuser:
                auth_login(request, user)
                messages.info(request, f'{username}, You are logged in as Admin.')
                return redirect('home')  # Replace with your admin home view name
            elif role == 'user' and not user.is_superuser:
                auth_login(request, user)
                messages.info(request, f'{username}, You are logged in as User.')
                return redirect('user_profile')  # Replace with your user profile view name
            else:
                messages.error(request, 'Invalid login credentials for the selected role.')
                return redirect('login')
        else:
            messages.error(request, 'Wrong username or password.')
            return redirect('base_login')

    return render(request, 'base_login.html')
