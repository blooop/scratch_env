from python_template.basic_class import BasicClass

bc = BasicClass()
print(bc.int_var)


bc2 = bc

bc.int_var=100

print(bc)
print(bc2)