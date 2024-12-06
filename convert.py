#!/usr/bin/env python3

import sys


def generate_uml_comment(class_name, class_body):
    return f"""/**
@startuml
class {class_name} {{
{''.join(class_body)}
}}
@enduml
*/"""

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    list_of_classes = []

    with open(input_file, 'r') as uml:
        inside_class = False
        private = []
        protected = []
        public = []
        class_body = ""
        class_name = ""
        for line in uml:
            stripped_line = line.strip()
            if stripped_line.startswith('class '):
                inside_class = True
                class_name = stripped_line.split()[1].strip().rstrip('{')
                class_body = stripped_line + "\n"
            if inside_class:
                if stripped_line.startswith('-'):
                    private.append(stripped_line+'\n')
                elif stripped_line.startswith('#'):
                    protected.append(stripped_line+'\n')
                elif stripped_line.startswith('+'):
                    public.append(stripped_line+'\n')
                if not (stripped_line.startswith('class ') or stripped_line.endswith('}')):
                    class_body += line

            if stripped_line.endswith('}') and inside_class:
                inside_class = False
                class_body = []
                class_body.extend(private + protected + public)
                list_of_classes.append((class_name, class_body))
                private.clear()
                protected.clear()
                public.clear()
    
    starting_points = []
    
    with open(output_file, 'r') as out:
        lines = out.readlines()
        i = 0
        for line in lines:
            i += 1
            if line.startswith('class '):
                starting_points.append(i)
    
    with open(output_file, 'w') as out:
        for i, start in enumerate(starting_points):
            before = lines[:start-1]
            after = lines[start-1:]
            out.write(''.join(before))
            if i < len(list_of_classes):
                class_name, class_body = list_of_classes[i]
                out.write(generate_uml_comment(class_name, class_body))
                out.write("\n\n")
            out.write(''.join(after))