# Users
users
------
user_id BIGSERIAL PRIMARY KEY
public_id UUID UNIQUE
username VARCHAR(50)
email VARCHAR(255)
password_hash TEXT
bio TEXT
avatar_url TEXT
city VARCHAR(100)
taste_profile JSONB
is_verified BOOLEAN
created_at TIMESTAMPTZ

# Restaurant
restaurants
------
restaurant_id BIGSERIAL PRIMARY KEY
name VARCHAR(200)
address TEXT
city VARCHAR(100)
lat NUMERIC
lng NUMERIC
cuisine_tags TEXT[]
avg_rating NUMERIC
created_by BIGINT
approved BOOLEAN

# Dishes
dishes
------
dish_id BIGSERIAL PRIMARY KEY
name VARCHAR(200)
description TEXT
category VARCHAR(100)
embedding_vector VECTOR(384)
created_at TIMESTAMPTZ

# Restaurant_dish
restaurant_dish
------
restaurant_dish_id BIGSERIAL PRIMARY KEY
restaurant_id BIGINT
dish_id BIGINT
price NUMERIC
love_count INT
avg_rating NUMERIC

# Reviews
reviews
------
review_id BIGSERIAL PRIMARY KEY
user_id BIGINT
restaurant_dish_id BIGINT
rating SMALLINT
text TEXT
sentiment_score NUMERIC
tags TEXT[]
photo_urls TEXT[]
is_deleted BOOLEAN
created_at TIMESTAMPTZ

# Followers
followers
------
follow_id BIGSERIAL PRIMARY KEY
follower_id BIGINT
following_id BIGINT
created_at TIMESTAMPTZ
UNIQUE(follower_id, following_id)

# Lists
lists
------
list_id BIGSERIAL PRIMARY KEY
user_id BIGINT
title VARCHAR(200)
description TEXT
is_public BOOLEAN
created_at TIMESTAMPTZ

# Bookmarks
bookmarks
------
bookmark_id BIGSERIAL PRIMARY KEY
user_id BIGINT
restaurant_dish_id BIGINT

# Comments
comments
------
comment_id BIGSERIAL PRIMARY KEY
user_id BIGINT
review_id BIGINT 
text TEXT
created_at TIMESTAMPTZ

# Likes
------
like_id BIGSERIAL PRIMARY KEY
user_id BIGINT
review_id BIGINT

# Notifications
notifications
------
notification_id BIGSERIAL PRIMARY KEY
user_id BIGINT
type VARCHAR(50) 
message TEXT
is_read BOOLEAN 
created_at TIMESTAMPTZ
