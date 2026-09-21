import os
import re

def fix_mockito(root_dir):
    pattern = re.compile(r'Mockito\.any\(UUID\.class\)\.toString\(\)')
    count = 0
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith("Test.java"):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                if pattern.search(content):
                    new_content = pattern.sub('Mockito.anyString()', content)
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    print(f"Fixed Mockito bug in {filepath}")
                    count += 1
    print(f"Total files fixed: {count}")

if __name__ == "__main__":
    fix_mockito("/Users/rakesh/Dev/Projects/train ticket web app/train ticket")
