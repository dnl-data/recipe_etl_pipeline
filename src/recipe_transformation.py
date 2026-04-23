from collections import defaultdict
import re
import pandas as pd
import numpy as np

def del_unwanted_columns(df, column_name):
    """Delete columns containing a specific string in their name"""
    for column in df.columns:  
        if column_name in column:
            df = df.drop(columns=[column])
    return df

def reset_id(df, column_name):
    """Reset the index of a column"""
    for index in range(len(df)):
        df.at[index, column_name] = str(index + 1)
    return df

def lower_case(df, column_name):
    """Apply small letters to values of rows"""
    df[column_name] = df[column_name].str.lower()
    return df

def creating_table(df, column_name, id_column_name):
    """Creates a table with unique values and IDs"""
    new_table = df[[column_name]].drop_duplicates().reset_index(drop=True)
    new_table.insert(0, id_column_name, range(1, len(new_table) + 1))
    return new_table

def count_word_frequencies(df, column_name):
    """Count word frequencies in ingredients"""
    df[column_name] = df[column_name].str.lower().str.replace(r'[^\w\s]', '', regex=True)
    all_words = df[column_name].str.split().explode()
    word_counts = all_words.value_counts().reset_index()
    word_counts.columns = ['word', 'frequency']
    return word_counts

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

def transform_recipes(all_recipes):
    """Transform raw recipe data into multiple clean DataFrames"""
    
    # Convert to DataFrame
    uncleaned_df = pd.DataFrame(all_recipes)
    
    # Delete unwanted columns
    unwanted_patterns = [
        'strDrinkAlternate', 'strInstructions', 'strMealThumb', 'strYoutube',
        'strImageSource', 'strCreativeCommonsConfirmed', 'dateModified',
        'strSource', 'strTags', 'strMeasure'
    ]
    for pattern in unwanted_patterns:
        uncleaned_df = del_unwanted_columns(uncleaned_df, pattern)
    
    # Reset ID
    uncleaned_df = reset_id(uncleaned_df, 'idMeal')
    
    # Rename columns
    uncleaned_df.rename(columns={
        'idMeal': 'recipe_id',
        'strMeal': 'recipe_name',
        'strCategory': 'type_course',
        'strArea': 'type_cuisine'
    }, inplace=True)
    
    # Remove 'str' from ingredient columns
    for col in uncleaned_df.columns:
        if 'str' in col:
            uncleaned_df.rename(columns={col: col.replace('str', '')}, inplace=True)
    
    # Apply lowercase to ingredients
    for col in uncleaned_df.columns:
        if col.startswith('Ingredient'):
            uncleaned_df = lower_case(uncleaned_df, col)
    
    # Create type_diet column
    uncleaned_df.insert(3, 'type_diet', '')
    for i in uncleaned_df['type_course']:
        if i == 'Vegan':
            uncleaned_df.loc[uncleaned_df['type_course'] == i, 'type_diet'] = 'Vegan'
        elif i == 'Vegetarian':
            uncleaned_df.loc[uncleaned_df['type_course'] == i, 'type_diet'] = 'Vegetarian'
        else:
            uncleaned_df.loc[uncleaned_df['type_course'] == i, 'type_diet'] = 'Non-Vegetarian'
    
    # Categorize type_course
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
    
    # Create dimension tables
    type_course_table = creating_table(cleaned_df, 'type_course', 'type_course_id')
    type_cuisine_table = creating_table(cleaned_df, 'type_cuisine', 'type_cuisine_id')
    type_diet_table = creating_table(cleaned_df, 'type_diet', 'type_diet_id')
    
    # Create recipe table
    recipe_table = creating_table(cleaned_df, 'recipe_name', 'recipe_id')
    
    # Join recipe with type_course
    recipe_table = recipe_table.merge(cleaned_df[['recipe_name', 'type_course']], on='recipe_name', how='left').drop_duplicates()
    recipe_table = recipe_table.merge(type_course_table, on='type_course', how='left')
    recipe_table = recipe_table[['recipe_id', 'recipe_name', 'type_course_id']]
    
    # Join with type_cuisine
    recipe_table = recipe_table.merge(cleaned_df[['recipe_name', 'type_cuisine']], on='recipe_name', how='left').drop_duplicates()
    recipe_table = recipe_table.merge(type_cuisine_table, on='type_cuisine', how='left')
    recipe_table = recipe_table[['recipe_id', 'recipe_name', 'type_course_id', 'type_cuisine_id']]
    
    # Join with type_diet
    recipe_table = recipe_table.merge(cleaned_df[['recipe_name', 'type_diet']], on='recipe_name', how='left').drop_duplicates()
    recipe_table = recipe_table.merge(type_diet_table, on='type_diet', how='left')
    recipe_table = recipe_table[['recipe_id', 'recipe_name', 'type_course_id', 'type_cuisine_id', 'type_diet_id']]
    
    # Create ingredient table
    all_ingredients = []
    for col in cleaned_df.columns:
        if col.startswith('Ingredient'):
            all_ingredients.extend(cleaned_df[col].dropna())
    
    all_ingredients_df = pd.DataFrame(all_ingredients, columns=['ingredient']).drop_duplicates()
    
    replace_ingredients_name = {
        'almonds': 'almond',
        'plain flour': 'flour',
    }
    
    standardized_ingredients = replace_standardized_words(all_ingredients_df, 'ingredient', replace_ingredients_name)
    
    ingredient_table = pd.concat([
        all_ingredients_df[['ingredient']].rename(columns={'ingredient': 'original_ingredient'}),
        standardized_ingredients[['standardized_ingredient']]
    ], axis=1).drop_duplicates(subset=['original_ingredient'])
    
    ingredient_table.columns = ['ingredient', 'standardized_ingredient']
    ingredient_table = creating_table(ingredient_table, 'standardized_ingredient', 'ingredient_id')
    ingredient_table = ingredient_table.rename(columns={'standardized_ingredient': 'ingredient_name'})
    
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
        .merge(ingredient_table, left_on='ingredient', right_on='ingredient_name', how='left')
        [['recipe_id', 'recipe_name', 'ingredient_id', 'ingredient']]
    )
    
    # Prepare final dictionary
    transformed_data = {
        'recipe_table': recipe_table,
        'ingredient_table': ingredient_table[['ingredient_id', 'ingredient_name']],
        'recipe_ingredient_table': recipe_ingredient_table,
        'type_diet_table': type_diet_table,
        'type_course_table': type_course_table,
        'type_cuisine_table': type_cuisine_table
    }
    
    # Validation
    total_recipes = len(transformed_data['recipe_table'])
    print(f"✅ {total_recipes} recipes transformed successfully!", flush=True)
    print("✅ All DataFrames ready for loading!", flush=True)
    
    return transformed_data

if __name__ == "__main__":
    from recipe_extraction import extract_recipes
    raw_data = extract_recipes()
    transformed = transform_recipes(raw_data)