"""
Music-Makro API - REST API Server
Análise de áudio via API REST com autenticação JWT
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import tempfile
import time
import uuid

from config import settings
from api.models import Token, AnalysisResponse, ErrorResponse, HealthResponse, User
from api.auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from api.rate_limit import limiter
from slowapi.errors import RateLimitExceeded

from core.audio_analyzer import AudioAnalyzer

# Criar app FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API REST para análise de áudio e geração de descrições para Ace Step 1.5",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adicionar rate limiter
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "success": False,
            "error": "Rate limit exceeded",
            "detail": "Too many requests. Please try again later.",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc),
            timestamp=datetime.utcnow()
        ).dict()
    )

# ============================================================================
# ENDPOINTS PÚBLICOS
# ============================================================================

@app.get("/", response_model=HealthResponse)
async def root():
    """Endpoint raiz - Health check"""
    return HealthResponse(
        status="online",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow()
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Verifica saúde da API"""
    return HealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow()
    )

# ============================================================================
# AUTENTICAÇÃO
# ============================================================================

@app.post("/token", response_model=Token)
@limiter.limit("5/minute")
async def login(request: Request, username: str, password: str):
    """
    Endpoint de autenticação JWT
    
    Retorna token Bearer para uso nos endpoints protegidos
    """
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# ============================================================================
# ENDPOINTS PROTEGIDOS
# ============================================================================

@app.post("/analyze", response_model=AnalysisResponse)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def analyze_audio(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Analisa arquivo MP3 e retorna descrição para Ace Step 1.5
    
    Requer: Bearer token (obtenha via /token)
    """
    start_time = time.time()
    
    # Validar tipo de arquivo
    if not file.filename.lower().endswith('.mp3'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only MP3 files are supported"
        )
    
    # Validar tamanho
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
        )
    
    # Garantir diretório temporário
    settings.ensure_temp_dir()
    
    # Salvar temporariamente
    temp_path = os.path.join(settings.TEMP_DIR, f"{uuid.uuid4()}.mp3")
    with open(temp_path, 'wb') as f:
        f.write(contents)
    
    try:
        # Analisar áudio
        analyzer = AudioAnalyzer(temp_path)
        technical_data = analyzer.analyze()
        description = analyzer.generate_description(technical_data)
        
        processing_time = time.time() - start_time
        analysis_id = str(uuid.uuid4())
        
        return AnalysisResponse(
            success=True,
            file_name=file.filename,
            analysis_id=analysis_id,
            timestamp=datetime.utcnow(),
            technical_data=technical_data,
            description=description,
            processing_time_seconds=round(processing_time, 2)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )
    finally:
        # Limpar arquivo temporário
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Retorna informações do usuário autenticado"""
    return current_user

# ============================================================================
# UTILITÁRIOS (REMOVER EM PRODUÇÃO)
# ============================================================================

@app.get("/utils/hash-password")
async def hash_password_util(password: str):
    """
    Gera hash bcrypt de uma senha
    
    ⚠️ REMOVA ESTE ENDPOINT EM PRODUÇÃO!
    """
    return {
        "password": password,
        "password_hash": get_password_hash(password),
        "warning": "Remove this endpoint in production!"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )