from collections import defaultdict
import re
import pandas as pd
import numpy as np

from recipe_extraction import extract_recipes  
uncleaned_df = pd.DataFrame(extract_recipes())  

def del_unwanted_columns(column_name):
    """Delete columns containing a specific string in their name"""
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
  """Reset the index of a column"""
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


def lower_case(column_name):
  """Apply small letters to values of rows"""
  uncleaned_df[column_name] = uncleaned_df[column_name].str.lower()


# Apply lowercase to ingredients
for i in uncleaned_df.columns:
  if i.startswith('Ingredient'):
    lower_case(i)


# Creating new column 'type_diet'
uncleaned_df.insert(3,'type_diet', '')

for i in uncleaned_df['type_course']:
  if i == 'Vegan':
    uncleaned_df.loc[uncleaned_df['type_course'] == i, 'type_diet'] = 'Vegan'
  elif i == 'Vegetarian':
    uncleaned_df.loc[uncleaned_df['type_course'] == i, 'type_diet'] = 'Vegetarian'
  else:
    uncleaned_df.loc[uncleaned_df['type_course'] == i, 'type_diet'] = 'Non-Vegetarian'


# Categorizing 'type_course'
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
  """Creates a table with unique values and IDs"""
  new_table = df[[column_name]].drop_duplicates().reset_index(drop=True)
  new_table.insert(0, id_column_name, range(1, len(new_table) + 1))
  return new_table


type_course_table = creating_table(cleaned_df, 'type_course', 'type_course_id')
type_cuisine_table = creating_table(cleaned_df, 'type_cuisine', 'type_cuisine_id')
type_diet_table = creating_table(cleaned_df, 'type_diet', 'type_diet_id')


# Creating recipe table
recipe_table = creating_table(cleaned_df, 'recipe_name', 'recipe_id')

# Joining tables
recipe_table = recipe_table.merge(cleaned_df[['recipe_name', 'type_course']], on='recipe_name', how='left').drop_duplicates()
recipe_table = recipe_table.merge(type_course_table, on='type_course', how='left')
recipe_table = recipe_table[['recipe_id', 'recipe_name', 'type_course_id']]

recipe_table = recipe_table.merge(cleaned_df[['recipe_name', 'type_cuisine']], on='recipe_name', how='left').drop_duplicates()
recipe_table = recipe_table.merge(type_cuisine_table, on='type_cuisine', how='left')
recipe_table = recipe_table[['recipe_id', 'recipe_name', 'type_course_id','type_cuisine_id']]

recipe_table = recipe_table.merge(cleaned_df[['recipe_name', 'type_diet']], on='recipe_name', how='left').drop_duplicates()
recipe_table = recipe_table.merge(type_diet_table, on='type_diet', how='left')
recipe_table = recipe_table[['recipe_id', 'recipe_name', 'type_course_id','type_cuisine_id','type_diet_id']]


# Creating ingredient table
all_ingredients = []

for col in cleaned_df.columns:
    if col.startswith('Ingredient'):
        all_ingredients.extend(uncleaned_df[col].dropna())
all_ingredients_df = pd.DataFrame(all_ingredients, columns=['ingredient']).drop_duplicates()

def count_word_frequencies(df, column_name):
    """Count word frequencies in ingredients"""
    df[column_name] = df[column_name].str.lower().str.replace(r'[^\w\s]', '', regex=True)
    all_words = df[column_name].str.split().explode()
    word_counts = all_words.value_counts().reset_index()
    word_counts.columns = ['word', 'frequency']
    return word_counts

word_frequencies_df = count_word_frequencies(all_ingredients_df, 'ingredient')

def replace_standardized_words(df, column_name, replace_dict):
    """Standardize ingredient names"""
    df = df.copy()  
    def replace_words(text):
        for word, replace_word in replace_dict.items():
            text = re.sub(rf'\b{word}\b', replace_word, text)
        text = re.sub(r'(s{2,})\b', 's', text)
        text = re.sub(r'(es{2,})\b', 'es', text)
        return text
    df['standardized_ingredient'] = df[column_name].astype(str).apply(replace_words)
    return df

replace_ingredients_name = {
    'almonds': 'almond',
    'plain flour': 'flour',
    
}

standardized_ingredients = replace_standardized_words(all_ingredients_df, 'ingredient', replace_ingredients_name)

ingredient_table = pd.concat([
    all_ingredients_df[['ingredient']].rename(columns={'ingredient': 'original_ingredient'}),
    standardized_ingredients[['standardized_ingredient']]
], axis=1).drop_duplicates(subset=['original_ingredient'])

ingredient_table.columns = ['ingredient_id', 'ingredient']
ingredient_table = creating_table(ingredient_table, 'ingredient', 'ingredient_id')

# Create recipe-ingredient mapping
ingredient_cols = [col for col in cleaned_df.columns if col.startswith('Ingredient')]
long_format = pd.melt(
    cleaned_df,
    id_vars=['recipe_id', 'recipe_name'],
    value_vars=ingredient_cols,
    var_name='ingredient_column',
    value_name='ingredient'
).dropna(subset=['ingredient'])

long_format = (long_format
    .pipe(replace_standardized_words, 'ingredient', replace_ingredients_name)
    .assign(ingredient=lambda x: x['standardized_ingredient'].str.strip().str.lower())
    .drop(columns=['standardized_ingredient', 'ingredient_column'])
    .drop_duplicates(subset=['recipe_id', 'ingredient'])
)

recipe_ingredient_table = (long_format
    .merge(ingredient_table, on='ingredient', how='left')
    .assign(ingredient_id=lambda x: x['ingredient_id'].fillna(0).astype(int))
    [['recipe_id', 'recipe_name','ingredient_id', 'ingredient']]
)

# Prepare the final dictionary of DataFrames to pass to recipe_load
transformed_data = {
    'recipe_table': recipe_table,
    'ingredient_table': ingredient_table,
    'recipe_ingredient_table': recipe_ingredient_table,
    'type_diet_table': type_diet_table,
    'type_course_table': type_course_table,
    'type_cuisine_table': type_cuisine_table
}

def transform_recipes():
    """Validates and returns the transformed recipe data."""
    try:
        total_recipes = len(transformed_data['recipe_table'])
        print(f"✅ {total_recipes} recipes transformed successfully!",flush=True)
        print("✅ All DataFrames ready for loading!",flush=True)
        return transformed_data
        
    except Exception as e:
        print(f"❌ Validation error: {str(e)}",flush=True)
        raise

if __name__ == "__main__":
    import sys
    transform_recipes()
