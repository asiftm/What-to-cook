def simple():
    import random

    recipe_dict = scrape()
    random_key = random.choice(list(recipe_dict.keys()))
    # dish = output_format(recipe_dict, random_key)

    output_pdf(recipe_dict, random_key)


def course_specific(chosen_course):
    import random
    import os

    chosen_course = chosen_course.lower()
    recipe_dict = scrape()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = '../data/recipe_course.csv'
    file_path = os.path.join(current_dir, file_name)

    file = open(file_path).read().split('\n')
    course_specific_lst = []
    for i in file:
        if i.startswith(chosen_course):
            lst = i.split(',')
            for j in range(1, len(lst)):
                if len(lst[j]) > 0:
                    course_specific_lst.append(lst[j])

    random_key = random.choice(course_specific_lst)
    while random_key not in recipe_dict.keys():
        random_key = random.choice(course_specific_lst)

    output_pdf(recipe_dict, random_key)


def seasonal():
    import datetime
    import random
    import os

    current_month = datetime.datetime.now().strftime("%B")  # getting current month

    recipe_dict = scrape()
    random_key = random.choice(list(recipe_dict.keys()))

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = '../data/vegetable.csv'
    file_path = os.path.join(current_dir, file_name)

    file = open(file_path).read().split('\n')
    all_ingredients = file[0].split(',')
    for i in file:
        if i.startswith(current_month):
            month_ingredients = i.rstrip(',').replace(f'{current_month},', '').split(',')
            condition = False
            while not condition:
                dish = output_format(recipe_dict, random_key)
                for j in range(1, len(all_ingredients)):
                    if all_ingredients[j].strip().lower() in dish and all_ingredients[
                        j].strip() not in month_ingredients:
                        random_key = random.choice(list(recipe_dict.keys()))
                        break
                    if j == len(all_ingredients) - 1:
                        condition = True
            break
    output_pdf(recipe_dict, random_key)


def combined(chosen_course):
    import random
    import datetime
    import os

    current_month = datetime.datetime.now().strftime("%B")
    dish = ''
    random_key = ''

    recipe_dict = scrape()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = '../data/recipe_course.csv'
    file_path = os.path.join(current_dir, file_name)

    file = open(file_path).read().split('\n')

    chosen_course = chosen_course.lower()
    course_specific_lst = []
    for i in file:
        if i.startswith(chosen_course):
            lst = i.split(',')
            for j in range(1, len(lst)):
                if len(lst[j]) > 0:
                    course_specific_lst.append(lst[j])
            break

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = '../data/vegetable.csv'
    file_path = os.path.join(current_dir, file_name)

    file = open(file_path).read().split('\n')
    all_ingredients = file[0].split(',')
    for i in file:
        if i.startswith(current_month):
            month_ingredients = i.rstrip(',').replace(f'{current_month},', '').split(',')
            condition = False
            while not condition:
                random_key = random.choice(course_specific_lst)
                dish = output_format(recipe_dict, random_key)
                for j in range(1, len(all_ingredients)):
                    if all_ingredients[j].strip().lower() in dish and all_ingredients[j].strip() not in month_ingredients:
                        random_key = random.choice(list(recipe_dict.keys()))
                        break
                    if j == len(all_ingredients) - 1:
                        condition = True
            break
    output_pdf(recipe_dict, random_key)


def scrape():
    from bs4 import BeautifulSoup
    import requests

    recipe_dict = {}  # each recipe will be in this dict which will be added to the all_recipes list. the key of this dict is recipe name and the value is ingredients and procedures

    ingredients_procedure_lst = []  # this list will have two items, all ingredients and procedure
    ingredients = ''
    procedure = ''
    recipe_name = ''

    # two (3)
    try:
        # https://www.internationalcuisine.com/category/rwanda/
        lst = ['rwandan-hard-boiled-eggs', 'rwandan-goat-brochettes', 'rwandan-mandazi']
        for i in lst:
            ingredients_procedure_lst = []
            ingredients = ''
            procedure = ''
            recipe_name = ''

            url = f'https://www.internationalcuisine.com/{i}/'
            response = requests.get(url)
            html_txt = response.text
            soup = BeautifulSoup(html_txt, 'html.parser')

            # recipe_name
            name_tags = soup.find('h2', {'class': 'wprm-recipe-name wprm-block-text-bold'})
            recipe_name = name_tags.text.replace('Rwandan ', '')

            # ingredients
            ingredients_tags = soup.find_all('li', {'class': 'wprm-recipe-ingredient'})
            txt = ''
            for tag in ingredients_tags:
                txt = txt + tag.text + ','
            ingredients = txt.rstrip(', ')

            # procedure
            procedure_tags = soup.find_all('div', {'class': 'wprm-recipe-instruction-text'})
            txt = ''
            for tag in procedure_tags:
                txt = txt + tag.text + ' '
            procedure = txt.strip()

            ingredients_procedure_lst.append(ingredients)
            ingredients_procedure_lst.append(procedure)
            recipe_dict[recipe_name] = ingredients_procedure_lst
    except:
        ingredients_procedure_lst = []
        ingredients = ''
        procedure = ''
        recipe_name = ''

    # three(1)
    try:
        # https://www.food.com/recipe/rwandan-chicken-457010?ic1=suggestedAsset%7Crwandan
        ingredients_procedure_lst = []
        ingredients = ''
        procedure = ''
        recipe_name = ''

        url = 'https://www.food.com/recipe/rwandan-chicken-457010?ic1=suggestedAsset%7Crwandan'
        response = requests.get(url)
        html_txt = response.text
        soup = BeautifulSoup(html_txt, 'html.parser')

        # recipe_name
        name_tags = soup.find('h1', {'class': 'svelte-1muv3s8'})
        recipe_name = name_tags.text

        # ingredients
        ingredients_tags = soup.find_all('li', {'style': 'display: contents'})
        txt = ''
        for i in ingredients_tags:
            txt = txt + i.text.replace(',', '').replace('\n\n\n', '').replace('  ', ' ').replace('\n', '').replace('  ',
                                                                                                                   ' ').strip() + ', '
        ingredients = txt.rstrip(', ')
        ingredients_procedure_lst.append(ingredients)

        # procedure
        procedure_tags = soup.find_all('li', {'class': 'direction svelte-ovaflp'})
        txt = ''
        for tag in procedure_tags:
            txt = txt + tag.text + ' '
        procedure = txt.rstrip(' ')
        ingredients_procedure_lst.append(procedure)

        recipe_dict[recipe_name] = ingredients_procedure_lst
    except:
        ingredients_procedure_lst = []
        ingredients = ''
        procedure = ''
        recipe_name = ''

    # four(1)
    try:
        # https://www.goway.com/travel-information/africa-middle-east/rwanda/food-and-drink/
        ingredients_procedure_lst = []
        ingredients = ''
        procedure = ''
        recipe_name = ''

        url = 'https://healthiersteps.com/recipe/matoke-recipe/'
        response = requests.get(url)
        html_txt = response.text
        soup = BeautifulSoup(html_txt, 'html.parser')

        # recipe_name
        name_tag = soup.find('h1', {'itemprop': 'headline'})
        recipe_name = name_tag.text.split(' ')[0]

        # ingredients
        ingredients_tags = soup.find_all('strong')
        txt = ''
        for i in ingredients_tags:
            if ':' in i.text and 'Step' not in i.text:
                txt = txt + (i.text.replace(':', '')) + ', '
        ingredients = txt.rstrip(', ')
        ingredients_procedure_lst.append(ingredients)

        # procedures
        txt = ''
        procedure_tags = soup.find_all('p')
        for i in procedure_tags:
            if i.text.startswith('Step'):
                txt = txt + i.text.split(': ')[1] + '\n'
        procedure = txt.rstrip('\n')
        ingredients_procedure_lst.append(procedure)

        recipe_dict[recipe_name] = ingredients_procedure_lst
    except:
        ingredients_procedure_lst = []
        ingredients = ''
        procedure = ''
        recipe_name = ''

    # six(1)
    try:
        # https://blog.firepot.com/recipes/rwandan-ginger-tea-recipe
        ingredients_procedure_lst = []
        ingredients = ''
        procedure = ''
        recipe_name = ''

        url = 'https://blog.firepot.com/recipes/rwandan-ginger-tea-recipe'
        response = requests.get(url)

        html_txt = response.text
        soup = BeautifulSoup(html_txt, 'html.parser')

        # recipe_name
        name_tag = soup.find('div', {'class': 'title-inner-wrapper'})
        recipe_name = name_tag.text.strip().replace('Rwandan ', '').replace(' Recipe', '')

        # ingredients
        ingredients_tags = soup.find('span', {'id': 'hs_cos_wrapper_post_body'})
        txt = ''
        ingredient_condition = False
        procedure_conditon = False
        for i in (ingredients_tags.text.split('\n')):
            if procedure_conditon:
                if i[0].isnumeric():
                    txt = txt + i[3:] + ' '
                else:
                    procedure = txt.strip()
                    break

            if i.startswith('to make:'):
                ingredients = txt.rstrip(',')
                ingredient_condition = False
                txt = ''
                procedure_conditon = True

            if ingredient_condition and len(i) > 1:
                txt = txt + i + ','

            if i.startswith('You will need:'):
                ingredient_condition = True

        ingredients_procedure_lst.append(ingredients)
        ingredients_procedure_lst.append(procedure)
        recipe_dict[recipe_name] = ingredients_procedure_lst
    except:
        ingredients_procedure_lst = []
        ingredients = ''
        procedure = ''
        recipe_name = ''

    # seven (1)
    try:
        # https://www.bigoven.com/recipe/rwandan-beef/2372715

        ingredients_procedure_lst = []
        ingredients = ''
        procedure = ''
        recipe_name = ''

        url = 'https://www.bigoven.com/recipe/rwandan-beef/2372715'
        response = requests.get(url)
        html_txt = response.text
        soup = BeautifulSoup(html_txt, 'html.parser')

        # recipe_name
        recipe_name = soup.find('h1').text.strip()

        # ingredients
        txt = ''
        ingredient_tags = soup.find_all('span', {'class': 'ingredient'})
        for i in ingredient_tags:
            txt = txt + i.text.strip().replace('\n', ' ').replace(';  ', '; ') + ', '
        ingredients = txt.rstrip(', ')

        # procedure
        txt = ''
        procedure_tags = soup.find('div', {'class': 'instructions'}).text.replace('\n', ' ').split('.')
        for i in procedure_tags:
            txt = txt + i.strip() + '.'
        procedure = txt.strip()

        ingredients_procedure_lst.append(ingredients)
        ingredients_procedure_lst.append(procedure)
        recipe_dict[recipe_name] = ingredients_procedure_lst
    except:
        ingredients_procedure_lst = []
        ingredients = ''
        procedure = ''
        recipe_name = ''

    # eight (1)
    try:
        # https://www.supervalue.co.nz/recipes/rewena-bread/

        ingredients_procedure_lst = []
        ingredients = ''
        procedure = ''
        recipe_name = ''

        url = 'https://www.supervalue.co.nz/recipes/rewena-bread/'
        response = requests.get(url)
        html_txt = response.text
        soup = BeautifulSoup(html_txt, 'html.parser')

        name_tag = soup.find('h1', {'class': 'sv-recipe__heading'})
        recipe_name = name_tag.text

        # ingredients
        ingredient_tag = soup.find_all('div', {'class': 'sv-recipe__ingredients'})
        txt = ''
        for i in ingredient_tag:
            lst = i.text.split('\n')
            for j in lst:
                if j.strip() != '' and j.lower() != 'rēwena bug' and j.lower() != 'rēwena bread' and j.lower() != 'ingredients' and j.lower() != 'view method':
                    txt = txt + j.replace(',', '').strip() + ', '
        ingredients = txt.rstrip(', ')

        # procedure
        procedure_tag = soup.find_all('div', {'class': 'sv-recipe__instructions-inner'})
        txt = ''
        for i in procedure_tag:
            lst = i.text.split('\n')
            for j in lst:
                if len(j) > 40:
                    txt = txt + j.strip()
        procedure = txt.strip()

        ingredients_procedure_lst.append(ingredients)
        ingredients_procedure_lst.append(procedure)
        recipe_dict[recipe_name] = ingredients_procedure_lst
    except:
        ingredients_procedure_lst = []
        ingredients = ''
        procedure = ''
        recipe_name = ''

    # nine (1)
    try:
        # https://www.internationalcuisine.com/rwandan-sweet-potato-fries/

        ingredients_procedure_lst = []
        ingredients = ''
        procedure = ''
        recipe_name = ''

        url = 'https://www.internationalcuisine.com/rwandan-sweet-potato-fries/'
        response = requests.get(url)
        html_txt = response.text
        soup = BeautifulSoup(html_txt, 'html.parser')

        name_tag = soup.find('h2', {'class': 'wprm-recipe-name wprm-block-text-bold'})
        recipe_name = name_tag.text

        # ingredients
        ingredient_tag = soup.find_all('li', {'class': 'wprm-recipe-ingredient'})
        txt = ''
        for i in ingredient_tag:
            txt = txt + i.text.strip() + ', '
        ingredients = txt.rstrip(', ')

        # procedure
        procedure_tag = soup.find_all('div', {'class': 'wprm-recipe-instruction-text'})
        txt = ''
        for i in procedure_tag:
            txt = txt + i.text.strip()
        procedure = txt.strip()

        ingredients_procedure_lst.append(ingredients)
        ingredients_procedure_lst.append(procedure)
        recipe_dict[recipe_name] = ingredients_procedure_lst
    except:
        ingredients_procedure_lst = []
        ingredients = ''
        procedure = ''
        recipe_name = ''

    # end
    # now return the recipe_dict dictionary with all the recipes

    return recipe_dict


def output_format(recipe_dict, random_key):
    dish = ''
    random_item = recipe_dict[random_key]

    dish = dish + random_key + '\n'

    dish = dish + 'Ingredients' + '\n'
    for i in random_item[0].split(','):
        if i != '':
            dish = dish + i.strip() + '\n'

    dish = dish + 'Method' + '\n'
    for i in random_item[1].split('.'):
        if i != '':
            dish = dish + i.strip() + '\n'

    return dish


def picture(search_string):
    import json
    import requests

    url = "https://joj-image-search.p.rapidapi.com/v2/"

    querystring = {"q": f"{search_string}", "hl": "en"}

    headers = {
        "X-RapidAPI-Key": "9a81a971b3msh34cb1c391aed569p10a071jsnf95a632ba13e",
        "X-RapidAPI-Host": "joj-image-search.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    json_data = json.loads(response.text)
    #
    img_link = json_data['response']['images'][0]['image']['url']
    return img_link


def output_pdf(recipe_dict, random_key):
    from PIL import ImageDraw, Image, ImageFont
    import os
    import requests
    import io

    pdf = Image.new('RGBA', (2000, 1200), 'white')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_filename = '../data/Techni Sans V2.ttf'
    font_path = os.path.join(current_dir, font_filename)
    font = ImageFont.truetype(font_path, size=24)

    draw = ImageDraw.Draw(pdf)

    random_item = recipe_dict[random_key]
    draw.text((20, 20), random_key, fill='black', font=font)

    # image
    img_link = picture(random_key)
    response = requests.get(img_link)
    img = Image.open(io.BytesIO(response.content))
    new_size = (200, 200)
    img = img.resize(new_size)
    pdf.paste(img, (20, 50))

    txt = 'Ingredients\n'
    for i in random_item[0].split(','):
        if i != '':
            txt = txt + i.strip() + '\n'
    txt = txt + '\nMethods\n'
    for i in random_item[1].split('.'):
        if i != '':
            txt = txt + i.strip() + '.\n'

    draw.text((20, 300), txt, fill='black', font=font)

    pdf = pdf.convert('RGB')
    pdf.save(f'{random_key}.pdf',format='PDF')


