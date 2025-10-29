# utf16_to_utf8.py

# Input .raw file (UTF-16 encoded)
input_file = "recovered-config.raw"

# Output file (UTF-8 encoded)
output_file = "output.txt"

# Read as UTF-16 and write as UTF-8
with open(input_file, "r", encoding="utf-16") as f_in:
    content = f_in.read()

with open(output_file, "w", encoding="utf-8") as f_out:
    f_out.write(content)

print(f"Successfully converted {input_file} from UTF-16 to UTF-8 → {output_file}")