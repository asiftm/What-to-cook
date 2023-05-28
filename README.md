# What to cook
This package provides recipes from 'Rwandan' cuisine.

It provides:

1. A pdf file that has the pdf includes the name, a picture, ingredients and method of a recipe
2. Random recipe
3. Random recipe based on the course (lunch,dinner,breakfast,snack)
4. Random recipe based on the availability of the vegetables on current month
5. Random recipe based on current month and course (lunch,dinner,breakfast,snack)


### Installation:
    !pip install whattocook

### Functions:
    def simple():

    def course_specific():

    def seasonal():

    def combined():


### Example 1
    from whattocook import simple
    simple()


### Example 2
    from whattocook import course_specific
    course_specific('breakfast')


### Example 3
    from whattocook import seasonal
    seasonal()


### Example 4
    from whattocook import combined
    combined('lunch')