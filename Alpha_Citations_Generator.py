#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re


# In[2]:


def parse_bib_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        bib_entries = f.read().strip().split('\n\n')
    
    bib_data = []
    
    for entry in bib_entries:
        entry = entry.strip().replace("ibitem", "\bibitem")  # Fix incorrect characters
        entry_lines = entry.split('\n')
        key_match = re.search(r'\\bibitem\s*\{(.+?)\}', entry_lines[0].strip())
        title_match = re.search(r'\\textbf\{(.+?)\}', entry)
        year_match = re.search(r'(\d{4})', entry)
        
        if not key_match:
            print(f"Skipping entry due to missing key: {entry}")
            continue
        if not title_match:
            print(f"Skipping entry due to missing title: {entry}")
            continue
        if not year_match:
            print(f"Skipping entry due to missing year: {entry}")
            continue
        
        key = key_match.group(1)
        title = title_match.group(1)
        year = year_match.group(1)
        
        # Attempt to extract the first author's last name
        try:
            first_author = title.split(',')[0].split()[0]
        except IndexError:
            print(f"Skipping entry due to unexpected author format: {entry}")
            continue
        
        alpha_key = f"{first_author[:3].capitalize()}{year[-2:]}"  # Create alpha citation label
        
        bib_data.append((first_author.lower(), alpha_key, key, entry))
    
    # Sort the data by the first author's last name
    bib_data.sort(key=lambda x: x[0])
    
    return bib_data


# In[3]:


def format_alpha_bib(bib_data):
    formatted_entries = []
    
    for first_author, alpha_key, key, entry in bib_data:
        new_entry = re.sub(r'\\bibitem\s*\{(.+?)\}', f'\\bibitem[{alpha_key}]{{{key}}}', entry)
        formatted_entries.append(new_entry)
    
    return formatted_entries


# In[4]:


def save_to_file(formatted_entries, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(formatted_entries))


# In[5]:


if __name__ == "__main__":
    input_file = 'citation.txt'  # Replace with input file
    output_file = 'alpha_citations.txt'
    
    bib_data = parse_bib_file(input_file)
    print(f"Number of citations processed: {len(bib_data)}")  # Print the number of citations
    formatted_entries = format_alpha_bib(bib_data)
    save_to_file(formatted_entries, output_file)
    
    print(f"Formatted citations saved to {output_file}")


# In[ ]:




