# api/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import librosa
import numpy as np
from sklearn.preprocessing import StandardScaler

class CompareAudioFiles(APIView):
    def post(self, request, format=None):
        # Assuming you are sending audio_file1 and audio_file2 in the request data
        audio_file1 = request.data.get('audio_file1', None)
        audio_file2 = request.data.get('audio_file2', None)

        if not audio_file1 or not audio_file2:
            return Response({'error': 'audio_file1 and audio_file2 are required in the request data'},
                            status=status.HTTP_400_BAD_REQUEST)

        distance = self.compare_audio_files(audio_file1, audio_file2)
        return Response({'distance': distance}, status=status.HTTP_200_OK)

    def compare_audio_files(self, audio_file1, audio_file2):
        # Load the audio files
        audio1, sr1 = librosa.load(audio_file1)
        audio2, sr2 = librosa.load(audio_file2)

        # Preprocess the audio files
        # Pad the audio files to the same length
        if len(audio2) < len(audio1):
            audio2 = np.pad(audio2, (0, len(audio1) - len(audio2)), 'constant')
        elif len(audio2) > len(audio1):
            audio1 = np.pad(audio1, (0, len(audio2) - len(audio1)), 'constant')

        # Extract features from the audio files
        features1 = librosa.feature.mfcc(y=audio1, sr=sr1)
        features2 = librosa.feature.mfcc(y=audio2, sr=sr2)

        # Normalize the extracted features
        scaler = StandardScaler()
        features1n = scaler.fit_transform(features1.reshape(-1, 1))
        features2n = scaler.transform(features2.reshape(-1, 1))

        # Compare the features using a distance metric
        distance = np.mean((features1n - features2n)**2)
        distance = 1 - distance
        distance = distance * 100
        print(distance)
        # Return the distance as a measure of similarity
        return distance

def form(request):
    return render(request, "form.html")