"""
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


ratings = pd.read_csv('rating_mbti.csv')
movies = pd.read_csv('movie_movie.csv')

# 데이터프레임을 출력했을때 더 많은 열이 보이도록 함
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 300)
# movieId를 기준으로 ratings 와 movies 를 결합함
movie_ratings = pd.merge(ratings, movies, on='movie_id')


#유저기반 협업 필터링
title_user = movie_ratings.pivot_table('like', index=['userId', 'description'], columns='title')

# 평점을 부여안한 영화는 그냥 0이라고 부여
title_user = title_user.fillna(0)


# 유저 1~610 번과 유저 1~610 번 간의 코사인 유사도를 구함
user_based_collab = cosine_similarity(title_user, title_user)

# 위는 그냥 numpy 행렬이니까, 이를 데이터프레임으로 변환
user_based_collab = pd.DataFrame(user_based_collab, index=title_user.index, columns=title_user.index)
user_based_collab.head

# 1번 유저와 비슷한 유저를 내림차순으로 정렬한 후에, 상위 10개만 뽑음
user_based_collab[1].sort_values(by='userId', ascending=False)[:10]




# # 1번 유저와 가장 비슷한 20번 유저를 뽑고,
user = user_based_collab[1].sort_values(by='userId', ascending=False)[:10].index[0]
# # 20번 유저가 좋아했던 영화를 평점 내림차순으로 출력
result = title_user.query(f"userId == {user}",).sort_values(ascending=False, by=user, axis=1)

for i in result:
    print(i)
    
"""