# Configuration Guide

## Initial Setup

1. Update desk_booking_config.yaml with your environment details
2. Set database credentials via environment variables
3. Configure notification channels (email, Slack, etc.)

## Database Setup

Run the database initialization script:
```bash
psql -U admin -d desk_booking_db -f config/database_setup.sql
```

## Email Notifications

Configure email settings in config file:
- SMTP server
- Sender address
- Email templates

## Slack Integration

1. Create a Slack app
2. Add bot token to configuration
3. Set channel for notifications

## Performance Tuning

- Adjust database pool size based on user count
- Configure caching for analytics
- Set appropriate timeouts

## Security

- Use strong database passwords
- Enable SSL for all connections
- Restrict API access with tokens
- Enable audit logging
