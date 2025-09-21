# Coolify Deployment Guide

This guide shows you how to deploy the Keyword Volume Checker using Coolify, avoiding port conflicts with your existing Coolify installation.

## Prerequisites

- Coolify running on port 8000
- Docker and Docker Compose installed
- Git repository access

## Deployment Options

### Option 1: Deploy as Coolify Service

Since you already have Coolify running on port 8000, you can deploy the Keyword Volume Checker as a new service in Coolify:

1. **Create New Service in Coolify**
   - Go to your Coolify dashboard
   - Click "New Service"
   - Choose "Docker Compose" or "Dockerfile"

2. **Configure Service**
   - **Name**: `keyword-volume-checker`
   - **Port**: `8001` (to avoid conflict with Coolify on 8000)
   - **Environment Variables**: Use the values from `env.example`

3. **Deploy**
   - Coolify will build and deploy the service
   - Access at: `http://your-server:8001`

### Option 2: Manual Docker Deployment

If you prefer to deploy manually alongside Coolify:

1. **Clone and Setup**
   ```bash
   git clone <your-repo>
   cd keyword-volume-checker
   cp env.example .env
   ```

2. **Deploy with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Access the Service**
   - Web Dashboard: `http://your-server:8001`
   - API Documentation: `http://localhost:8001/docs`

### Option 3: Use Different Port

If you want to use a different port, update the `docker-compose.yml`:

```yaml
services:
  keyword-volume-checker:
    build: .
    ports:
      - "YOUR_PORT:8000"  # Change YOUR_PORT to desired port
    # ... rest of configuration
```

## Coolify Integration

### 1. Add to Coolify Services

1. **Create New Project**
   - In Coolify, create a new project
   - Choose "Docker Compose" as the source

2. **Configure Environment**
   ```yaml
   # Add these environment variables in Coolify
   GOOGLE_TRENDS_ENABLED=true
   GOOGLE_TRENDS_TIMEOUT=10
   GOOGLE_TRENDS_DELAY=1.0
   AMAZON_AUTOCOMPLETE_ENABLED=true
   AMAZON_AUTOCOMPLETE_TIMEOUT=10
   AMAZON_AUTOCOMPLETE_DELAY=0.5
   CACHE_ENABLED=true
   CACHE_TTL=86400
   ```

3. **Set Port Mapping**
   - **Host Port**: `8001` (or your preferred port)
   - **Container Port**: `8000`

### 2. Domain Configuration

If you want to use a custom domain:

1. **Add Domain in Coolify**
   - Go to your service settings
   - Add custom domain: `keyword-checker.yourdomain.com`
   - Coolify will handle SSL automatically

2. **Update n8n Integration**
   - Use the custom domain instead of IP:port
   - Example: `https://keyword-checker.yourdomain.com/check-volume`

## Environment Variables

Create these environment variables in Coolify:

| Variable | Value | Description |
|----------|-------|-------------|
| `GOOGLE_TRENDS_ENABLED` | `true` | Enable Google Trends data source |
| `GOOGLE_TRENDS_TIMEOUT` | `10` | Google Trends request timeout |
| `GOOGLE_TRENDS_DELAY` | `1.0` | Delay between Google Trends requests |
| `AMAZON_AUTOCOMPLETE_ENABLED` | `true` | Enable Amazon autocomplete data source |
| `AMAZON_AUTOCOMPLETE_TIMEOUT` | `10` | Amazon autocomplete request timeout |
| `AMAZON_AUTOCOMPLETE_DELAY` | `0.5` | Delay between Amazon requests |
| `CACHE_ENABLED` | `true` | Enable response caching |
| `CACHE_TTL` | `86400` | Cache time-to-live (24 hours) |

## n8n Integration with Coolify

### 1. Internal Network Access

If both services are in the same Coolify network:

```bash
# Use service name instead of localhost
curl "http://keyword-volume-checker:8000/check-volume?keyword=seo&country=US"
```

### 2. External Access

If accessing from outside Coolify:

```bash
# Use your server IP and port
curl "http://your-server-ip:8001/check-volume?keyword=seo&country=US"
```

### 3. Custom Domain Access

If using a custom domain:

```bash
# Use your custom domain
curl "https://keyword-checker.yourdomain.com/check-volume?keyword=seo&country=US"
```

## Monitoring and Management

### 1. Health Checks

Coolify will automatically monitor the service health:

- **Health Check URL**: `http://keyword-volume-checker:8000/health`
- **Check Interval**: Every 30 seconds (configurable)

### 2. Logs

View logs in Coolify:
- Go to your service
- Click "Logs" tab
- View real-time logs

### 3. Restart and Updates

- **Restart**: Use Coolify's restart button
- **Update**: Push new code to trigger rebuild
- **Scale**: Adjust resources in Coolify settings

## Troubleshooting

### Common Issues

1. **Port Conflict**
   - Ensure you're using port 8001 (or another available port)
   - Check Coolify's port usage in settings

2. **Service Not Starting**
   - Check logs in Coolify
   - Verify environment variables
   - Ensure Docker has enough resources

3. **Network Issues**
   - Check if services can communicate
   - Verify firewall settings
   - Test with internal network names

### Debug Commands

```bash
# Check if service is running
docker ps | grep keyword-volume-checker

# View logs
docker logs keyword-volume-checker

# Test API
curl http://localhost:8001/health

# Check environment variables
docker exec keyword-volume-checker env | grep -E "(GOOGLE|AMAZON|CACHE)"
```

## Performance Optimization

### 1. Resource Allocation

In Coolify, allocate appropriate resources:
- **CPU**: 0.5-1 vCPU
- **Memory**: 512MB-1GB
- **Storage**: 1-2GB for cache

### 2. Caching

The service includes built-in caching:
- **SQLite Database**: Stored in `/app/data/`
- **TTL**: 24 hours (configurable)
- **Persistence**: Data survives container restarts

### 3. Scaling

For high traffic:
- **Horizontal Scaling**: Deploy multiple instances
- **Load Balancer**: Use Coolify's load balancing
- **Database**: Consider external database for cache

## Security Considerations

### 1. Network Security

- **Internal Access**: Use Coolify's internal network
- **External Access**: Use custom domain with SSL
- **Firewall**: Restrict access to necessary ports only

### 2. Data Privacy

- **No External APIs**: Service uses only open-source data
- **Local Storage**: All data stays on your server
- **No API Keys**: No sensitive credentials required

### 3. Updates

- **Regular Updates**: Keep the service updated
- **Security Patches**: Monitor for security updates
- **Backup**: Regular backup of cache data

## Backup and Recovery

### 1. Data Backup

```bash
# Backup cache database
docker cp keyword-volume-checker:/app/data/keyword_volumes.db ./backup/

# Backup configuration
docker cp keyword-volume-checker:/app/.env ./backup/
```

### 2. Recovery

```bash
# Restore cache database
docker cp ./backup/keyword_volumes.db keyword-volume-checker:/app/data/

# Restart service
docker-compose restart
```

## Support

For issues with Coolify deployment:
1. Check Coolify logs and documentation
2. Verify Docker and Docker Compose installation
3. Test service independently of Coolify
4. Check network connectivity and port availability

For Keyword Volume Checker issues:
1. Check service logs in Coolify
2. Test API endpoints directly
3. Verify environment variables
4. Check resource allocation
