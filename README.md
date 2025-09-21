# Keyword Volume Checker

A lightweight, **completely self-hosted** FastAPI service that estimates keyword search volumes for **US, UK, CA, SA** using open-source data sources. No external API dependencies required! Designed to be deployed with Docker and integrated into n8n workflows or used as a standalone microservice.

## 🚀 Features

- **100% Self-Hosted**: No external API dependencies or API keys required
- **Open-Source Data Sources**: Uses Google Trends and Amazon autocomplete data
- **Multiple Estimation Methods**: Combined, Google Trends, Amazon autocomplete, or fallback
- **Single & Batch Processing**: Check one keyword or multiple keywords at once
- **Multi-Country Support**: US, UK, Canada, South Africa
- **Export Options**: CSV and JSON export functionality
- **Web Dashboard**: Built-in web interface for testing and visualization
- **Docker Ready**: Containerized for easy deployment
- **Intelligent Caching**: SQLite-based caching with 24-hour TTL
- **Rate Limiting**: Built-in rate limiting and retry logic
- **Health Checks**: Monitoring endpoints for production use

## 📁 Project Structure

```
keyword-volume-checker/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── services.py      # Keyword API logic
│   └── config.py        # Configuration and settings
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
└── README.md           # This file
```

## 🛠️ Quick Start

### Local Development

1. **Clone and setup**:
   ```bash
   git clone <your-repo>
   cd keyword-volume-checker
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access the dashboard**: http://localhost:8000

### Docker Deployment

1. **Build the image**:
   ```bash
   docker build -t keyword-volume-checker .
   ```

2. **Run the container**:
   ```bash
   docker run -d -p 8000:8000 \
     -e KEYWORD_API_KEY=your_api_key \
     -e KEYWORD_API_URL=https://api.example.com/keywords/volume \
     --name keyword-checker \
     keyword-volume-checker
   ```

3. **Access the service**: http://localhost:8000

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_TRENDS_ENABLED` | Enable Google Trends data source | `true` |
| `GOOGLE_TRENDS_TIMEOUT` | Google Trends request timeout | `10` |
| `GOOGLE_TRENDS_DELAY` | Delay between Google Trends requests | `1.0` |
| `AMAZON_AUTOCOMPLETE_ENABLED` | Enable Amazon autocomplete data source | `true` |
| `AMAZON_AUTOCOMPLETE_TIMEOUT` | Amazon autocomplete request timeout | `10` |
| `AMAZON_AUTOCOMPLETE_DELAY` | Delay between Amazon requests | `0.5` |
| `API_TIMEOUT` | General request timeout in seconds | `30` |
| `API_MAX_RETRIES` | Maximum retry attempts | `3` |
| `API_RATE_LIMIT_DELAY` | Delay between requests in seconds | `0.1` |
| `CACHE_ENABLED` | Enable response caching | `true` |
| `CACHE_TTL` | Cache time-to-live in seconds | `86400` (24 hours) |

### Data Source Configuration

The service uses open-source data sources that don't require API keys:

- **Google Trends**: Estimates volume based on search trend data
- **Amazon Autocomplete**: Uses Amazon's autocomplete API for volume estimation
- **Combined Method**: Averages results from multiple sources for better accuracy
- **Fallback Method**: Uses keyword analysis patterns when external sources fail

All data sources are enabled by default and can be configured via environment variables.

## 📚 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web dashboard |
| `GET` | `/check-volume` | Check single keyword volume |
| `POST` | `/check-batch` | Check multiple keyword volumes |
| `GET` | `/export/csv` | Export results as CSV |
| `GET` | `/export/json` | Export results as JSON |
| `GET` | `/methods` | Get available estimation methods |
| `POST` | `/cache/clear` | Clear keyword volume cache |
| `GET` | `/health` | Health check |

### Usage Examples

#### Single Keyword Check
```bash
curl "http://localhost:8001/check-volume?keyword=seo&country=US&method=combined"
```

Response:
```json
{
  "keyword": "seo",
  "country": "US",
  "volume": 12000,
  "method": "combined"
}
```

#### Batch Keywords Check
```bash
curl -X POST "http://localhost:8001/check-batch" \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["seo", "marketing", "digital"], "country": "US", "method": "combined"}'
```

Response:
```json
{
  "country": "US",
  "method": "combined",
  "total_keywords": 3,
  "results": [
    {"keyword": "seo", "country": "US", "volume": 12000},
    {"keyword": "marketing", "country": "US", "volume": 8500},
    {"keyword": "digital", "country": "US", "volume": 15000}
  ]
}
```

#### Export CSV
```bash
curl "http://localhost:8001/export/csv?keywords=seo,marketing,digital&country=US&method=combined" \
  -o keyword-volumes.csv
```

#### Export JSON
```bash
curl "http://localhost:8001/export/json?keywords=seo,marketing,digital&country=US&method=combined" \
  -o keyword-volumes.json
```

#### Get Available Methods
```bash
curl "http://localhost:8001/methods"
```

#### Clear Cache
```bash
curl -X POST "http://localhost:8001/cache/clear"
```

## 🌐 Web Dashboard

The built-in web dashboard provides:

- **Single keyword testing**: Enter a keyword and country to get instant results
- **Batch processing**: Upload multiple keywords for bulk analysis
- **Export functionality**: Download results as CSV or JSON
- **Real-time results**: See results immediately in the browser

Access the dashboard at: http://localhost:8001

## 🔌 n8n Integration

### HTTP Request Node Configuration

1. **URL**: `http://your-server:8000/check-volume`
2. **Method**: `GET`
3. **Query Parameters**:
   - `keyword`: The keyword to check
   - `country`: Country code (US, UK, CA, SA)

### Batch Processing in n8n

1. **URL**: `http://your-server:8000/check-batch`
2. **Method**: `POST`
3. **Body** (JSON):
   ```json
   {
     "keywords": ["keyword1", "keyword2", "keyword3"],
     "country": "US"
   }
   ```

## 🚀 Production Deployment

### Docker Compose

```yaml
version: '3.8'
services:
  keyword-checker:
    build: .
    ports:
      - "8000:8000"
    environment:
      - KEYWORD_API_KEY=your_actual_api_key
      - KEYWORD_API_URL=https://api.your-provider.com/endpoint
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Coolify Deployment

1. Connect your Git repository to Coolify
2. Set environment variables in Coolify dashboard
3. Deploy with one click

## 🔧 Customization

### Adding New API Providers

1. Update `app/config.py` with new provider mappings
2. Add provider method in `app/services.py`
3. Update the provider selection logic

### Adding New Countries

1. Add country code to `SUPPORTED_COUNTRIES` in `config.py`
2. Add location mappings for each provider
3. Update validation logic

## 📊 Performance

- **Memory Usage**: ~50-100MB typical usage
- **CPU Usage**: Low, suitable for 2 vCPU servers
- **Response Time**: <2 seconds per keyword (depending on API provider)
- **Concurrent Requests**: Supports multiple simultaneous requests

## 🛡️ Security

- Non-root user in Docker container
- Input validation and sanitization
- Rate limiting to prevent abuse
- Error handling without sensitive data exposure

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the API documentation at `/docs` (Swagger UI)
- Review the health check endpoint at `/health`
