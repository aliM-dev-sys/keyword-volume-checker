from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import json
import csv
import io
from datetime import datetime
from app.services import get_keyword_volume, get_batch_keyword_volume, get_method_info, clear_cache
from app.config import SUPPORTED_COUNTRIES

app = FastAPI(
    title="Keyword Volume Checker",
    description="Lightweight API to fetch keyword search volume for US, UK, CA, SA",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Simple web dashboard for testing the API"""
    return FileResponse("app/static/dashboard.html")

@app.get("/check-volume")
def check_volume(
    keyword: str = Query(..., description="Keyword to check"),
    country: str = Query(..., description="Country code (US, UK, CA, SA)"),
    method: str = Query("combined", description="Estimation method (combined, google_trends, amazon_autocomplete, fallback)")
):
    """
    Returns keyword search volume for a specific country using open-source methods.
    """
    if country not in SUPPORTED_COUNTRIES:
        raise HTTPException(status_code=400, detail=f"Unsupported country. Must be one of: {', '.join(SUPPORTED_COUNTRIES)}")
    
    try:
        volume = get_keyword_volume(keyword, country, method)
        return {
            "keyword": keyword,
            "country": country,
            "volume": volume,
            "method": method
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/check-batch")
def check_batch_volume(request: dict):
    """
    Returns keyword search volumes for multiple keywords in a specific country.
    """
    try:
        # Extract data from request body
        keywords = request.get("keywords", [])
        country = request.get("country", "US")
        method = request.get("method", "combined")
        
        if country not in SUPPORTED_COUNTRIES:
            raise HTTPException(status_code=400, detail=f"Unsupported country. Must be one of: {', '.join(SUPPORTED_COUNTRIES)}")
        
        if not keywords or len(keywords) == 0:
            raise HTTPException(status_code=400, detail="At least one keyword is required")
        
        # Clean and validate keywords
        cleaned_keywords = [k.strip() for k in keywords if k.strip()]
        if not cleaned_keywords:
            raise HTTPException(status_code=400, detail="No valid keywords provided")
        
        results = get_batch_keyword_volume(cleaned_keywords, country, method)
        return {
            "country": country,
            "method": method,
            "total_keywords": len(cleaned_keywords),
            "results": results
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/n8n/check-keywords")
def n8n_check_keywords(request: dict):
    """
    N8N-specific endpoint that handles the webhook format from n8n.
    Expects: { "keywords": [...], "geo": "US", "method": "combined" }
    """
    try:
        # Extract data from n8n webhook format
        if isinstance(request, list) and len(request) > 0:
            # Handle array format (webhook data)
            data = request[0]
        else:
            # Handle direct object format
            data = request
        
        # Extract keywords and geo
        keywords = data.get("keywords", [])
        geo = data.get("geo", "US")
        method = data.get("method", "combined")
        
        # Validate geo (convert to supported format if needed)
        geo_mapping = {
            "US": "US",
            "UK": "UK", 
            "CA": "CA",
            "SA": "SA",
            "United States": "US",
            "United Kingdom": "UK",
            "Canada": "CA",
            "South Africa": "SA"
        }
        
        country = geo_mapping.get(geo, geo.upper())
        
        if country not in SUPPORTED_COUNTRIES:
            raise HTTPException(status_code=400, detail=f"Unsupported geo '{geo}'. Must be one of: {', '.join(SUPPORTED_COUNTRIES)}")
        
        if not keywords or len(keywords) == 0:
            raise HTTPException(status_code=400, detail="No keywords provided")
        
        # Clean and validate keywords
        cleaned_keywords = [k.strip() for k in keywords if k.strip()]
        if not cleaned_keywords:
            raise HTTPException(status_code=400, detail="No valid keywords provided")
        
        # Get keyword volumes
        results = get_batch_keyword_volume(cleaned_keywords, country, method)
        
        # Return in n8n-friendly format
        return {
            "success": True,
            "country": country,
            "method": method,
            "total_keywords": len(cleaned_keywords),
            "keywords": cleaned_keywords,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/export/csv")
def export_csv(
    keywords: str = Query(..., description="Comma-separated keywords"),
    country: str = Query(..., description="Country code (US, UK, CA, SA)"),
    method: str = Query("combined", description="Estimation method")
):
    """
    Export keyword volumes as CSV file.
    """
    if country not in SUPPORTED_COUNTRIES:
        raise HTTPException(status_code=400, detail=f"Unsupported country. Must be one of: {', '.join(SUPPORTED_COUNTRIES)}")
    
    keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
    if not keyword_list:
        raise HTTPException(status_code=400, detail="At least one keyword is required")
    
    try:
        results = get_batch_keyword_volume(keyword_list, country, method)
        
        # Create CSV content
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Keyword', 'Country', 'Volume', 'Method'])
        for result in results:
            writer.writerow([result['keyword'], result['country'], result['volume'], method])
        
        csv_content = output.getvalue()
        output.close()
        
        return FileResponse(
            io.BytesIO(csv_content.encode('utf-8')),
            media_type='text/csv',
            filename=f'keyword-volumes-{country.lower()}-{method}.csv'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export/json")
def export_json(
    keywords: str = Query(..., description="Comma-separated keywords"),
    country: str = Query(..., description="Country code (US, UK, CA, SA)"),
    method: str = Query("combined", description="Estimation method")
):
    """
    Export keyword volumes as JSON file.
    """
    if country not in SUPPORTED_COUNTRIES:
        raise HTTPException(status_code=400, detail=f"Unsupported country. Must be one of: {', '.join(SUPPORTED_COUNTRIES)}")
    
    keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
    if not keyword_list:
        raise HTTPException(status_code=400, detail="At least one keyword is required")
    
    try:
        results = get_batch_keyword_volume(keyword_list, country, method)
        
        json_content = json.dumps({
            "country": country,
            "method": method,
            "total_keywords": len(results),
            "results": results
        }, indent=2)
        
        return FileResponse(
            io.BytesIO(json_content.encode('utf-8')),
            media_type='application/json',
            filename=f'keyword-volumes-{country.lower()}-{method}.json'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/methods")
def get_methods():
    """Get information about available estimation methods"""
    return get_method_info()

@app.post("/cache/clear")
def clear_cache_endpoint():
    """Clear the keyword volume cache"""
    try:
        success = clear_cache()
        if success:
            return {"message": "Cache cleared successfully"}
        else:
            return {"message": "No cache to clear"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "keyword-volume-checker"}

@app.post("/n8n/test")
def n8n_test(request: dict):
    """
    Test endpoint to debug n8n input format
    """
    return {
        "received_data": request,
        "data_type": type(request).__name__,
        "keys": list(request.keys()) if isinstance(request, dict) else "Not a dict",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
