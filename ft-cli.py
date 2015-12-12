# simple script for testing at command line
import ft

CONFIG_TREE_TO_SOLVE = "./example.ft"

def main():
    t = ft.tree()
    print "Create tree from fault tree file"
    t.create_from_ft(CONFIG_TREE_TO_SOLVE)
    print "Prepare tree (check multiple refs)"
    t.prepare()
    print "Solve tree ..."
    t.solve()
    t.print_gate()

main()
