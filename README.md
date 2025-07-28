# E-commerce Platform

A modern e-commerce platform built with Flask and MySQL, fully containerized with Docker for easy deployment and development.

## 🚀 Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- Git (for cloning the repository)

### One-Command Setup
```bash
# Clone and setup the entire application
git clone <repository-url>
cd e-commerce
make setup
```

### Manual Setup
```bash
# 1. Copy environment configuration
cp .env.docker .env

# 2. Build and start containers
docker-compose up -d

# 3. Wait for containers to be ready (about 30 seconds)
# The API will automatically run migrations and seed data
```

### Access the Application
- **Frontend**: http://localhost:3000 (React Application)
- **API**: http://localhost:5001 (Flask Backend)
- **Health Check**: http://localhost:5001/health
- **API Status**: http://localhost:5001/api/status
- **Database**: localhost:3306 (MySQL)

## 🐳 Docker Commands

### Using Makefile (Recommended)
```bash
make help          # Show all available commands
make build         # Build Docker images
make up            # Start containers
make down          # Stop containers
make logs          # View logs
make test          # Run tests
make shell         # Access API container
make clean         # Clean up everything
```

### Using Docker Compose Directly
```bash
docker-compose build              # Build images
docker-compose up -d              # Start in background
docker-compose logs -f api        # Follow API logs
docker-compose exec api bash      # Access API container
docker-compose down               # Stop containers
```

## 🗄️ Database Management

### Migrations
```bash
# Initialize migrations (first time only)
docker-compose exec api flask db init

# Create new migration
docker-compose exec api flask db migrate -m "Description"

# Apply migrations
docker-compose exec api flask db upgrade

# Rollback migration
docker-compose exec api flask db downgrade
```

### Seed Data
```bash
# Seed default data
docker-compose exec api python seed_data.py

# Or use make command
make seed
```

## 🧪 Testing

```bash
# Run all tests
make test

# Or directly
docker-compose exec api python -m pytest tests/ -v
```

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Products
- `GET /api/products` - List products
- `GET /api/products/{id}` - Get product details
- `POST /api/products` - Create product (admin)
- `PUT /api/products/{id}` - Update product (admin)
- `DELETE /api/products/{id}` - Delete product (admin)

### Categories
- `GET /api/categories` - List categories
- `POST /api/categories` - Create category (admin)

### Cart
- `GET /api/cart` - Get user cart
- `POST /api/cart/add` - Add item to cart
- `PUT /api/cart/update` - Update cart item
- `DELETE /api/cart/remove` - Remove cart item
- `DELETE /api/cart/clear` - Clear cart

### Orders
- `GET /api/orders` - List user orders
- `GET /api/orders/{id}` - Get order details
- `POST /api/orders` - Create order
- `POST /api/orders/from-cart` - Create order from cart
- `PUT /api/orders/{id}/status` - Update order status (admin)

### Order Statuses
- `GET /order-statuses` - List order statuses
- `POST /order-statuses` - Create order status (admin)

## 🔧 Development

### Local Development with Hot Reload
The Docker setup includes volume mounting for real-time code changes:

```bash
# Start development environment
make up

# View logs in real-time
make logs

# Make code changes - they'll be reflected immediately
```

### Frontend Development
The React frontend is containerized and includes:

- **Hot Module Replacement**: Changes reflect immediately
- **Nginx Proxy**: API calls are proxied to backend
- **Environment Configuration**: Configurable via .env files

```bash
# Frontend-specific commands
docker-compose logs -f frontend    # View frontend logs
docker-compose exec frontend sh    # Access frontend container

# Local development (alternative)
cd frontend
npm install
npm start                          # Runs on http://localhost:3000
```

### Frontend Structure
```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/        # React components
│   ├── context/          # State management
│   ├── hooks/            # Custom hooks
│   ├── services/         # API services
│   ├── utils/            # Utility functions
│   └── styles/           # CSS files
├── Dockerfile            # Container configuration
├── nginx.conf           # Nginx configuration
└── package.json         # Dependencies
```

### Environment Variables
Key environment variables (configured in `.env.docker`):

- `FLASK_ENV=development` - Flask environment
- `FLASK_DEBUG=True` - Enable debug mode
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Flask secret key
- `CORS_ORIGINS` - Allowed CORS origins

## 🛡️ Security Features

- Password hashing with bcrypt
- Session-based authentication
- CORS protection
- SQL injection prevention with SQLAlchemy ORM
- Input validation and sanitization

## 📈 Production Deployment

For production deployment:

1. Update environment variables in `.env.docker`
2. Set `FLASK_ENV=production`
3. Use strong passwords and secret keys
4. Configure proper CORS origins
5. Set up SSL/TLS certificates
6. Configure backup strategies

## 🔍 Troubleshooting

### Common Issues

**Containers won't start:**
```bash
# Check container status
make status

# View logs
make logs

# Clean and rebuild
make clean
make build
make up
```

**Database connection issues:**
```bash
# Check MySQL container health
docker-compose exec mysql mysqladmin ping

# Verify environment variables
docker-compose exec api env | grep DB
```

**Migration issues:**
```bash
# Reset migrations
docker-compose exec api rm -rf migrations/
make init
```

### Logs and Debugging
```bash
# API logs
docker-compose logs -f api

# MySQL logs
docker-compose logs -f mysql

# All logs
docker-compose logs -f
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test with `make test`
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.