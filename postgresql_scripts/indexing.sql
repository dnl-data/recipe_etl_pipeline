-- Index on primary keys
CREATE INDEX idx_recipe_id ON recipe_table(recipe_id);
CREATE INDEX idx_ingredient_id ON ingredient_table(ingredient_id);
CREATE INDEX idx_type_course_id ON type_course_table(type_course_id);
CREATE INDEX idx_type_cuisine_id ON type_cuisine_table(type_cuisine_id);
CREATE INDEX idx_type_diet_id ON type_diet_table(type_diet_id);

-- Index on foreign keys (for frequent joins)
CREATE INDEX idx_recipeingredient_recipe_id ON recipe_ingredient_table(recipe_id);
CREATE INDEX idx_recipeingredient_ingredient_id ON recipe_ingredient_table(ingredient_id);

CREATE INDEX idx_recipe_type_course_id ON recipe_table(type_course_id);
CREATE INDEX idx_recipe_type_cuisine_id ON recipe_table(type_cuisine_id);
CREATE INDEX idx_recipe_type_diet_id ON recipe_table(type_diet_id);

-- Index on columns used in filtering
CREATE INDEX idx_recipe_name ON recipe_table(recipe_name);
CREATE INDEX idx_ingredient_name ON ingredient_table(ingredient_name);
