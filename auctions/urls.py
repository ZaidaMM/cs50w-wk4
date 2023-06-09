from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path('add_to_watchlist/<int:listing_id>', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:listing_id>', views.remove_from_watchlist, name='remove_from_watchlist'),
    path("watchlist", views.watchlist, name="watchlist"),
    path("new_bid/<int:listing_id>", views.new_bid, name="new_bid"),
    path("close_bid/<int:listing_id>", views.close_bid, name="close_bid"),
    path("new_comment/<int:listing_id>", views.new_comment, name="new_comment"),
    path("category", views.category, name="category"),
    path("listingsByCategory/<str:category>", views.listingsByCategory, name="listingsByCategory"),
]
