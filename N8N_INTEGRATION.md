# n8n Integration Guide

This guide shows you how to integrate the Keyword Volume Checker with n8n workflows using HTTP Request nodes.

## Prerequisites

- n8n instance running
- Keyword Volume Checker deployed and accessible
- Basic knowledge of n8n workflows

## Quick Start

### 1. Basic Single Keyword Check

**Node Configuration:**
- **Node Type**: HTTP Request
- **Method**: GET
- **URL**: `http://your-server:8001/check-volume`
- **Query Parameters**:
  - `keyword`: `{{ $json.keyword }}`
  - `country`: `{{ $json.country }}`
  - `method`: `combined` (optional)

**Example Input Data:**
```json
{
  "keyword": "seo tools",
  "country": "US"
}
```

**Expected Output:**
```json
{
  "keyword": "seo tools",
  "country": "US",
  "volume": 8500,
  "method": "combined"
}
```

### 2. Batch Keyword Processing

**Node Configuration:**
- **Node Type**: HTTP Request
- **Method**: POST
- **URL**: `http://your-server:8001/check-batch`
- **Headers**:
  - `Content-Type`: `application/json`
- **Body** (JSON):
```json
{
  "keywords": ["seo", "marketing", "digital marketing"],
  "country": "US",
  "method": "combined"
}
```

**Expected Output:**
```json
{
  "country": "US",
  "method": "combined",
  "total_keywords": 3,
  "results": [
    {"keyword": "seo", "country": "US", "volume": 12000},
    {"keyword": "marketing", "country": "US", "volume": 8500},
    {"keyword": "digital marketing", "country": "US", "volume": 15000}
  ]
}
```

## Advanced Workflows

### 1. Keyword Research Workflow

**Workflow Steps:**
1. **Manual Trigger** - Start the workflow
2. **Set** - Define keywords to research
3. **HTTP Request** - Check volumes for each keyword
4. **Filter** - Filter keywords by volume threshold
5. **Google Sheets** - Save results to spreadsheet

**Node Configuration:**

**Set Node:**
```json
{
  "keywords": ["seo tools", "marketing automation", "content management"],
  "countries": ["US", "UK", "CA"],
  "min_volume": 1000
}
```

**HTTP Request Node (in Loop):**
- **URL**: `http://your-server:8001/check-volume`
- **Query Parameters**:
  - `keyword`: `{{ $json.keyword }}`
  - `country`: `{{ $json.country }}`

**Filter Node:**
- **Condition**: `{{ $json.volume }} >= {{ $('Set').item.json.min_volume }}`

### 2. Competitor Analysis Workflow

**Workflow Steps:**
1. **Webhook** - Receive competitor domain
2. **Code** - Extract keywords from competitor site
3. **HTTP Request** - Check volumes for extracted keywords
4. **Sort** - Sort by volume (descending)
5. **Slack** - Send top keywords to team

**Code Node (Extract Keywords):**
```javascript
// Simple keyword extraction (replace with your preferred method)
const keywords = [
  "seo optimization",
  "digital marketing",
  "content strategy",
  "social media marketing"
];

return keywords.map(keyword => ({ keyword }));
```

**HTTP Request Node:**
- **URL**: `http://your-server:8001/check-batch`
- **Method**: POST
- **Body**:
```json
{
  "keywords": "{{ $json.keyword }}",
  "country": "US"
}
```

### 3. Content Planning Workflow

**Workflow Steps:**
1. **Schedule Trigger** - Run weekly
2. **Google Sheets** - Read content ideas
3. **HTTP Request** - Check keyword volumes
4. **Filter** - Select high-volume keywords
5. **Notion** - Create content calendar entries

**Google Sheets Node:**
- **Operation**: Read
- **Range**: `A:A` (assuming keywords are in column A)

**HTTP Request Node:**
- **URL**: `http://your-server:8001/check-batch`
- **Method**: POST
- **Body**:
```json
{
  "keywords": "{{ $json.keywords }}",
  "country": "US",
  "method": "combined"
}
```

## Error Handling

### 1. Retry Logic

**HTTP Request Node Settings:**
- **Retry**: Enable
- **Max Retries**: 3
- **Retry Delay**: 1000ms

### 2. Error Response Handling

**Code Node (After HTTP Request):**
```javascript
// Check if the request was successful
if ($input.statusCode === 200) {
  return $input.json;
} else {
  // Log error and return default values
  console.log('Error:', $input.statusCode, $input.json);
  return {
    keyword: $('Previous Node').item.json.keyword,
    country: $('Previous Node').item.json.country,
    volume: 0,
    error: 'API request failed'
  };
}
```

## Performance Optimization

### 1. Batch Processing

Instead of making individual requests for each keyword, use the batch endpoint:

**Before (Inefficient):**
- 10 keywords = 10 HTTP requests

**After (Efficient):**
- 10 keywords = 1 HTTP request

### 2. Caching

The Keyword Volume Checker caches results for 24 hours. If you're processing the same keywords frequently, consider:

1. **Check cache first** using a simple HTTP request
2. **Only process new keywords** that aren't cached
3. **Use the cache/clear endpoint** to refresh data when needed

### 3. Rate Limiting

The service includes built-in rate limiting. For high-volume processing:

1. **Add delays** between requests
2. **Use batch processing** when possible
3. **Consider running multiple instances** behind a load balancer

## Monitoring and Alerts

### 1. Health Check Monitoring

**HTTP Request Node:**
- **URL**: `http://your-server:8001/health`
- **Schedule**: Every 5 minutes
- **Alert**: If status is not "healthy"

### 2. Performance Monitoring

**Code Node (After HTTP Request):**
```javascript
// Log performance metrics
const responseTime = Date.now() - $('HTTP Request').item.json.timestamp;
console.log(`Response time: ${responseTime}ms`);

// Alert if response time is too high
if (responseTime > 5000) {
  // Send alert to Slack/Email
}
```

## Common Use Cases

### 1. SEO Content Planning
- Research keywords for blog posts
- Identify trending topics
- Plan content calendar based on search volume

### 2. PPC Campaign Planning
- Research high-volume keywords for ad campaigns
- Identify keyword opportunities
- Analyze competitor keyword strategies

### 3. Market Research
- Understand search trends in different countries
- Identify seasonal keyword patterns
- Research industry-specific keywords

### 4. Content Optimization
- Find related keywords for existing content
- Identify keyword gaps
- Optimize content for better search visibility

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Check if the service is running
   - Verify the URL and port
   - Check firewall settings

2. **Timeout Errors**
   - Increase timeout in HTTP Request node
   - Check server performance
   - Consider using fallback method

3. **Rate Limiting**
   - Add delays between requests
   - Use batch processing
   - Check rate limit settings

### Debug Tips

1. **Enable Debug Mode** in n8n
2. **Check Logs** in the Keyword Volume Checker
3. **Test API Endpoints** directly with curl
4. **Monitor Response Times** and error rates

## Example Workflow JSON

Here's a complete n8n workflow for keyword research:

```json
{
  "name": "Keyword Research Workflow",
  "nodes": [
    {
      "parameters": {
        "values": {
          "string": [
            {
              "name": "keywords",
              "value": "seo tools,marketing automation,content management"
            },
            {
              "name": "country",
              "value": "US"
            }
          ]
        }
      },
      "name": "Set Keywords",
      "type": "n8n-nodes-base.set"
    },
    {
      "parameters": {
        "url": "http://your-server:8001/check-batch",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "keywords",
              "value": "={{ $json.keywords.split(',') }}"
            },
            {
              "name": "country",
              "value": "={{ $json.country }}"
            },
            {
              "name": "method",
              "value": "combined"
            }
          ]
        }
      },
      "name": "Check Keyword Volumes",
      "type": "n8n-nodes-base.httpRequest"
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.volume }}",
              "operation": "larger",
              "value2": 1000
            }
          ]
        }
      },
      "name": "Filter High Volume",
      "type": "n8n-nodes-base.filter"
    }
  ],
  "connections": {
    "Set Keywords": {
      "main": [
        [
          {
            "node": "Check Keyword Volumes",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Check Keyword Volumes": {
      "main": [
        [
          {
            "node": "Filter High Volume",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

## Support

For issues with the Keyword Volume Checker:
1. Check the service logs: `docker-compose logs`
2. Test the API directly: `curl http://localhost:8001/health`
3. Check the service status: `docker-compose ps`

For n8n integration issues:
1. Check n8n execution logs
2. Test HTTP requests manually
3. Verify node configurations
