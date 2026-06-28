CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE users(
    user_id BIGSERIAL PRIMARY KEY,
    public_id UUID UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL, 
    bio TEXT,
    avatar_url TEXT,
    city VARCHAR(100),
    taste_profile JSONB,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE restaurants(
    restaurant_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    lat NUMERIC(9,6) NOT NULL,
    lng NUMERIC(9,6) NOT NULL,
    cuisine_tags TEXT[],
    avg_rating NUMERIc(3,2),
    created_by BIGINT REFERENCES users(user_id),
    approved BOOLEAN DEFAULT FALSE
);
CREATE TABLE dishes(
    dish_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    embedding_vector VECTOR(384),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE restaurant_dish(
    restaurant_dish_id BIGSERIAL PRIMARY KEY,
    restaurant_id BIGINT NOT NULL REFERENCES restaurants(restaurant_id),
    dish_id BIGINT NOT NULL REFERENCES dishes(dish_id),
    price NUMERIC(8,2),
    love_count INT DEFAULT 0,
    avg_rating NUMERIC(3,2)
);
CREATE TABLE reviews(
    review_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    restaurant_dish_id BIGINT NOT NULL REFERENCES restaurant_dish(restaurant_dish_id),
    rating SMALLINT CHECK (rating BETWEEN 1 AND 5),
    text TEXT,
    sentiment_score NUMERIC(4,3),
    tags TEXT[],
    photo_urls TEXT[],
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE followers(
    follow_id BIGSERIAL PRIMARY KEY,
    follower_id BIGINT NOT NULL REFERENCES users(user_id),
    following_id BIGINT NOT NULL REFERENCES users(user_id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(follower_id, following_id)
);
CREATE TABLE lists(
    list_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE bookmarks(
    bookmark_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    restaurant_dish_id BIGINT NOT NULL REFERENCES restaurant_dish(restaurant_dish_id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id,restaurant_dish_id)
);
CREATE TABLE comments(
    comment_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    review_id BIGINT NOT NULL REFERENCES reviews(review_id), 
    text TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE likes(
    like_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    review_id BIGINT NOT NULL REFERENCES reviews(review_id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id,review_id)
);
CREATE TABLE notifications(
    notification_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);