
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.response import Response
# from users.models import User



"""  
like_user = pd.read_csv('movies/movie_like_user.csv')
movies = pd.read_csv('movies/movie_movie.csv')

# 데이터프레임을 출력했을때 더 많은 열이 보이도록 함
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 300)
# movieId를 기준으로 like_user 와 movies 를 결합함
movie_like = pd.merge(like_user, movies, on='movie_id')


#유저기반 협업 필터링
title_user = movie_like.pivot_table('love', index=['user_id'], columns='movie_id')

# 좋아요을 부여안한 영화는 그냥 0이라고 부여
title_user = title_user.fillna(0)


# 유저 1~ 번과 유저 1~ 번 간의 코사인 유사도를 구함
user_based_collab = cosine_similarity(title_user, title_user)

# 위는 그냥 numpy 행렬이니까, 이를 데이터프레임으로 변환
user_based_collab = pd.DataFrame(user_based_collab, index=title_user.index, columns=title_user.index)
# print(user_based_collab)

# 로그인 유저와 비슷한 유저를 내림차순으로 정렬한 후에, 상위 10개만 뽑음
# print(user_based_collab[3].sort_values(ascending=False)[:10])
print(user_based_collab)
# # 로그인유저와 가장 비슷한 유저를 뽑고,
user = user_based_collab[3].sort_values( ascending=False)[:10].index[1]
print(user)
# # 비슷한 유저가 좋아했던 영화를 내림차순으로 출력
result = title_user.query(f"user_id == {user}").sort_values(ascending=False, by=user, axis=1)

#영화의 id값만 list로 출력
movie_list = result.columns.values.tolist()
# print(movie_list)

"""  



def ExtractListMachine(request, id):
    like_user = pd.read_csv('movies/movie_like_user.csv')
    movies = pd.read_csv('movies/movie_movie.csv')
    # 데이터프레임을 출력했을때 더 많은 열이 보이도록 함
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 300)
    # movieId를 기준으로 like_user 와 movies 를 결합함
    movie_like = pd.merge(like_user, movies, on='movie_id')
    # print(id)


    #유저기반 협업 필터링
    title_user = movie_like.pivot_table('love', index=['user_id'], columns='movie_id')

    # 좋아요을 부여안한 영화는 그냥 0이라고 부여
    title_user = title_user.fillna(0)


    # 유저 1~ 번과 유저 1~ 번 간의 코사인 유사도를 구함
    user_based_collab = cosine_similarity(title_user, title_user)

    # 위는 그냥 numpy 행렬이니까, 이를 데이터프레임으로 변환
    user_based_collab = pd.DataFrame(user_based_collab, index=title_user.index, columns=title_user.index)

    # 로그인 유저와 비슷한 유저를 내림차순으로 정렬한 후에, 상위 10개만 뽑음
    # print(user_based_collab[id].sort_values(ascending=False)[:10])

    # 로그인유저와 가장 비슷한 유저를 뽑고,
    user = user_based_collab[id].sort_values(ascending=False)[:10].index[1]


    # 비슷한 유저가 좋아했던 영화를 내림차순으로 출력
    result = title_user.query(f"user_id == {user}").sort_values(ascending=False, by=user, axis=1)

    #영화의 id값만 list로 출력
    movie_list = result.columns.values.tolist()
    return movie_list
        
