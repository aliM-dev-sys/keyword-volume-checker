# Endpoint Compatibility Guide

This document explains how both the dashboard and n8n endpoints handle the same keyword input format.

## Input Format

Both endpoints accept the same keyword array format:

```json
{
  "keywords": [
    "IPTV restream business models US entrepreneurs",
    "Monetization strategies IPTV streaming US",
    "IPTV service revenue generation US",
    "Launching IPTV restream platform US",
    "Subscription video on demand business US"
  ]
}
```

## Dashboard Endpoint: `/check-batch`

**Method:** POST  
**Content-Type:** application/json

### Request Format:
```json
{
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "country": "US",
  "method": "combined"
}
```

### Response Format:
```json
{
  "country": "US",
  "method": "combined",
  "total_keywords": 3,
  "results": [
    {
      "keyword": "keyword1",
      "country": "US",
      "volume": 8500
    },
    {
      "keyword": "keyword2", 
      "country": "US",
      "volume": 12000
    }
  ]
}
```

## N8N Endpoint: `/n8n/check-keywords`

**Method:** POST  
**Content-Type:** application/json

### Request Format (Direct Object):
```json
{
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "geo": "US",
  "method": "combined"
}
```

### Request Format (Array/Webhook):
```json
[
  {
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "geo": "US", 
    "method": "combined"
  }
]
```

### Response Format:
```json
{
  "success": true,
  "country": "US",
  "method": "combined",
  "total_keywords": 3,
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "results": [
    {
      "keyword": "keyword1",
      "country": "US",
      "volume": 8500
    }
  ],
  "timestamp": "2025-01-21T10:30:00.000Z"
}
```

## Key Differences

1. **Country Parameter:**
   - Dashboard: `"country": "US"`
   - N8N: `"geo": "US"`

2. **Response Format:**
   - Dashboard: Simple response with results
   - N8N: Extended response with success flag, keywords array, and timestamp

3. **Input Flexibility:**
   - Dashboard: Only accepts direct object format
   - N8N: Accepts both direct object and array format (for webhooks)

## Usage Examples

### Dashboard JavaScript:
```javascript
fetch('/check-batch', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
        keywords: keywords, 
        country: country 
    })
})
```

### N8N HTTP Request Node:
```json
{
  "keywords": ["keyword1", "keyword2"],
  "geo": "US",
  "method": "combined"
}
```

### cURL Examples:

**Dashboard:**
```bash
curl -X POST "http://your-server:8001/check-batch" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["keyword1", "keyword2"],
    "country": "US"
  }'
```

**N8N:**
```bash
curl -X POST "http://your-server:8001/n8n/check-keywords" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["keyword1", "keyword2"],
    "geo": "US"
  }'
```

## Error Handling

Both endpoints return the same error format:
```json
{
  "detail": "Error message here"
}
```

Common error codes:
- `400`: Bad Request (invalid input)
- `500`: Internal Server Error
