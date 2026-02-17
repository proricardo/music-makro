"""
Music-Makro - Interface Gráfica
Aplicação desktop para análise de áudio
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import threading

from core.audio_analyzer import AudioAnalyzer
from config import settings

class MusicMakroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{settings.APP_NAME} v{settings.APP_VERSION}")
        self.root.geometry("1100x750")
        
        self.file_path = tk.StringVar()
        self.analyzing = False
        self.setup_ui()
        
    def setup_ui(self):
        """Configura interface gráfica"""
        # Header
        header = tk.Frame(self.root, bg="#2C3E50", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header, 
            text=settings.APP_NAME,
            font=("Arial", 18, "bold"),
            bg="#2C3E50",
            fg="white"
        ).pack(pady=15)
        
        # Frame superior - Seleção de arquivo
        top_frame = tk.Frame(self.root, padx=15, pady=15, bg="#ECF0F1")
        top_frame.pack(fill=tk.X)
        
        tk.Label(
            top_frame, 
            text="Arquivo MP3:", 
            font=("Arial", 11, "bold"),
            bg="#ECF0F1"
        ).pack(side=tk.LEFT)
        
        entry = tk.Entry(top_frame, textvariable=self.file_path, width=65, font=("Arial", 10))
        entry.pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            top_frame, 
            text="📁 Selecionar", 
            command=self.select_file,
            bg="#3498DB",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=3)
        
        tk.Button(
            top_frame, 
            text="▶ Analisar", 
            command=self.analyze_file,
            bg="#27AE60",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=3)
        
        # Frame de progresso
        self.progress_frame = tk.Frame(self.root, padx=15, bg="#ECF0F1")
        self.progress_frame.pack(fill=tk.X)
        
        self.progress_label = tk.Label(
            self.progress_frame, 
            text="",
            font=("Arial", 9),
            bg="#ECF0F1"
        )
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='indeterminate')
        
        # Frame central - Análise técnica
        middle_frame = tk.LabelFrame(
            self.root, 
            text="📊 Análise Técnica", 
            padx=15, 
            pady=10,
            font=("Arial", 10, "bold")
        )
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 10))
        
        self.technical_text = scrolledtext.ScrolledText(
            middle_frame, 
            height=10, 
            font=("Consolas", 9),
            bg="#FAFAFA"
        )
        self.technical_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame inferior - Descrição
        bottom_frame = tk.LabelFrame(
            self.root, 
            text="🎵 Descrição para Ace Step 1.5", 
            padx=15, 
            pady=10,
            font=("Arial", 10, "bold")
        )
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        self.description_text = scrolledtext.ScrolledText(
            bottom_frame, 
            height=12, 
            font=("Arial", 10), 
            wrap=tk.WORD,
            bg="#FAFAFA"
        )
        self.description_text.pack(fill=tk.BOTH, expand=True)
        
        # Botões de ação
        button_frame = tk.Frame(self.root, padx=15, pady=10, bg="#ECF0F1")
        button_frame.pack(fill=tk.X)
        
        tk.Button(
            button_frame, 
            text="📋 Copiar Descrição", 
            command=self.copy_description,
            bg="#9B59B6",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame, 
            text="💾 Salvar JSON", 
            command=self.save_json,
            bg="#34495E",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame, 
            text="🗑️ Limpar", 
            command=self.clear_all,
            bg="#95A5A6",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            relief=tk.FLAT
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame, 
            text="❌ Sair", 
            command=self.root.quit,
            bg="#E74C3C",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            relief=tk.FLAT
        ).pack(side=tk.RIGHT, padx=5)
        
    def select_file(self):
        """Abre diálogo para selecionar arquivo MP3"""
        filename = filedialog.askopenfilename(
            title="Selecionar arquivo MP3",
            filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
    
    def analyze_file(self):
        """Inicia análise do arquivo em thread separada"""
        if not self.file_path.get():
            messagebox.showwarning("Aviso", "Selecione um arquivo MP3 primeiro")
            return
        
        if not os.path.exists(self.file_path.get()):
            messagebox.showerror("Erro", "Arquivo não encontrado")
            return
        
        if self.analyzing:
            return
        
        self.analyzing = True
        self.progress_label.config(text="Analisando arquivo...")
        self.progress_bar.pack(fill=tk.X, pady=5)
        self.progress_bar.start(10)
        
        thread = threading.Thread(target=self.run_analysis, daemon=True)
        thread.start()
    
    def run_analysis(self):
        """Executa análise completa do arquivo"""
        try:
            analyzer = AudioAnalyzer(self.file_path.get())
            
            self.root.after(0, self.progress_label.config, {"text": "Extraindo features de áudio..."})
            technical_data = analyzer.analyze()
            
            self.root.after(0, self.progress_label.config, {"text": "Gerando descrição para Ace Step 1.5..."})
            description = analyzer.generate_description(technical_data)
            
            self.root.after(0, self.update_results, technical_data, description)
            
        except Exception as e:
            self.root.after(
                0, 
                messagebox.showerror, 
                "Erro", 
                f"Erro na análise:\n{str(e)}\n\nVerifique se o FFmpeg está instalado."
            )
        finally:
            self.analyzing = False
            self.root.after(0, self.progress_bar.stop)
            self.root.after(0, self.progress_bar.pack_forget)
            self.root.after(0, self.progress_label.config, {"text": ""})
    
    def update_results(self, technical_data, description):
        """Atualiza interface com resultados"""
        self.technical_text.delete(1.0, tk.END)
        tech_str = json.dumps(technical_data, indent=2, ensure_ascii=False)
        self.technical_text.insert(1.0, tech_str)
        
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(1.0, description)
    
    def copy_description(self):
        """Copia descrição para clipboard"""
        description = self.description_text.get(1.0, tk.END).strip()
        if description:
            self.root.clipboard_clear()
            self.root.clipboard_append(description)
            messagebox.showinfo("Sucesso", "Descrição copiada para a área de transferência!")
    
    def save_json(self):
        """Salva resultados em arquivo JSON"""
        technical = self.technical_text.get(1.0, tk.END).strip()
        description = self.description_text.get(1.0, tk.END).strip()
        
        if not technical or not description:
            messagebox.showwarning("Aviso", "Nenhum dado para salvar")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        
        if filename:
            try:
                data = {
                    "file": self.file_path.get(),
                    "technical_analysis": json.loads(technical),
                    "ace_step_description": description
                }
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Sucesso", "Análise salva com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
    
    def clear_all(self):
        """Limpa todos os campos"""
        self.file_path.set("")
        self.technical_text.delete(1.0, tk.END)
        self.description_text.delete(1.0, tk.END)

def main():
    """Função principal"""
    print("=" * 70)
    print(f"{settings.APP_NAME} v{settings.APP_VERSION}")
    print("=" * 70)
    
    required = ['librosa', 'numpy', 'soundfile', 'mutagen']
    missing = []
    
    for module in required:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"\n⚠️  DEPENDÊNCIAS FALTANDO: {', '.join(missing)}")
        print(f"\nInstale com: pip install {' '.join(missing)}")
        input("\nPressione ENTER para sair...")
        sys.exit(1)
    
    print("✓ Todas as dependências instaladas\n")
    print("Iniciando interface gráfica...\n")
    
    root = tk.Tk()
    app = MusicMakroGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()