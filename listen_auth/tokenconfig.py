from datetime import timedelta


JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': timedelta(minutes=3),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(hours=2),
    'REFRESH_SECRET': 'refresh-insecure-h2ks^!ij@(=5$6333333_w4ye_u3txd$8d^p5k^%9xw_&k%b*',
    'ACCESS_SECRET': 'access-insecure-h2ks^!ij@(=5$6fa&7*z_w4ye_u3txd$8d111%9xw_&k%ba*',
}