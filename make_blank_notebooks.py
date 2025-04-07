import os
import json

# Specifiy subdirectories to iterate over
directories = ['Homework','Lecture Notebooks','Discussion Notebooks']

# Define a function for importing and parsing notebook, editing, and writing new file.
def make_blank_notebook(filename):

    # Load original notebook file
    with open(filename) as file:
        lines = file.read()

    # Parse notebook string into JSON
    data = json.loads(lines)

    # Cell indices to delete
    cells_to_delete = []

    # Iterate over cells. Find code cells and remove exectution count, metadata output, source
    for i,cell in enumerate(data['cells']):
        if cell['cell_type'] =='code':
            data['cells'][i]['execution_count'] = None
            data['cells'][i]['metadata'] = {}
            data['cells'][i]['outputs'] = []

            if any("CELL NOT PROVIDED" in s.upper() for s in data['cells'][i]['source']):
                cells_to_delete.append(i)
            
            if i !=0 or not any("import" in s for s in cell['source']):
                if not any("CELL PROVIDED" in s for s in cell['source']):
                    new_line_counter = 0
                    for j, line in enumerate(cell['source']):
                        
                        if (not line.lstrip().startswith('#') and not 'PROVIDED' in cell['source'][j-1]) or 'NOT PROVIDED' in line:
                            if new_line_counter<2:
                                cell['source'][j] = '\n'
                            else:
                                cell['source'][j] = ''
                            new_line_counter+=1
                        else:
                            new_line_counter=0
                        
            if len(data['cells'][i]['source'])>0:
                if data['cells'][i]['source'][-1]=='\n':
                    del data['cells'][i]['source'][-1]

        elif cell['cell_type'] == 'markdown':
            for j,line in enumerate(cell['source']):
                if '<!--answer-->' in line.replace(" ","").lower():
                    if line.split(".")[0].isdigit():
                        newline = line.split(" ")[0]+"  "
                    else:
                        newline = "  "
                    if line.endswith('\n'):
                        newline+='\n\n'
                    data['cells'][i]['source'][j] = newline

    # Reverse the list of cells to delete so that the correct indices will be deleted
    cells_to_delete.reverse()

    # Delete desired indices
    for i in cells_to_delete:
        del data['cells'][i]

    # Write new notebook
    with open(filename.split('.')[0]+'_blank'+'.ipynb','w') as newfile:
        newfile.write(json.dumps(data,indent=4))

# Iterate over all notebooks in specified subdirectories.
pwd = os.getcwd()

for directory in directories:
    for filename in os.listdir(os.path.join(pwd,directory)):
        if filename.endswith('.ipynb') and '_blank' not in filename:
            if filename.startswith('Example'):
                pass
            else:
                print(os.path.join(pwd,directory,filename))
                make_blank_notebook(os.path.join(pwd,directory,filename))