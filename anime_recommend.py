import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

df = pd.read_csv("anime.csv")
df = df.drop(columns=['members', 'type', 'episodes', 'genre'])

# print(df.head())
# print(df.shape)
# print(df.columns)

user_df = pd.read_csv("C:\\Users\\abhi2\\Documents\\Self Learning\\python\\rating.csv")
# print(user_df.head())
# print(user_df.shape)
# print(user_df["user_id"].nunique())
# print(user_df.columns)

anime = pd.merge(df, user_df, on="anime_id")

df_mean = anime.groupby("name")["rated"].mean()
df_mean_sort = df_mean.sort_values(ascending=False)
# print(df_mean_sort.head())

df_count = anime.groupby("name")["rated"].count()
df_count_sort = df_count.sort_values(ascending=False)
# print(df_count_sort.head(n=50))

rating = pd.DataFrame(df_mean)
# print(rating.head())
rating["count"] = pd.DataFrame(df_count)
# print(rating)
rating_sort = rating.sort_values(by="rated", ascending=False)
# print(rating_sort)

# plt.figure(figsize=(10,6))
# plt.hist(rating["count"],bins=70)
# plt.show()
# sns.jointplot(x="rated", y="count", data=rating, alpha=0.5)
# plt.show()


# anime dataset
# print(anime.head())
anime_pivot_table = anime.pivot_table(index="user_id", columns="name", values="rated")
# print(anime_pivot_table.head())



# function
def predict_anime(anime_name):
    anime_user_rating = anime_pivot_table[anime_name]
    similar_to_anime = anime_pivot_table.corrwith(anime_user_rating)
    correlation_anime = pd.DataFrame(similar_to_anime, columns=["correlation"])
    correlation_anime.dropna(inplace=True)
    correlation_anime = correlation_anime.join(rating["count"])
    predictions = correlation_anime[correlation_anime["count"] > 500].sort_values("correlation", ascending=False)
    return predictions


try:
    prediction = predict_anime("High School DxD")
    print(prediction.head(n=10))
except:
    print("does not match with our dataset")

