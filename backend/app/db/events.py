from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.review import Review
from app.models.dish import RestaurantDish
from app.models.restaurant import Restaurant

def update_ratings(mapper, connection, target):
    # This function calculates the new avg_rating for the restaurant_dish
    # and the overall restaurant whenever a review is inserted, updated, or deleted.
    session = Session(bind=connection)
    
    # 1. Update RestaurantDish
    restaurant_dish_id = target.restaurant_dish_id
    
    avg_rating_query = session.query(func.avg(Review.rating)).filter(
        Review.restaurant_dish_id == restaurant_dish_id,
        Review.is_deleted == False
    )
    new_avg = avg_rating_query.scalar()
    
    love_count_query = session.query(func.count(Review.review_id)).filter(
        Review.restaurant_dish_id == restaurant_dish_id,
        Review.rating >= 4,
        Review.is_deleted == False
    )
    new_love_count = love_count_query.scalar()
    
    rd = session.query(RestaurantDish).get(restaurant_dish_id)
    if rd:
        rd.avg_rating = new_avg
        rd.love_count = new_love_count
        
        # 2. Update overall Restaurant avg_rating
        rest_id = rd.restaurant_id
        rest_avg_query = session.query(func.avg(Review.rating)).join(
            RestaurantDish, Review.restaurant_dish_id == RestaurantDish.restaurant_dish_id
        ).filter(
            RestaurantDish.restaurant_id == rest_id,
            Review.is_deleted == False
        )
        new_rest_avg = rest_avg_query.scalar()
        
        restaurant = session.query(Restaurant).get(rest_id)
        if restaurant:
            restaurant.avg_rating = new_rest_avg
            
    session.commit()

# Note: Asyncio with SQLAlchemy events can be tricky, 
# for standard triggers it might be better to implement them in Alembic using raw SQL triggers
# But for now we use SQLAlchemy core events with synchronous connections provided by the event listener.

event.listen(Review, 'after_insert', update_ratings)
event.listen(Review, 'after_update', update_ratings)
event.listen(Review, 'after_delete', update_ratings)
