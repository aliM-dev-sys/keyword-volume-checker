from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from typing import List
import json
import csv
import io
from app.services import get_keyword_volume, get_batch_keyword_volume, get_method_info, clear_cache
from app.config import SUPPORTED_COUNTRIES

app = FastAPI(
    title="Keyword Volume Checker",
    description="Lightweight API to fetch keyword search volume for US, UK, CA, SA",
    version="1.0.0"
)

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Simple web dashboard for testing the API"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Keyword Volume Checker</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { background: #f5f5f5; padding: 20px; border-radius: 8px; }
            input, select, button { padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; }
            button { background: #007bff; color: white; cursor: pointer; }
            button:hover { background: #0056b3; }
            .result { margin-top: 20px; padding: 15px; background: white; border-radius: 4px; }
            .error { color: red; }
            .success { color: green; }
            .batch-input { width: 100%; height: 100px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 Keyword Volume Checker</h1>
            
            <h3>Single Keyword Check</h3>
            <input type="text" id="keyword" placeholder="Enter keyword" />
            <select id="country">
                <option value="US">United States</option>
                <option value="UK">United Kingdom</option>
                <option value="CA">Canada</option>
                <option value="SA">South Africa</option>
            </select>
            <button onclick="checkSingle()">Check Volume</button>
            
            <h3>Batch Keywords Check</h3>
            <textarea id="keywords" class="batch-input" placeholder="Enter keywords separated by new lines"></textarea>
            <select id="batchCountry">
                <option value="US">United States</option>
                <option value="UK">United Kingdom</option>
                <option value="CA">Canada</option>
                <option value="SA">South Africa</option>
            </select>
            <button onclick="checkBatch()">Check All</button>
            <button onclick="exportCSV()">Export CSV</button>
            <button onclick="exportJSON()">Export JSON</button>
            
            <div id="result" class="result" style="display: none;"></div>
        </div>

        <script>
            let lastResults = [];
            
            async function checkSingle() {
                const keyword = document.getElementById('keyword').value;
                const country = document.getElementById('country').value;
                
                if (!keyword) {
                    showResult('Please enter a keyword', 'error');
                    return;
                }
                
                try {
                    const response = await fetch(`/check-volume?keyword=${encodeURIComponent(keyword)}&country=${country}`);
                    const data = await response.json();
                    
                    if (data.error) {
                        showResult(`Error: ${data.error}`, 'error');
                    } else {
                        showResult(`Keyword: ${data.keyword}<br>Country: ${data.country}<br>Volume: ${data.volume.toLocaleString()}`, 'success');
                    }
                } catch (error) {
                    showResult(`Error: ${error.message}`, 'error');
                }
            }
            
            async function checkBatch() {
                const keywords = document.getElementById('keywords').value.split('\\n').filter(k => k.trim());
                const country = document.getElementById('batchCountry').value;
                
                if (keywords.length === 0) {
                    showResult('Please enter at least one keyword', 'error');
                    return;
                }
                
                try {
                    const response = await fetch('/check-batch', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ keywords, country })
                    });
                    const data = await response.json();
                    
                    if (data.error) {
                        showResult(`Error: ${data.error}`, 'error');
                    } else {
                        lastResults = data.results;
                        let html = '<h4>Results:</h4><table border="1" style="width: 100%; border-collapse: collapse;"><tr><th>Keyword</th><th>Volume</th></tr>';
                        data.results.forEach(result => {
                            html += `<tr><td>${result.keyword}</td><td>${result.volume.toLocaleString()}</td></tr>`;
                        });
                        html += '</table>';
                        showResult(html, 'success');
                    }
                } catch (error) {
                    showResult(`Error: ${error.message}`, 'error');
                }
            }
            
            function exportCSV() {
                if (lastResults.length === 0) {
                    showResult('No results to export. Please run a batch check first.', 'error');
                    return;
                }
                
                const csv = 'Keyword,Volume\\n' + lastResults.map(r => `${r.keyword},${r.volume}`).join('\\n');
                downloadFile(csv, 'keyword-volumes.csv', 'text/csv');
            }
            
            function exportJSON() {
                if (lastResults.length === 0) {
                    showResult('No results to export. Please run a batch check first.', 'error');
                    return;
                }
                
                const json = JSON.stringify(lastResults, null, 2);
                downloadFile(json, 'keyword-volumes.json', 'application/json');
            }
            
            function downloadFile(content, filename, type) {
                const blob = new Blob([content], { type });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                a.click();
                URL.revokeObjectURL(url);
            }
            
            function showResult(message, type) {
                const result = document.getElementById('result');
                result.innerHTML = message;
                result.className = `result ${type}`;
                result.style.display = 'block';
            }
        </script>
    </body>
    </html>
    """

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
def check_batch_volume(
    keywords: List[str],
    country: str,
    method: str = "combined"
):
    """
    Returns keyword search volumes for multiple keywords in a specific country.
    """
    if country not in SUPPORTED_COUNTRIES:
        raise HTTPException(status_code=400, detail=f"Unsupported country. Must be one of: {', '.join(SUPPORTED_COUNTRIES)}")
    
    if not keywords or len(keywords) == 0:
        raise HTTPException(status_code=400, detail="At least one keyword is required")
    
    try:
        results = get_batch_keyword_volume(keywords, country, method)
        return {
            "country": country,
            "method": method,
            "total_keywords": len(keywords),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
