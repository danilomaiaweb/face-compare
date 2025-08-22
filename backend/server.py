from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import cv2
import numpy as np
from PIL import Image
import io
import base64
from sklearn.metrics.pairwise import cosine_similarity

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Load OpenCV face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class FaceComparisonResult(BaseModel):
    image_index: int
    similarity_percentage: float
    has_face: bool
    image_data: Optional[str] = None  # Base64 encoded image
    error_message: Optional[str] = None

class ComparisonResponse(BaseModel):
    base_image_has_face: bool
    base_image_data: Optional[str] = None  # Base64 encoded base image
    results: List[FaceComparisonResult]
    total_images: int
    processing_time: float

def detect_faces(image_array):
    """Detect faces in an image using OpenCV"""
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        return len(faces) > 0, faces
    except Exception as e:
        return False, []

def extract_face_features(image_array, faces):
    """Extract simple features from detected faces"""
    try:
        if len(faces) == 0:
            return None
            
        # Get the largest face
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = largest_face
        
        # Extract face region
        face_region = image_array[y:y+h, x:x+w]
        
        # Resize to standard size for comparison
        face_resized = cv2.resize(face_region, (128, 128))
        
        # Convert to grayscale and normalize
        if len(face_resized.shape) == 3:
            face_gray = cv2.cvtColor(face_resized, cv2.COLOR_RGB2GRAY)
        else:
            face_gray = face_resized
            
        # Calculate simple histogram features
        hist = cv2.calcHist([face_gray], [0], None, [256], [0, 256])
        features = hist.flatten()
        
        # Normalize features
        features = features / (np.linalg.norm(features) + 1e-6)
        
        return features
        
    except Exception as e:
        return None

def image_to_base64(image_array, max_size=(150, 150)):
    """Convert image array to base64 string for frontend display"""
    try:
        # Convert numpy array to PIL Image
        if isinstance(image_array, np.ndarray):
            image = Image.fromarray(image_array)
        else:
            image = image_array
            
        # Resize for thumbnail
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Convert to base64
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='JPEG', quality=80)
        img_buffer.seek(0)
        
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        return f"data:image/jpeg;base64,{img_str}"
        
    except Exception as e:
        return None

def calculate_similarity(features1, features2):
    """Calculate similarity between two feature vectors"""
    try:
        if features1 is None or features2 is None:
            return 0.0
            
        # Reshape for cosine similarity
        f1 = features1.reshape(1, -1)
        f2 = features2.reshape(1, -1)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(f1, f2)[0][0]
        
        # Convert to percentage (0-100)
        similarity_percentage = max(0, min(100, similarity * 100))
        
        return float(similarity_percentage)
        
    except Exception as e:
        return 0.0

def process_uploaded_image(file_content):
    """Process uploaded image and return numpy array"""
    try:
        # Open image with PIL
        image = Image.open(io.BytesIO(file_content))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Convert to numpy array
        image_array = np.array(image)
        
        return image_array
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Face Comparison API"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

@api_router.post("/compare-faces", response_model=ComparisonResponse)
async def compare_faces(
    base_image: UploadFile = File(...),
    comparison_images: List[UploadFile] = File(...)
):
    """Compare faces between base image and multiple comparison images"""
    start_time = datetime.now()
    
    try:
        # Validate file count
        if len(comparison_images) > 50:
            raise HTTPException(status_code=400, detail="Maximum 50 images allowed")
        
        # Process base image
        base_content = await base_image.read()
        base_array = process_uploaded_image(base_content)
        
        # Detect faces in base image
        base_has_face, base_faces = detect_faces(base_array)
        
        if not base_has_face:
            raise HTTPException(
                status_code=400, 
                detail="Nenhum rosto detectado na imagem base. Por favor, envie uma imagem com pelo menos um rosto visível."
            )
        
        # Extract features from base image
        base_features = extract_face_features(base_array, base_faces)
        
        if base_features is None:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível extrair características da face na imagem base."
            )
        
        # Process comparison images
        results = []
        
        for i, comp_image in enumerate(comparison_images):
            try:
                # Process comparison image
                comp_content = await comp_image.read()
                comp_array = process_uploaded_image(comp_content)
                
                # Detect faces
                comp_has_face, comp_faces = detect_faces(comp_array)
                
                if not comp_has_face:
                    results.append(FaceComparisonResult(
                        image_index=i,
                        similarity_percentage=0.0,
                        has_face=False,
                        error_message="Nenhum rosto detectado nesta imagem"
                    ))
                    continue
                
                # Extract features
                comp_features = extract_face_features(comp_array, comp_faces)
                
                if comp_features is None:
                    results.append(FaceComparisonResult(
                        image_index=i,
                        similarity_percentage=0.0,
                        has_face=True,
                        error_message="Não foi possível extrair características da face"
                    ))
                    continue
                
                # Calculate similarity
                similarity = calculate_similarity(base_features, comp_features)
                
                results.append(FaceComparisonResult(
                    image_index=i,
                    similarity_percentage=similarity,
                    has_face=True
                ))
                
            except Exception as e:
                results.append(FaceComparisonResult(
                    image_index=i,
                    similarity_percentage=0.0,
                    has_face=False,
                    error_message=f"Erro ao processar imagem: {str(e)}"
                ))
        
        # Sort results by similarity (highest first)
        results.sort(key=lambda x: x.similarity_percentage, reverse=True)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return ComparisonResponse(
            base_image_has_face=True,
            results=results,
            total_images=len(comparison_images),
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()