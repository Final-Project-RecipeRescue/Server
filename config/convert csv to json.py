import pandas as pd
import json

def load_and_process_csv(file_path):
    # Load the CSV file
    df = pd.read_csv(file_path, delimiter=';', names=['ingredient', 'ingredientId'])

    # Convert to dictionary with ingredient as key and ingredientId as value
    ingredient_dict = dict(zip(df['ingredient'], df['ingredientId']))

    # Create JSON file for sorted ingredients by name
    sorted_ingredient_dict = dict(sorted(ingredient_dict.items()))
    sorted_json_path = 'sorted_ingredients.json'
    with open(sorted_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(sorted_ingredient_dict, json_file, ensure_ascii=False)

    # Generate JSON file with ingredientId as key and ingredient as value
    id_map_json_path = 'ingredientId_map.json'
    id_map = dict(zip(df['ingredientId'], df['ingredient']))
    with open(id_map_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(id_map, json_file, ensure_ascii=False)

    print(f"Files generated: {sorted_json_path}, {id_map_json_path}")

if __name__ == "__main__":
    csv_file_path = 'C:\\Users\\nissa\\PycharmProjects\\Server\\config\\ingredients.csv'
    load_and_process_csv(csv_file_path)
