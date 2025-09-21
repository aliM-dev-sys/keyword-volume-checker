# Keyword Volume Checker API Documentation

## Overview

The Keyword Volume Checker API provides endpoints to fetch search volume data for keywords across multiple countries (US, UK, CA, SA). The API is built with FastAPI and provides both REST endpoints and a web dashboard.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

## Authentication

Currently, the API does not require authentication for basic usage. API keys for external services are configured via environment variables.

## Endpoints

### 1. Health Check

**GET** `/health`

Check if the API is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "service": "keyword-volume-checker"
}
```

### 2. Web Dashboard

**GET** `/`

Access the built-in web dashboard for testing and visualization.

**Response:** HTML page with interactive dashboard

### 3. Single Keyword Volume

**GET** `/check-volume`

Get search volume for a single keyword in a specific country.

**Parameters:**
- `keyword` (string, required): The keyword to check
- `country` (string, required): Country code (US, UK, CA, SA)

**Example Request:**
```bash
GET /check-volume?keyword=seo&country=US
```

**Response:**
```json
{
  "keyword": "seo",
  "country": "US",
  "volume": 12000
}
```

**Error Response:**
```json
{
  "detail": "Unsupported country. Must be one of: US, UK, CA, SA"
}
```

### 4. Batch Keyword Volumes

**POST** `/check-batch`

Get search volumes for multiple keywords in a specific country.

**Request Body:**
```json
{
  "keywords": ["seo", "marketing", "digital marketing"],
  "country": "US"
}
```

**Response:**
```json
{
  "country": "US",
  "total_keywords": 3,
  "results": [
    {
      "keyword": "seo",
      "country": "US",
      "volume": 12000
    },
    {
      "keyword": "marketing",
      "country": "US",
      "volume": 8500
    },
    {
      "keyword": "digital marketing",
      "country": "US",
      "volume": 15000
    }
  ]
}
```

### 5. Export CSV

**GET** `/export/csv`

Export keyword volumes as a CSV file.

**Parameters:**
- `keywords` (string, required): Comma-separated list of keywords
- `country` (string, required): Country code (US, UK, CA, SA)

**Example Request:**
```bash
GET /export/csv?keywords=seo,marketing,digital&country=US
```

**Response:** CSV file download

**CSV Format:**
```csv
Keyword,Country,Volume
seo,US,12000
marketing,US,8500
digital,US,15000
```

### 6. Export JSON

**GET** `/export/json`

Export keyword volumes as a JSON file.

**Parameters:**
- `keywords` (string, required): Comma-separated list of keywords
- `country` (string, required): Country code (US, UK, CA, SA)

**Example Request:**
```bash
GET /export/json?keywords=seo,marketing,digital&country=US
```

**Response:** JSON file download

## Country Codes

| Code | Country |
|------|---------|
| US | United States |
| UK | United Kingdom |
| CA | Canada |
| SA | South Africa |

## Error Handling

The API uses standard HTTP status codes:

- `200`: Success
- `400`: Bad Request (invalid parameters)
- `500`: Internal Server Error

Error responses include a `detail` field with the error message:

```json
{
  "detail": "Error message here"
}
```

## Rate Limiting

The API includes built-in rate limiting to prevent abuse:
- Default delay between requests: 0.1 seconds
- Configurable via `API_RATE_LIMIT_DELAY` environment variable

## API Providers

The API is designed to work with multiple keyword data providers:

### DataForSEO (Default)
- Location codes: US=2840, UK=2826, CA=2124, SA=7100
- Authentication: Basic Auth with API key

### Semrush
- Location codes: US=us, UK=uk, CA=ca, SA=za
- Authentication: API key in query parameters

### Ahrefs
- Location codes: US=us, UK=uk, CA=ca, SA=za
- Authentication: Bearer token

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `KEYWORD_API_KEY` | API key for keyword service | `your_api_key_here` |
| `KEYWORD_API_URL` | API endpoint URL | `https://api.example.com/keywords/volume` |
| `API_TIMEOUT` | Request timeout (seconds) | `30` |
| `API_MAX_RETRIES` | Maximum retry attempts | `3` |
| `API_RATE_LIMIT_DELAY` | Delay between requests (seconds) | `0.1` |
| `CACHE_ENABLED` | Enable response caching | `true` |
| `CACHE_TTL` | Cache time-to-live (seconds) | `3600` |

## Usage Examples

### cURL Examples

**Single Keyword:**
```bash
curl "http://localhost:8000/check-volume?keyword=seo&country=US"
```

**Batch Keywords:**
```bash
curl -X POST "http://localhost:8000/check-batch" \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["seo", "marketing"], "country": "US"}'
```

**Export CSV:**
```bash
curl "http://localhost:8000/export/csv?keywords=seo,marketing&country=US" \
  -o volumes.csv
```

### Python Examples

```python
import requests

# Single keyword
response = requests.get(
    "http://localhost:8000/check-volume",
    params={"keyword": "seo", "country": "US"}
)
data = response.json()
print(f"Volume: {data['volume']}")

# Batch keywords
response = requests.post(
    "http://localhost:8000/check-batch",
    json={"keywords": ["seo", "marketing"], "country": "US"}
)
data = response.json()
for result in data['results']:
    print(f"{result['keyword']}: {result['volume']}")
```

### JavaScript Examples

```javascript
// Single keyword
fetch('http://localhost:8000/check-volume?keyword=seo&country=US')
  .then(response => response.json())
  .then(data => console.log(data.volume));

// Batch keywords
fetch('http://localhost:8000/check-batch', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ keywords: ['seo', 'marketing'], country: 'US' })
})
.then(response => response.json())
.then(data => console.log(data.results));
```

## n8n Integration

### HTTP Request Node

1. **URL**: `http://your-server:8000/check-volume`
2. **Method**: `GET`
3. **Query Parameters**:
   - `keyword`: `{{ $json.keyword }}`
   - `country`: `{{ $json.country }}`

### Batch Processing

1. **URL**: `http://your-server:8000/check-batch`
2. **Method**: `POST`
3. **Body** (JSON):
   ```json
   {
     "keywords": "{{ $json.keywords }}",
     "country": "{{ $json.country }}"
   }
   ```

## Monitoring

### Health Check
Monitor the API health with:
```bash
curl http://localhost:8000/health
```

### Metrics
The API provides basic health metrics through the `/health` endpoint.

## Troubleshooting

### Common Issues

1. **"Unsupported country" error**
   - Ensure country code is one of: US, UK, CA, SA

2. **"API request failed" error**
   - Check API key configuration
   - Verify API URL is correct
   - Check network connectivity

3. **Slow responses**
   - Check rate limiting settings
   - Verify API provider status
   - Consider enabling caching

### Debug Mode

Enable debug logging by setting the log level in your environment:
```bash
export LOG_LEVEL=DEBUG
```

## Support

For issues and questions:
- Check the API documentation at `/docs` (Swagger UI)
- Review server logs for error details
- Test with the built-in web dashboard at `/`
