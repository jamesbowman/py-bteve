import sys

c1_fmt = """
STATIC mp_obj_t _{lname}(mp_obj_t self {arglist}) {{
{unpacks}
    C4(self, {expr});
    return mp_const_none;
}}
STATIC MP_DEFINE_CONST_FUN_OBJ_{n1}({lname}_obj, _{lname});
"""

c4_fmt = """
STATIC mp_obj_t _{lname}(size_t n_args, const mp_obj_t *args) {{
{unpacks}
    C4(args[0], {expr});
    return mp_const_none;
}}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN({lname}_obj, {n1}, {n1}, _{lname});
"""

if __name__ == "__main__":
    o = open("gen_api.h", "wt")
    # o = sys.stdout
    decls = []
    for l in open("api"):
        (name, args, expr) = l.split(maxsplit = 2)
        if args == ".":
            args = []
        else:
            args = args.split(",")
        lname = name.lower()
        arglist = "".join([", mp_obj_t a" + str(i) for i in range(len(args))])
        n1 = len(args) + 1;

        if len(args) < 3:
            unpacks = "\n".join(["    uint32_t {0} = mp_obj_get_int_truncated(a{1});".format(nm, i) for (i, nm) in enumerate(args)])
            f = c1_fmt
        else:
            unpacks = "\n".join(["    uint32_t {0} = mp_obj_get_int_truncated(args[{1}]);".format(nm, i) for (i, nm) in enumerate(args, 1)])
            f = c4_fmt
        o.write(f.format(**locals()))
        n = len(decls)
        decls.append("stem_locals_dict_table[{n}] = (mp_map_elem_t){{ MP_OBJ_NEW_QSTR(MP_QSTR_{name}), MP_OBJ_FROM_PTR(&{lname}_obj) }};".format(**locals()))
        print("    f." + name + "(" + ",".join([c for c,_ in zip("abcdefg", args)]) + ")")
    o.write("#define N_METHODS {0}\n".format(len(decls)))
    o.write("#define METHOD_SETUP do {{ {0} }} while (0)\n".format(" ".join(decls)))
    o.close()
