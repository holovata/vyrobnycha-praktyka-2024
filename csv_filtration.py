import pandas as pd

df = pd.read_csv('data/SWOW-EN.R100.csv', na_values=['NA'])

with open('data/100most_used.txt', 'r', encoding='utf-8') as txt_file:
    target_words = [word.strip() for word in txt_file]

# Filter by cue
filtered_df = df[df['cue'].isin(target_words)]

result_df = filtered_df[['cue', 'R1']]

result_df.to_csv('data/100most_used_filtered.csv', index=False)

print("Файл '100most_used_filtered.csv' создан")

df_main = pd.read_csv('data/100most_used_filtered.csv', na_values=['NA'])

df_strength = pd.read_csv('data/strength.SWOW-EN.R1.csv', sep='\t')

with open('data/100most_used.txt', 'r', encoding='utf-8') as txt_file:
    target_words = [word.strip() for word in txt_file]

# Remove cases when resp -> cue
filtered_df = df_main[df_main['cue'].isin(target_words) & ~df_main['R1'].isin(target_words)]

filtered_df = filtered_df.drop_duplicates(subset=['cue', 'R1'])

result_df = filtered_df[['cue', 'R1']]

df_strength = df_strength.drop_duplicates(subset=['cue', 'response', 'R1.Strength'])

merged_df = pd.merge(result_df, df_strength[['cue', 'response', 'R1.Strength']], left_on=['cue', 'R1'], right_on=['cue', 'response'], how='left')

merged_df = merged_df.drop(columns=['response'])

merged_df.to_csv('data/100most_used_filtered_with_strength.csv', index=False)

print("Файл '100most_used_filtered_with_strength.csv' создан")

filtered_strength_df = merged_df[merged_df['R1.Strength'] >= 0.05][['cue', 'R1', 'R1.Strength']]

filtered_strength_df.to_csv('data/100most_used_filtered_with_strength_filtered.csv', index=False)

print("Файл '100most_used_filtered_with_strength_filtered.csv' создан")