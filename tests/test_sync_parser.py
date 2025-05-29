import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from utils.sync_parser import parse_actions, parse_resources


resources = parse_resources("data/recursos.txt")
actions = parse_actions("data/acciones.txt")

print("✅ Recursos cargados:")
for r in resources.values():
    print(r)

print("\n✅ Acciones cargadas:")
for a in actions:
    print(a)
