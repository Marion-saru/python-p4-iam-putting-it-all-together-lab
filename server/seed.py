#!/usr/bin/env python3

from app import app
from models import db, User, Recipe

with app.app_context():
    
    # Clear existing data
    Recipe.query.delete()
    User.query.delete()
    
    # Create users
    user1 = User(
        username="chef_mario",
        image_url="https://example.com/mario.jpg",
        bio="Professional chef with 20 years of experience"
    )
    user1.password_hash = "password123"
    
    user2 = User(
        username="home_cook_jane",
        image_url="https://example.com/jane.jpg",
        bio="Home cooking enthusiast who loves trying new recipes"
    )
    user2.password_hash = "password456"
    
    # Create recipes
    recipe1 = Recipe(
        title="Classic Margherita Pizza",
        instructions="Start by making the dough with flour, water, yeast, and salt. Let it rise for 2 hours. Roll out the dough and add tomato sauce, fresh mozzarella, and basil leaves. Bake in a preheated oven at 450°F for 10-12 minutes until the crust is golden and the cheese is bubbly.",
        minutes_to_complete=45,
        user=user1
    )
    
    recipe2 = Recipe(
        title="Chocolate Chip Cookies",
        instructions="Cream together butter and sugars until light and fluffy. Beat in eggs and vanilla. In a separate bowl, whisk together flour, baking soda, and salt. Gradually mix dry ingredients into wet ingredients. Fold in chocolate chips. Drop spoonfuls of dough onto baking sheets and bake at 375°F for 9-11 minutes.",
        minutes_to_complete=30,
        user=user2
    )
    
    recipe3 = Recipe(
        title="Beef Stir Fry",
        instructions="Cut beef into thin strips and marinate in soy sauce, garlic, and ginger for 30 minutes. Heat oil in a wok or large skillet over high heat. Add beef and cook for 2-3 minutes. Add vegetables like bell peppers, broccoli, and snap peas. Stir-fry for another 3-4 minutes. Serve over rice with additional soy sauce if desired.",
        minutes_to_complete=25,
        user=user1
    )
    
    # Add all objects to session
    db.session.add_all([user1, user2, recipe1, recipe2, recipe3])
    
    # Commit the session
    db.session.commit()
    
    print("Database seeded successfully!")
    print(f"Created {User.query.count()} users")
    print(f"Created {Recipe.query.count()} recipes")