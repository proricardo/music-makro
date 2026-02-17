"""
Music-Makro - Description Generator
Gerador de descrições textuais para Ace Step 1.5
"""

class DescriptionGenerator:
    """Converte análise técnica em descrição textual"""
    
    def __init__(self, technical_data: dict):
        self.data = technical_data
        
    def generate(self) -> str:
        """Gera descrição completa no estilo Ace Step 1.5"""
        
        genre_style = self._identify_genre_style()
        atmosphere = self._describe_atmosphere()
        structure = self._describe_structure()
        vocals = self._describe_vocals()
        lyrics_theme = self._describe_lyrics_theme()
        production = self._describe_production()
        
        description = f"""{genre_style}
{atmosphere}
{structure}
{vocals}
{lyrics_theme}
{production}"""
        
        return description.strip()
    
    def _identify_genre_style(self) -> str:
        """Identifica gênero e estilo musical"""
        tempo = self.data['rhythmic']['tempo_bpm']
        percussive_ratio = self.data['harmonic']['percussive_ratio']
        spectral_centroid = self.data['spectral']['centroid_mean']
        energy = self.data['energy']['loudness_mean']
        
        if tempo > 120 and percussive_ratio > 0.5 and energy > -20:
            if spectral_centroid > 2000:
                return "Funk / Trap: A heavy, bass-driven Brazilian track inspired by the raw street intensity of MC Poze do Rodo blended with the melodic trap swagger of Matuê."
            else:
                return "Funk Carioca / Phonk: A raw street funk with deep bass and minimal melodic elements, channeling underground Brazilian sound."
        elif tempo < 90 and self.data['harmonic']['harmonic_ratio'] > 0.6:
            return "R&B / Soul: A smooth, melodic track with rich harmonic textures and emotional depth."
        elif tempo > 140 and percussive_ratio > 0.6:
            return "Electronic / Dance: A high-energy electronic track with pulsating rhythms and club-ready production."
        else:
            return "Urban / Hip-Hop: A contemporary urban track blending various street music influences with modern production techniques."
    
    def _describe_atmosphere(self) -> str:
        """Descreve atmosfera e elementos sonoros"""
        loudness = self.data['energy']['loudness_mean']
        dynamic_range = self.data['energy']['dynamic_range']
        
        if loudness > -15 and dynamic_range > 0.05:
            atmosphere = "Dark, dominant atmosphere"
        elif loudness > -20:
            atmosphere = "Energetic, vibrant atmosphere"
        else:
            atmosphere = "Smooth, laid-back atmosphere"
        
        elements = []
        
        if self.data['spectral']['rolloff_mean'] < 3000:
            elements.append("distorted sub-heavy 808s")
        if self.data['rhythmic']['onset_strength_max'] > 0.5:
            elements.append("hard punchy kicks")
        if dynamic_range > 0.06:
            elements.append("explosive snares")
        
        elements.extend(["classic tamborzão percussion", "spacious trap-style hi-hats"])
        
        return f"{atmosphere} with {', '.join(elements)}."
    
    def _describe_structure(self) -> str:
        """Descreve estrutura e progressão"""
        tempo = self.data['rhythmic']['tempo_bpm']
        duration = self.data['metadata']['duration']
        
        return f"The instrumental builds from a tense, minimal intro into a massive low-end drop, layering hypnotic rhythms with cinematic synth textures over {int(duration/60)} minutes at {int(tempo)} BPM."
    
    def _describe_vocals(self) -> str:
        """Descreve características vocais"""
        tempo = self.data['rhythmic']['tempo_bpm']
        
        if tempo > 120:
            return "Vocals delivered with commanding, gritty flow — alternating between aggressive chant-style funk cadence and melodic trap hooks with autotuned textures."
        else:
            return "Vocals delivered with smooth, melodic flow — balancing emotional delivery with rhythmic precision and subtle vocal layering."
    
    def _describe_lyrics_theme(self) -> str:
        """Descreve temática lírica"""
        genre_meta = self.data['metadata'].get('genre', 'Unknown').lower()
        
        if 'funk' in genre_meta or 'trap' in genre_meta:
            return "Lyrics centered on luxury cars, fast lifestyles, power, and seductive energy, maintaining a street-authentic tone without losing mainstream appeal."
        else:
            return "Lyrics exploring personal experiences, emotional depth, and contemporary themes with authentic storytelling and relatable narratives."
    
    def _describe_production(self) -> str:
        """Descreve qualidade de produção"""
        bitrate = self.data['metadata'].get('bitrate', 0)
        spectral_bandwidth = self.data['spectral']['bandwidth_mean']
        
        if bitrate > 256000 and spectral_bandwidth > 2000:
            quality = "gritty yet polished"
        elif bitrate > 128000:
            quality = "raw with professional clarity"
        else:
            quality = "authentic and street-ready"
        
        return f"Production must feel {quality} — heavy club pressure in the low-end, modern trap clarity in the highs, and the immersive energy of a packed Rio night scene."