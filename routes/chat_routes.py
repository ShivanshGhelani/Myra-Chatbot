from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
import logging
from core.chat import ChatManager
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize chat manager
try:
    chat_manager = ChatManager()
except Exception as e:
    logger.error(f"Failed to initialize ChatManager: {str(e)}")
    # Don't raise here, let the endpoints handle it

class ChatRequest(BaseModel):
    query: str

    @field_validator('query')
    @classmethod
    def query_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()

class TextInput(BaseModel):
    text: str

    @field_validator('text')
    @classmethod
    def text_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty')
        return v.strip()

class SummarizeRequest(BaseModel):
    text: str

    @field_validator('text')
    @classmethod
    def text_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty')
        if len(v.strip()) < 10:
            raise ValueError('Text is too short to summarize')
        return v.strip()

class Detection(BaseModel):
    object_id: str
    position: str
    confidence: float

class DetectionData(BaseModel):
    status: str
    filename: str
    detections: Dict[str, List[Detection]]

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v != "success":
            raise ValueError('Status must be "success"')
        return v

class ChatRequestWithName(ChatRequest):
    userName: str = None

@router.post("/chat")
async def chat(request: ChatRequestWithName):
    try:
        logger.info(f"Received chat request with query: {request.query[:100]}...")  # Log truncated query
        response = chat_manager.chat(request.query, request.userName)
        logger.info("Chat request processed successfully")
        return {"response": response}
    except HTTPException as he:
        logger.error(f"HTTP error in chat endpoint: {str(he)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}", exc_info=True)  # Include full traceback
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat request: {str(e)}"
        )


@router.post("/summarize")
async def summarize(request: SummarizeRequest):
    try:
        prompt = f"""Your task is to summarize the following text concisely while preserving key information and meaning:

{request.text}

Provide a clear and focused summary."""
        
        summary = chat_manager.chat(prompt)
        if not summary:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate summary"
            )
        return {"summary": summary}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Summarize endpoint error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process summarization request"
        )

@router.post("/scenario")
async def scenario_description(request: DetectionData):
    try:
        # Prepare the prompt with the required instruction text
        scenario_prompt = """You are a helpful and observant visual assistant. A user cannot see the image, so your task is to describe the visible scene clearly and naturally, as if you're standing next to them.

Based on the detected objects from an image, including their labels (e.g., "dog", "car", "bench"), their approximate positions within the frame (e.g., "bottom-left", "centre-right", "top"), and confidence levels, describe the image as a human would — using natural, flowing language that paints a vivid mental picture.

Be descriptive, but do not make assumptions about things that aren't detected. Use spatial relationships and grouping to make the scene feel real.

Imagine you are describing the scene out loud to a visually impaired person, focusing on clarity, simplicity, and imagery.

The detected objects in the image are:
"""
        # Format the detection data for the prompt
        formatted_detections = []
        for object_type, detections in request.detections.items():
            for detection in detections:
                formatted_detections.append(
                    f"- {object_type} at {detection.position} (confidence: {detection.confidence:.2%})"
                )
        
        scenario_text = "\n".join(formatted_detections)
        full_prompt = scenario_prompt + "\n" + scenario_text
        
        # Use the chat manager to generate a response
        response = chat_manager.chat(full_prompt)
        return {"description": response}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Scenario description endpoint error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process scenario description request"
        )