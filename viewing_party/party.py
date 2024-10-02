# ------------- WAVE 1 -------------------- #
TITLE = "title"
GENRE = "genre"
RATING = "rating"
WATCHED = "watched"
WATCHLIST = "watchlist"
def create_movie(title, genre, rating):
    if not title or not genre or not rating:
        return None
    return {
        TITLE : title,
        GENRE :genre,
        RATING : rating
        }

def add_to_watched(user_data, movie):
    user_data[WATCHED].append(movie)
    return user_data

def add_to_watchlist(user_data, movie):
    user_data[WATCHLIST].append(movie)
    return user_data

def watch_movie(user_data, title):
    for movie in user_data[WATCHLIST]:
        if movie[TITLE] == title:
            add_to_watched(user_data, movie)
            user_data[WATCHLIST].remove(movie)
            break
    return user_data

# ------------- WAVE 2 -------------------- #

def get_watched_avg_rating(user_data):
    rating_sum = 0
    avg_rating = 0
    if not user_data["watched"]:
        return avg_rating
    
    for movie in user_data["watched"]:
        rating_sum += movie["rating"]
    avg_rating = rating_sum/len(user_data["watched"])

    return avg_rating

def get_most_watched_genre(user_data):
    genre_count={}

    for movie in user_data["watched"]:
        current_genre = movie["genre"]
        current_genre_count = genre_count.get(current_genre, 0)
        genre_count[current_genre] = current_genre_count + 1
   
    popular_genre = None
    popular_count = 0

    for genre, count in genre_count.items():
        if not popular_genre or popular_count < count:
            popular_genre = genre
            popular_count = count
    return popular_genre

# ------------- WAVE 3 -------------------- #

def get_unique_watched(user_data):
    unique_movie_list = user_data["watched"].copy()
    for friend in user_data["friends"]:
        friend_movie_list = friend[WATCHED]
        for movie in friend_movie_list:
            if movie in unique_movie_list:
                unique_movie_list.remove(movie)
    return unique_movie_list

def get_friends_unique_watched(user_data):
    user_movie_list = user_data["watched"].copy()
    friend_unique_list = []
    for friend in user_data["friends"]:
        friend_movie_list = friend["watched"]
        for friend_movie in friend_movie_list:
            if friend_movie not in user_movie_list and friend_movie not in friend_unique_list:
                friend_unique_list.append(friend_movie)
    return friend_unique_list

# ------------- WAVE 4 -------------------- #

def get_available_recs(user_data):
    friends_unique = get_friends_unique_watched(user_data)
    recommendations = []
    for movie in friends_unique:
        if movie["host"] in user_data["subscriptions"] and movie not in recommendations:
            recommendations.append(movie)
    return recommendations

# ------------- WAVE 5 -------------------- #

def get_new_rec_by_genre(user_data):
    recommendations = []

    most_watched_genre = get_most_watched_genre(user_data)
    friend_unique_watched = get_friends_unique_watched(user_data)


    recommendations = [movie for movie in friend_unique_watched if movie["genre"] == most_watched_genre]

    return recommendations

def get_rec_from_favorites(user_data):
    recommendations = []
    user_unique = get_unique_watched(user_data)
    if not user_data["favorites"]:
        return recommendations
    elif not user_data["friends"]:
        recommendations = user_data["favorites"]
        return recommendations
    else:
        for movie in user_data["favorites"]:
            if movie in user_unique:
                recommendations.append(movie)
    return recommendations