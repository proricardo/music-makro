"""
Music-Makro - Audio Analyzer
Análise técnica de arquivos de áudio
"""

import librosa
import numpy as np
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from core.description_generator import DescriptionGenerator

class AudioAnalyzer:
    """Analisador de áudio com extração de features"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.y = None
        self.sr = None
        
    def analyze(self) -> dict:
        """Executa análise completa do arquivo de áudio"""
        print(f"\n[Music-Makro] Analisando: {self.file_path}")
        
        # Carregar áudio
        print("→ Carregando áudio...")
        self.y, self.sr = librosa.load(self.file_path, sr=None)
        
        # Extrair features
        metadata = self._extract_metadata()
        temporal = self._analyze_temporal()
        spectral = self._analyze_spectral()
        rhythmic = self._analyze_rhythmic()
        harmonic = self._analyze_harmonic()
        energy = self._analyze_energy()
        
        return {
            "metadata": metadata,
            "temporal": temporal,
            "spectral": spectral,
            "rhythmic": rhythmic,
            "harmonic": harmonic,
            "energy": energy
        }
    
    def _extract_metadata(self) -> dict:
        """Extrai metadados do arquivo MP3"""
        try:
            audio = MP3(self.file_path)
            duration = audio.info.length
            bitrate = audio.info.bitrate
            sample_rate = audio.info.sample_rate
            
            try:
                tags = ID3(self.file_path)
                title = str(tags.get('TIT2', 'Unknown'))
                artist = str(tags.get('TPE1', 'Unknown'))
                genre = str(tags.get('TCON', 'Unknown'))
            except:
                title = artist = genre = 'Unknown'
            
            return {
                "duration": round(duration, 2),
                "bitrate": bitrate,
                "sample_rate": sample_rate,
                "title": title,
                "artist": artist,
                "genre": genre
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _analyze_temporal(self) -> dict:
        """Análise de características temporais"""
        rms = librosa.feature.rms(y=self.y)[0]
        zcr = librosa.feature.zero_crossing_rate(self.y)[0]
        
        return {
            "rms_mean": float(np.mean(rms)),
            "rms_std": float(np.std(rms)),
            "rms_max": float(np.max(rms)),
            "zcr_mean": float(np.mean(zcr)),
            "zcr_std": float(np.std(zcr))
        }
    
    def _analyze_spectral(self) -> dict:
        """Análise espectral"""
        spectral_centroids = librosa.feature.spectral_centroid(y=self.y, sr=self.sr)[0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=self.y, sr=self.sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=self.y, sr=self.sr)[0]
        spectral_contrast = librosa.feature.spectral_contrast(y=self.y, sr=self.sr)
        spectral_flatness = librosa.feature.spectral_flatness(y=self.y)[0]
        
        return {
            "centroid_mean": float(np.mean(spectral_centroids)),
            "centroid_std": float(np.std(spectral_centroids)),
            "bandwidth_mean": float(np.mean(spectral_bandwidth)),
            "bandwidth_std": float(np.std(spectral_bandwidth)),
            "rolloff_mean": float(np.mean(spectral_rolloff)),
            "rolloff_std": float(np.std(spectral_rolloff)),
            "contrast_mean": float(np.mean(spectral_contrast)),
            "contrast_std": float(np.std(spectral_contrast)),
            "flatness_mean": float(np.mean(spectral_flatness)),
            "flatness_std": float(np.std(spectral_flatness))
        }
    
    def _analyze_rhythmic(self) -> dict:
        """Análise rítmica"""
        tempo, beats = librosa.beat.beat_track(y=self.y, sr=self.sr)
        onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=self.sr)
        
        return {
            "tempo_bpm": float(tempo),
            "beats_count": len(beats),
            "onset_strength_mean": float(np.mean(onset_env)),
            "onset_strength_max": float(np.max(onset_env)),
            "tempogram_mean": float(np.mean(tempogram)),
            "tempogram_std": float(np.std(tempogram))
        }
    
    def _analyze_harmonic(self) -> dict:
        """Análise harmônica"""
        y_harmonic, y_percussive = librosa.effects.hpss(self.y)
        chroma = librosa.feature.chroma_stft(y=self.y, sr=self.sr)
        mfccs = librosa.feature.mfcc(y=self.y, sr=self.sr, n_mfcc=13)
        tonnetz = librosa.feature.tonnetz(y=y_harmonic, sr=self.sr)
        
        return {
            "harmonic_ratio": float(np.sum(np.abs(y_harmonic)) / np.sum(np.abs(self.y))),
            "percussive_ratio": float(np.sum(np.abs(y_percussive)) / np.sum(np.abs(self.y))),
            "chroma_mean": float(np.mean(chroma)),
            "chroma_std": float(np.std(chroma)),
            "mfcc_mean": float(np.mean(mfccs)),
            "mfcc_std": float(np.std(mfccs)),
            "tonnetz_mean": float(np.mean(tonnetz)),
            "tonnetz_std": float(np.std(tonnetz))
        }
    
    def _analyze_energy(self) -> dict:
        """Análise de energia e dinâmica"""
        total_energy = np.sum(self.y ** 2)
        S = librosa.stft(self.y)
        loudness = librosa.amplitude_to_db(np.abs(S), ref=np.max)
        rms = librosa.feature.rms(y=self.y)[0]
        dynamic_range = np.max(rms) - np.min(rms)
        
        return {
            "total_energy": float(total_energy),
            "loudness_mean": float(np.mean(loudness)),
            "loudness_max": float(np.max(loudness)),
            "loudness_min": float(np.min(loudness)),
            "dynamic_range": float(dynamic_range)
        }
    
    def generate_description(self, technical_data: dict) -> str:
        """Gera descrição textual para Ace Step 1.5"""
        generator = DescriptionGenerator(technical_data)
        return generator.generate()