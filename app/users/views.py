import random
import string
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.hashers import make_password
from .models import OTP, User
from .serializers import UserSerializer
from .utils import envoyer_email
from .permissions import IsAuthenticated ,IsAny ,IsAdmin

class SendOTPView(APIView):
    
    def post(self, request):
        try:
            email = request.data.get('email')
            if not email:
                return Response({"error": "Email requis"}, status=status.HTTP_400_BAD_REQUEST)

            otp_code = str(random.randint(100000, 999999))

            OTP.objects.filter(email=email).delete() 
            OTP.objects.create(email=email, code=otp_code)

            if envoyer_email(email, f"Votre code OTP est : {otp_code}"):
                return Response({"message": "OTP envoyé avec succès", "email": email}, status=status.HTTP_200_OK)

            return Response({"error": "Échec de l'envoi de l'OTP"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({"error": f"Erreur interne du serveur: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignupView(APIView):
    permission_classes = [IsAny]
    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp')

        if not email or not otp_code:
            return Response({"error": "Email et OTP requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_instance = OTP.objects.get(email=email, code=otp_code, is_used=False)
            if not otp_instance.is_valid():
                return Response({"error": "OTP expiré ou déjà utilisé"}, status=status.HTTP_400_BAD_REQUEST)
        except OTP.DoesNotExist:
            return Response({"error": "OTP invalide"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            otp_instance.is_used = True  
            otp_instance.save()
            return Response({"message": "Inscription réussie."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordView(APIView):
    permission_classes = [IsAny]
    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp')
        new_password = request.data.get('password')

        if not all([email, otp_code, new_password]):
            return Response({"error": "Tous les champs sont requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_instance = OTP.objects.get(email=email, code=otp_code, is_used=False)
            if not otp_instance.is_valid():
                return Response({"error": "OTP invalide ou expiré"}, status=status.HTTP_400_BAD_REQUEST)
        except OTP.DoesNotExist:
            return Response({"error": "OTP invalide"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()

        otp_instance.is_used = True
        otp_instance.save()

        return Response({"message": "Mot de passe mis à jour avec succès"}, status=status.HTTP_200_OK)


class RequestOldEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.user.email  
        otp_code = str(random.randint(100000, 999999))

        OTP.objects.filter(email=email).delete()
        OTP.objects.create(email=email, code=otp_code)

        envoyer_email(email, f"Votre code OTP pour confirmer votre ancienne adresse email est : {otp_code}")

        return Response({
            "message": "OTP envoyé pour l'ancienne adresse email",
            "email": email
        }, status=status.HTTP_200_OK)


class RequestNewEmailOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_email = request.user.email
        otp_code = request.data.get('otp')
        new_email = request.data.get('new_email')

        if not new_email or not otp_code:
            return Response({"error": "Nouvel email et OTP requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_instance = OTP.objects.get(email=old_email, code=otp_code, is_used=False)
            if not otp_instance.is_valid():
                return Response({"error": "OTP invalide ou expiré"}, status=status.HTTP_400_BAD_REQUEST)
        except OTP.DoesNotExist:
            return Response({"error": "OTP invalide"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=new_email).exists():
            return Response({"error": "Cette adresse email est déjà utilisée"}, status=status.HTTP_400_BAD_REQUEST)

        new_otp_code = str(random.randint(100000, 999999))
        OTP.objects.filter(email=new_email).delete()  # Supprimer tout ancien OTP pour ce nouvel email
        OTP.objects.create(email=new_email, code=new_otp_code)

        envoyer_email(new_email, f"Votre code OTP pour confirmer votre nouvelle adresse email est : {new_otp_code}")

        otp_instance.is_used = True
        otp_instance.save()

        return Response({
            "message": "OTP envoyé au nouvel email",
            "new_email": new_email
        }, status=status.HTTP_200_OK)


class AddModerateur(APIView):
    permission_classes = [IsAdmin]
    
    def generate_random_password(self, length=10):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def post(self, request):
        email = request.data.get('email')
        name = request.data.get('name')

        if not email or not name:
            return Response({"error": "Email et nom sont requis"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Cet email est déjà utilisé"}, status=status.HTTP_400_BAD_REQUEST)

        password = self.generate_random_password()
        user = User.objects.create(
            email=email,
            name=name,
            role='moderateur',
            password=make_password(password)
        )

        email_subject = "Compte Modérateur Créé"
        email_body = f"Bonjour {name},\n\nVotre compte modérateur a été créé avec succès.\n\nIdentifiant: {email}\nMot de passe: {password}\n\nVeuillez modifier votre mot de passe après votre première connexion.\n\nCordialement,\nL'équipe"

        envoyer_email(email, email_body)

        return Response({"message": "Modérateur ajouté avec succès, les identifiants ont été envoyés par email."}, status=status.HTTP_201_CREATED)

    

class VerifyNewEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_email = request.data.get('new_email')
        otp_code = request.data.get('otp')

        if not new_email or not otp_code:
            return Response({"error": "Nouvel email et OTP requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_instance = OTP.objects.get(email=new_email, code=otp_code, is_used=False)
            if not otp_instance.is_valid():
                return Response({"error": "OTP invalide ou expiré"}, status=status.HTTP_400_BAD_REQUEST)
        except OTP.DoesNotExist:
            return Response({"error": "OTP invalide"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.email = new_email
        request.user.save()

        otp_instance.is_used = True
        otp_instance.save()

        return Response({"message": "Adresse email mise à jour avec succès"}, status=status.HTTP_200_OK)

class LoginAPIView(APIView):
    permission_classes = [IsAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"error": "Identifiants incorrects"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "message": "Connexion réussie",
            "access_token": access_token,
            "refresh_token": str(refresh),
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)

            return Response({"message": "Déconnexion réussie"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Token invalide ou expiré"}, status=status.HTTP_400_BAD_REQUEST)


class CheckAuthView(APIView):
    permission_classes = [IsAny]
    def post(self, request):

        access_token = request.data.get("access_token")
        refresh_token = request.data.get("refresh_token")

        if not access_token or not refresh_token:
            return Response({"error": "Tokens requis"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            access = AccessToken(access_token)
            user = User.objects.get(id=access["user_id"])

            return Response({
                "message": "Utilisateur authentifié",
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        except Exception:
            try:
                refresh = RefreshToken(refresh_token)
                new_access_token = str(refresh.access_token)
                user = User.objects.get(id=refresh["user_id"])

                return Response({
                    "message": "Token rafraîchi",
                    "access_token": new_access_token,
                    "refresh_token": str(refresh),
                    "user": UserSerializer(user).data
                }, status=status.HTTP_200_OK)

            except Exception:
                return Response({"error": "Refresh token invalide"}, status=status.HTTP_401_UNAUTHORIZED)
            

