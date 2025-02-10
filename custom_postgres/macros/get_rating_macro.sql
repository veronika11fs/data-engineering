{% macro get_rating() %}

CASE 
    WHEN user_rating >= 4.5 THEN 'Excellent'
    WHEN user_rating >= 4.0 THEN 'Good'
    WHEN user_rating >= 3.5 THEN 'Average'
    ELSE 'Poor'
END as rating_category

{% endmacro %}