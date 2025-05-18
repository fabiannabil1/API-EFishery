class Config:
    JWT_SECRET_KEY = 'ini_jwtyangsangatpanjangdansusahdihack'
    SWAGGER = {
        "openapi": "3.0.1",
        "info": {
            "title": "API Pelelangan Barang",
            "version": "1.0.0",
            "description": "API Pelelangan Barang"
        },
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Masukkan token JWT Anda. Contoh: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`"
                }
            }
        },
        "security": [
            {
                "BearerAuth": []
            }
        ]
    }
