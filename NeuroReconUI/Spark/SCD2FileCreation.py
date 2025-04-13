import json
import pandas as pd
import os

def update_json_by_excel(json_path, excel_path, output_path=None):
    # Safety check for file existence
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Excel file not found: {excel_path}")

    # Set output file name if not provided
    if output_path is None:
        dir_name, file_name = os.path.split(json_path)
        name, ext = os.path.splitext(file_name)
        output_file_name = f"{name}SCD2{ext}"
        output_path = os.path.join(dir_name, output_file_name)

    # Load Excel and clean 'CDC' column
    df = pd.read_excel(excel_path)
    df['CDC'] = df['CDC'].astype(str).str.strip().str.upper()
    df = df[df['CDC'] == 'Y']
    df = df.dropna(subset=['Mapping'])

    # Get list of mappings like "Xref.OrderId"
    mappings = df['Mapping'].dropna().astype(str).str.strip().tolist()

    # Load JSON
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Define transformation logic based on data type
    def update_value(val):
        if isinstance(val, bool):
            return not val
        elif isinstance(val, int):
            return val + 100
        elif isinstance(val, float):
            return round(val + 0.100, 3)
        elif isinstance(val, str):
            try:
                # Skip date strings
                pd.to_datetime(val)
                return val
            except:
                return val + 'test'
        return val

    # Apply updates based on the mappings
    for item in data.get('results', []):
        for path in mappings:
            parts = path.split('.')
            if len(parts) != 2:
                continue  # ignore malformed paths

            parent, key = parts
            if parent in item and isinstance(item[parent], dict):
                if key in item[parent]:
                    original_value = item[parent][key]
                    updated_value = update_value(original_value)
                    item[parent][key] = updated_value
                    # Uncomment to debug:
                    # print(f"Updated {path}: {original_value} -> {updated_value}")

    # Save updated JSON
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

    return os.path.abspath(output_path)


# === Runner Code ===
if __name__ == "__main__":
    jar_dir = os.path.join(os.getcwd(), "Staging", "Incoming", "Product")
    json_file = os.path.join(jar_dir, 'Product.json')
    excel_file = 'F:\\ReconProjects\\NeuroRecon\\Staging\\DataModel\\ProductDataModel.xlsx'

    updated_file = update_json_by_excel(json_file, excel_file)
    print(f"✅ Updated JSON written to: {updated_file}")
