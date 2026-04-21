-- 1. Total number of recipes
SELECT 
  COUNT(r.recipe_name) AS total_recipes  
FROM 
  recipe r;


-- 2. Total numbers of dessert recipes
SELECT
  COUNT(r.recipe_name) AS total_dessert
FROM 
  recipe r
INNER JOIN
  type_course tcr ON r.type_course_id = tcr.type_course_id
WHERE
  tcr.type_course = 'Dessert';


-- 3. All Italian recipes
SELECT 
  r.recipe_name AS italian_recipes
FROM 
 recipe r
INNER JOIN
  type_cuisine tc ON r.type_cuisine_id = tc.type_cuisine_id
WHERE 
  tc.type_cuisine = 'Italian';


-- 4. Ingredients used in recipe 'Spaghetti Bolognese'
SELECT
 ri.ingredient AS ingredients
FROM recipe_ingredient ri
WHERE
  ri.recipe_name = 'Spaghetti Bolognese';


-- 5. Top 5 Most frequently used ingredients in Indian Cuisine
SELECT
  ri.ingredient AS ingredient,
  COUNT(ri.ingredient) AS count
FROM recipe_ingredient ri
INNER JOIN
  recipe r ON ri.recipe_id = r.recipe_id
INNER JOIN
  type_cuisine tc ON r.type_cuisine_id = tc.type_cuisine_id
WHERE 
  ri.ingredient IS NOT NULL 
  AND ri.ingredient <> ''
  AND tc.type_cuisine = 'Indian'
GROUP BY ri.ingredient
ORDER BY count DESC
LIMIT 5;


-- 6. Count the number of ingredients used per recipe with a rank column
SELECT
  r.recipe_name,
  COUNT(ri.ingredient) AS ingredient_count,
  ROW_NUMBER() OVER (PARTITION BY tc.type_cuisine ORDER BY COUNT(ri.ingredient) DESC) AS rank
FROM 
  recipe_ingredient ri
INNER JOIN
  recipe r ON ri.recipe_id = r.recipe_id
INNER JOIN
  type_cuisine tc ON r.type_cuisine_id = tc.type_cuisine_id
WHERE 
  ri.ingredient IS NOT NULL
GROUP BY 
  tc.type_cuisine, r.recipe_id, r.recipe_name
ORDER BY 
  tc.type_cuisine, rank;
