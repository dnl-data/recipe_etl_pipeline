from collections import defaultdict
import re

import pandas as pd
import numpy as np

uncleaned_df = pd.read_csv("uncleaned_recipes.csv")


def del_unwanted_columns(column_name):
    """Delete columns containing a specific string in their name

    Args:
        df (pd.DataFrame): Input DataFrame
        column_name (str): Substring to match for column removal

    Returns:
        pd.DataFrame: Copy of input DataFrame with matching columns removed

    """
    for column in uncleaned_df.columns:
      if column_name in column:
        del uncleaned_df[column]


del_unwanted_columns('strDrinkAlternate')
del_unwanted_columns('strInstructions')
del_unwanted_columns('strMealThumb')
del_unwanted_columns('strYoutube')
del_unwanted_columns('strImageSource')
del_unwanted_columns('strCreativeCommonsConfirmed')
del_unwanted_columns('dateModified')
del_unwanted_columns('strSource')
del_unwanted_columns('strTags')
del_unwanted_columns('strMeasure')


def reset_id(column_name):
  """Reset the index of a column

    Args:
        column_name (str): Name of column to reset with sequential IDs

    Returns:
        Column with updated IDs
  """
  for index, row in uncleaned_df.iterrows():
    uncleaned_df.at[index, column_name] = index + 1


reset_id('idMeal')


# Changing column names
uncleaned_df.rename(columns={
    'idMeal': 'recipe_id',
    'strMeal': 'recipe_name',
    'strCategory': 'type_course',
    'strArea': 'type_cuisine'
}, inplace=True)


# Removing 'str' from every ingredient columns
for i in uncleaned_df.columns:
  if 'str' in i:
    uncleaned_df.rename(columns={i: i.replace('str', '')}, inplace=True)


def lower_case (column_name):
  """Apply small letters to values of rows in the desired columns

    Args:
     column_name (str) : column where the all the values will turn to lowercase

    Returns:
      Values in desired columns are in lowercase

  """
  uncleaned_df[column_name] = uncleaned_df[column_name].str.lower()


# As there are several ingredient columns, we iterate in each column to apply lower case
for i in uncleaned_df.columns:
  if i.startswith('Ingredient'):
    lower_case(i)


# Creating new column 'type_diet' based on unmodified version of column 'type_course'
uncleaned_df.insert(3,'type_diet', '')

for i in uncleaned_df['type_course']:
  if i == 'Vegan':
    uncleaned_df.loc[uncleaned_df['type_course'] == i, 'type_diet'] = 'Vegan'
  elif i == 'Vegetarian':
    uncleaned_df.loc[uncleaned_df['type_course'] == i, 'type_diet'] = 'Vegetarian'
  else:
    uncleaned_df.loc[uncleaned_df['type_course'] == i, 'type_diet'] = 'Non-Vegetarian'


# Creating new categories in column 'type_course'

for i in uncleaned_df['type_course']:
  if i == 'Dessert':
    uncleaned_df.loc[uncleaned_df['type_course'] == i, 'type_course'] = 'Dessert'
  elif i == 'Side':
    uncleaned_df.loc[uncleaned_df['type_course'] == i, 'type_course'] = 'Side'
  elif i == 'Breakfast':
    uncleaned_df.loc[uncleaned_df['type_course'] == i, 'type_course'] = 'Breakfast'
  elif i == 'Starter':
    uncleaned_df.loc[uncleaned_df['type_course'] == i, 'type_course'] = 'Starter'
  else:
    uncleaned_df.loc[uncleaned_df['type_course'] == i, 'type_course'] = 'Main Course'
    

cleaned_df = uncleaned_df.copy()


def creating_table(df, column_name, id_column_name):
  """
    Creates a table with unique values and an ID column.

    Args:
      df (DataFrame): The original recipe database. # Corrected parameter description
      column_name (str): The name of the column to extract unique values from
      id_column_name (str): The name of the new ID column

    Returns:
      new_table: A table with unique values and an ID column
    """
  new_table = df[[column_name]].drop_duplicates().reset_index(drop=True)
  new_table.insert(0, id_column_name, range(1, len(new_table) + 1))
  return new_table


type_course_table = creating_table(cleaned_df, 'type_course', 'type_course_id')
type_cuisine_table = creating_table(cleaned_df, 'type_cuisine', 'type_cuisine_id')
type_diet_table = creating_table(cleaned_df, 'type_diet', 'type_diet_id')


# Creating 'recipe' table
recipe_table = creating_table(cleaned_df, 'recipe_name', 'recipe_id')

# Joining recipe_table with type_course_table, type_cuisine_table and type_diet_table
recipe_table = recipe_table.merge(cleaned_df[['recipe_name', 'type_course']], on='recipe_name', how='left').drop_duplicates()
recipe_table = recipe_table.merge(type_course_table, on='type_course', how='left')
recipe_table = recipe_table[['recipe_id', 'recipe_name', 'type_course_id']]

recipe_table = recipe_table.merge(cleaned_df[['recipe_name', 'type_cuisine']], on='recipe_name', how='left').drop_duplicates()
recipe_table = recipe_table.merge(type_cuisine_table, on='type_cuisine', how='left')
recipe_table = recipe_table[['recipe_id', 'recipe_name', 'type_course_id','type_cuisine_id']]

recipe_table = recipe_table.merge(cleaned_df[['recipe_name', 'type_diet']], on='recipe_name', how='left').drop_duplicates()
recipe_table = recipe_table.merge(type_diet_table, on='type_diet', how='left')
recipe_table = recipe_table[['recipe_id', 'recipe_name', 'type_course_id','type_cuisine_id','type_diet_id']]


# Creating 'ingredient' table

# Creating an empty list
all_ingredients = []

# Loop through each column and collect ingredients
for col in cleaned_df.columns:
    if col.startswith('Ingredient'):
        all_ingredients.extend(uncleaned_df[col].dropna())
all_ingredients_df = pd.DataFrame(all_ingredients, columns=['ingredient']).drop_duplicates()

def count_word_frequencies(df, column_name):
    """Function to count the frequency of each unique word in the ingredient column.
       Standardizing the ingredients name by replacing a name to most frequent similar word.

       Args:
        df (DataFrame): The original recipe database. # Corrected parameter description
        column_name (str): The name of the column to extract unique values from

      Returns :
        A DataFrame with two columns:
            - 'word' (str): The unique words found in the text
            - 'frequency' (int): The count of each word's occurrences

    """

    # 1. Clean ingredient names (convert to lowercase, remove punctuation)
    df[column_name] = df[column_name].str.lower().str.replace('[^\w\s]', '', regex=True)

    # 2. Split each ingredient into separate words
    all_words = df[column_name].str.split().explode()

    # 3. Count occurrences of each unique word
    word_counts = all_words.value_counts().reset_index()
    word_counts.columns = ['word', 'frequency']

    return word_counts

# Run the function
word_frequencies_df = count_word_frequencies(all_ingredients_df, 'ingredient')

def replace_standardized_words(df, column_name, replace_dict):
    """
    Replace specific standardized ingredient names found within strings in the specified column,
    ensuring words are replaced only once and avoiding excessive trailing 's' characters.

    Args:
      df (DataFrame): The original DataFrame
      column_name (str): The name of the column to extract unique values from
      replace_dict (dictionary) : dictionary mapping words to find (keys) with their standardized replacements (values)

    Returns:
      Modified DataFrame with an additional column named 'standardized_ingredient' containing the processed strings

    """
    def replace_words(text):
        # Replace only whole words using regex
        for word, replace_word in replace_dict.items():
            text = re.sub(rf'\b{word}\b', replace_word, text)  # Replace whole words only

        # Remove excessive trailing 's' (e.g., "mushroomssssss" -> "mushrooms")
        text = re.sub(r'(s{2,})\b', 's', text)  # Fix multiple trailing 's'
        text = re.sub(r'(es{2,})\b', 'es', text)  # Fix multiple "es"

        return text

    # Create a new column for standardized ingredients
    df['standardized_ingredient'] = df[column_name].astype(str).apply(replace_words)
    return df



replace_ingredients_name = {
    'almonds': 'almond',
    'plain flour': 'flour',
    'apples': 'apple',
    'abricot': 'abricots',
    'ball': 'balls',
    'bean': 'beans',
    'blackberrys': 'blackberries',
    'chicken breast': 'chicken',
    'bun': 'buns',
    'carrot': 'carrots',
    'cashew': 'cashews',
    'chestnut': 'chestnuts',
    'chilli': 'chili',
    'garlic clove': 'garlic cloves',
    'coco': 'coconut',
    'egg': 'eggs',
    'fillet': 'fillets',
    'goats': 'goat',
    'leafs': 'leaves',
    'leaf': 'leaves',
    'chicken leg': 'chicken',
    'chicken legs': 'chicken',
    'mincemeat': 'mince',
    'mushroom': 'mushrooms',
    'onion': 'onions',
    'parmigianoreggiano': 'parmesan',
    'peanuts': 'peanut',
    'pickles': 'pickle',
    'potato': 'potatoes',
    'purée': 'puree',
    'rasberry': 'rasberries',
    'seed': 'seeds',
    'smoky': 'smoked',
    'chicken thigh': 'chicken',
    'chicken thighs': 'chicken',
    'tomato': 'tomatoes',
    'tortilla': 'tortillas'
}

# Apply standardization but keep the original ingredient name
standardized_ingredients = replace_standardized_words(all_ingredients_df, 'ingredient', replace_ingredients_name)

# Ensure every unique original ingredient still appears in the final table
ingredient_table = pd.concat([
    all_ingredients_df[['ingredient']].rename(columns={'ingredient': 'original_ingredient'}),
    standardized_ingredients[['standardized_ingredient']]
], axis=1)

ingredient_table = ingredient_table.drop_duplicates(subset=['original_ingredient'])

ingredient_table.columns = ['ingredient_id', 'ingredient']

ingredient_table = creating_table(ingredient_table, 'ingredient', 'ingredient_id')

# Extract ingredient columns
ingredient_cols = [col for col in cleaned_df.columns if col.startswith('Ingredient')]

# Melt the DataFrame into long format keeping all recipe info
long_format = pd.melt(
    cleaned_df,
    id_vars=['recipe_id', 'recipe_name'],  # Keep all recipe details
    value_vars=ingredient_cols,
    var_name='ingredient_column',
    value_name='ingredient'
)

# Clean and standardize ingredients
long_format = (
    long_format
    .dropna(subset=['ingredient'])
    .pipe(replace_standardized_words, 'ingredient', replace_ingredients_name)
    .assign(ingredient=lambda x: x['standardized_ingredient'].str.strip().str.lower())
    .drop(columns=['standardized_ingredient', 'ingredient_column'])
    .drop_duplicates(subset=['recipe_id', 'ingredient'])
)

# Merge with ingredient table to get IDs
recipe_ingredient_table = (
    long_format
    .merge(ingredient_table, on='ingredient', how='left')
    .assign(ingredient_id=lambda x: x['ingredient_id'].fillna(0).astype(int))
    [['recipe_id', 'recipe_name','ingredient_id', 'ingredient']]
)


def df_to_csv(df, csv_name):
    """Export DataFrame to CSV in standardized format"""
    df.to_csv(f"{csv_name}.csv", index=False, encoding='utf-8')
    print(f"Exported {csv_name}.csv with {len(df)} rows")

# Apply to all tables
tables = {
    'recipe_table': recipe_table,
    'ingredient_table': ingredient_table,
    'recipe_ingredient_table': recipe_ingredient_table,
    'type_diet_table': type_diet_table,
    'type_course_table': type_course_table,
    'type_cuisine_table': type_cuisine_table
}

for name, df in tables.items():
    df_to_csv(df, name)
